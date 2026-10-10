# language: Python, file: modules/domain.py
import asyncio
import dns.resolver
import aiohttp


async def lookup(domain: str) -> str:
    lines = [f"<b>{domain}</b>"]

    for rectype in ("A", "MX", "NS", "TXT"):
        try:
            ans = dns.resolver.resolve(domain, rectype)
            vals = [str(r) for r in ans][:5]
            lines.append(f"{rectype}: {', '.join(vals)}")
        except Exception:
            pass

    return "\n".join(lines)


SOCIALS = {
    "telegram":  "https://t.me/{}",
    "vk":        "https://vk.com/{}",
    "github":    "https://github.com/{}",
    "reddit":    "https://reddit.com/user/{}",
    "instagram": "https://instagram.com/{}",
    "twitter":   "https://twitter.com/{}",
    "tiktok":    "https://tiktok.com/@{}",
    "youtube":   "https://youtube.com/@{}",
}


async def username_lookup(nick: str) -> str:
    async def check(name, url):
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(
                    url.format(nick),
                    timeout=aiohttp.ClientTimeout(total=8),
                    allow_redirects=True,
                    headers={"User-Agent": "Mozilla/5.0"},
                ) as r:
                    return name, r.status
        except Exception:
            return name, None

    tasks = [check(n, u) for n, u in SOCIALS.items()]
    results = await asyncio.gather(*tasks)

    lines = [f"<b>ник: {nick}</b>"]
    for name, status in results:
        if status == 200:
            lines.append(f"✓ {name}: {SOCIALS[name].format(nick)}")
        elif status == 404:
            lines.append(f"— {name}: свободен")
        else:
            lines.append(f"? {name}: не проверить")
    return "\n".join(lines)
