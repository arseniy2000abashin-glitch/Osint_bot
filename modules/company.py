# language: Python, file: modules/company.py
import aiohttp
from config import FNS_API_KEY, FNS_URL


async def lookup(inn: str) -> str:
    if not FNS_API_KEY:
        return "FNS ключ не задан (api-fns.ru)"
    if not inn.isdigit():
        return "ИНН должен быть числом"

    url = f"{FNS_URL}/req"
    params = {"key": FNS_API_KEY, "req": inn, "np": "1"}
    async with aiohttp.ClientSession() as s:
        async with s.get(url, params=params) as r:
            if r.status != 200:
                return f"ФНС ошибка: {r.status}"
            data = await r.json()

    items = data.get("items", [])
    if not items:
        return "не найдено"

    out = []
    for it in items[:3]:
        y = it.get("ЮЛ", {}) or it.get("ИП", {})
        out.append(
            f"<b>{y.get('НаимПолн', '—')}</b>\n"
            f"ИНН: {y.get('ИНН', '—')}\n"
            f"ОГРН: {y.get('ОГРН', '—')}\n"
            f"статус: {y.get('Статус', '—')}\n"
            f"дата рег.: {y.get('ДатаРег', '—')}\n"
            f"адрес: {y.get('АдресПолн', '—')}\n"
            f"руководитель: {(y.get('Руковод') or {}).get('ФИОПолн', '—')}\n"
            f"ОКВЭД: {(y.get('ОснВидДеят') or {}).get('Текст', '—')}"
        )
    return "\n\n".join(out)
