# language: Python, file: modules/debts.py
import aiohttp
from datetime import datetime
from config import FSSP_URL


async def lookup(raw: str) -> str:
    try:
        fio_part, bdate = [p.strip() for p in raw.split(",", 1)]
        last, first, *mid = fio_part.split()
        mid = mid[0] if mid else ""
        dt = datetime.strptime(bdate, "%d.%m.%Y").strftime("%d.%m.%Y")
    except Exception:
        return "формат: /debts Иванов Иван Иванович, 01.01.1990"

    params = {
        "token": "",
        "task": f"{last}&{first}&{mid}&{dt}",
        "region": "0",
    }
    async with aiohttp.ClientSession() as s:
        async with s.get(f"{FSSP_URL}/search/phys", params=params) as r:
            if r.status != 200:
                return f"ФССП ошибка: {r.status}"
            task = await r.json()

    task_id = task.get("response", {}).get("task")
    if not task_id:
        return f"не удалось создать задачу: {task}"

    async with aiohttp.ClientSession() as s:
        async with s.get(
            f"{FSSP_URL}/result",
            params={"token": "", "task": task_id},
        ) as r:
            res = await r.json()

    items = res.get("response", {}).get("result", [])
    if not items:
        return f"исполнительных производств не найдено: {last} {first}"

    out = [f"найдено <b>{len(items)}</b> производств:"]
    for it in items[:10]:
        out.append(
            f"• № {it.get('number', '—')} от {it.get('date', '—')}\n"
            f"  сумма: {it.get('sum', '—')} ₽\n"
            f"  отдел: {it.get('department', '—')}\n"
            f"  статус: {it.get('status', '—')}"
        )
    return "\n\n".join(out)
