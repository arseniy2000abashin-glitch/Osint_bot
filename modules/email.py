# language: Python, file: modules/email.py
import aiohttp
import dns.resolver
from config import HIBP_API_KEY, HIBP_URL


async def lookup(addr: str) -> str:
    if "@" not in addr:
        return "неверный формат почты"

    domain = addr.split("@")[1]
    lines = [f"<b>{addr}</b>"]

    try:
        mx = dns.resolver.resolve(domain, "MX")
        lines.append("MX:")
        for r in sorted(mx, key=lambda x: x.preference)[:5]:
            lines.append(f"  • {r.exchange} (prio {r.preference})")
    except Exception:
        lines.append("MX: не найдены")

    lines.append("")
    lines.append("<b>утечки:</b>")
    lines.append(await _hibp(addr))

    return "\n".join(lines)


async def _hibp(account: str) -> str:
    if not HIBP_API_KEY:
        return "HIBP ключ не задан"
    url = f"{HIBP_URL}/breachedaccount/{account}?truncateResponse=false"
    headers = {"hibp-api-key": HIBP_API_KEY, "user-agent": "osint-bot"}
    async with aiohttp.ClientSession() as s:
        async with s.get(url, headers=headers) as r:
            if r.status == 404:
                return "не найдено"
            if r.status == 200:
                data = await r.json()
                return "\n".join(
                    f"• <b>{b['Name']}</b> ({b['BreachDate']})\n  данные: {', '.join(b['DataClasses'])}"
                    for b in data
                )
            return f"HIBP: {r.status}"
