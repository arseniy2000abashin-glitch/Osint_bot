# language: Python, file: modules/court.py
import aiohttp
from config import KAD_URL


async def lookup(inn: str) -> str:
    if not inn.isdigit():
        return "ИНН должен быть числом"

    url = f"{KAD_URL}/Kad/SearchInstances"
    payload = {
        "Page": 1,
        "Count": 25,
        "Courts": [],
        "DateFrom": None,
        "DateTo": None,
        "Sides": [{"Inn": inn, "Name": "", "Type": 1}],
        "CaseType": "G",
    }
    headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0",
    }
    async with aiohttp.ClientSession() as s:
        async with s.post(url, json=payload, headers=headers) as r:
            if r.status != 200:
                return f"kad ошибка: {r.status}"
            data = await r.json()

    cases = data.get("Result", {}).get("Items", [])
    if not cases:
        return f"дел не найдено по ИНН {inn}"

    out = [f"найдено <b>{len(cases)}</b> дел:"]
    for c in cases[:10]:
        out.append(
            f"• № {c.get('CaseNumber', '—')}\n"
            f"  суд: {c.get('CourtName', '—')}\n"
            f"  дата: {c.get('FilingDate', '—')}\n"
            f"  истец: {c.get('Plaintiff', '—')}\n"
            f"  ответчик: {c.get('Respondent', '—')}\n"
            f"  сумма: {c.get('ClaimAmount', '—')} ₽"
        )
    return "\n\n".join(out)
