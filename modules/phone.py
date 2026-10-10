# language: Python, file: modules/phone.py
import phonenumbers
from phonenumbers import geocoder, carrier, number_type, PhoneNumberType
import aiohttp
from config import HIBP_API_KEY, HIBP_URL


OPERATOR_MAP = {
    "MTS": "МТС", "MegaFon": "МегаФон", "Beeline": "Билайн",
    "Tele2": "Tele2", "Yota": "Yota", "SberMobile": "СберМобайл",
}


async def lookup(raw: str) -> str:
    try:
        num = phonenumbers.parse(raw, "RU")
    except Exception as e:
        return f"не распознал номер: {e}"

    valid = phonenumbers.is_valid_number(num)
    region = geocoder.description_for_number(num, "ru") or "—"
    op = carrier.name_for_number(num, "ru") or "—"
    op = OPERATOR_MAP.get(op, op)

    ntype = number_type(num)
    types = {
        PhoneNumberType.MOBILE: "мобильный",
        PhoneNumberType.FIXED_LINE: "городской",
        PhoneNumberType.VOIP: "VoIP",
    }
    t = types.get(ntype, "неизвестно")

    leaks = await _hibp(raw)

    lines = [
        f"<b>{raw}</b>",
        f"валиден: {'да' if valid else 'нет'}",
        f"оператор: {op}",
        f"регион: {region}",
        f"тип: {t}",
        f"формат E164: {phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)}",
        "",
        f"<b>утечки:</b>\n{leaks}",
    ]
    return "\n".join(lines)


async def _hibp(account: str) -> str:
    if not HIBP_API_KEY:
        return "HIBP ключ не задан"
    url = f"{HIBP_URL}/breachedaccount/{account}?truncateResponse=false"
    headers = {"hibp-api-key": HIBP_API_KEY, "user-agent": "osint-bot"}
    async with aiohttp.ClientSession() as s:
        async with s.get(url, headers=headers) as r:
            if r.status == 404:
                return "не найдено в утечках"
            if r.status == 200:
                data = await r.json()
                return "\n".join(
                    f"• {b['Name']} ({b['BreachDate']}) — {', '.join(b['DataClasses'])}"
                    for b in data
                )
            return f"HIBP ошибка: {r.status}"
