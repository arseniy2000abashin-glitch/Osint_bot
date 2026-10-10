# language: Python, file: modules/leak.py
import aiohttp
from config import HIBP_API_KEY, HIBP_URL


async def lookup(account: str) -> str:
    if not HIBP_API_KEY:
        return "HIBP ключ не задан"

    headers = {"hibp-api-key": HIBP_API_KEY, "user-agent": "osint-bot"}
    async with aiohttp.ClientSession() as s:
        async with s.get(
            f"{HIBP_URL}/breachedaccount/{account}?truncateResponse=false",
            headers=headers,
        ) as r:
            if r.status == 404:
                return f"<b>{account}</b>\nв утечках не найдено"
            if r.status != 200:
                return f"HIBP ошибка: {r.status}"
            data = await r.json()

    lines = [f"<b>{account}</b>", f"найдено в <b>{len(data)}</b> утечках:", ""]
    for b in sorted(data, key=lambda x: x["BreachDate"], reverse=True):
        lines.append(
            f"• <b>{b['Name']}</b> ({b['BreachDate']})\n"
            f"  домен: {b.get('Domain', '—')}\n"
            f"  утекло: {', '.join(b['DataClasses'])}\n"
            f"  записей: {b.get('PwnCount', 0):,}"
        )
    return "\n".join(lines)
