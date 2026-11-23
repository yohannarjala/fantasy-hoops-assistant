import os

from lineup import OUT_STATUSES


def _reason(player):
    status = player.get("injury_status")
    return status if status in OUT_STATUSES else "no game today"


def build_report(team_name, day, lineup, moves, scorer):
    lines = [f"# {team_name}: daily report for {day}", "", "## Today's lineup", ""]
    lines += ["| Slot | Player | Score | Status |", "| --- | --- | --- | --- |"]
    for slot, p in lineup["starters"]:
        lines.append(f"| {slot} | {p['name']} | {scorer(p):.2f} | {p.get('injury_status')} |")
    if lineup["empty_slots"]:
        lines += ["", f"Could not fill: {', '.join(lineup['empty_slots'])}"]

    lines += ["", "## Bench", ""]
    lines += [f"- {p['name']} ({scorer(p):.2f})" for p in lineup["bench"]] or ["- none"]

    lines += ["", "## Not available today", ""]
    lines += [f"- {p['name']}: {_reason(p)}" for p in lineup["unavailable"]] or ["- none"]

    lines += ["", "## Suggested moves", ""]
    if moves:
        lines += [f"- Add {m['add']['name']}, drop {m['drop']['name']} (+{m['gain']:.2f})"
                  for m in moves]
    else:
        lines.append("No moves above the threshold today.")
    return "\n".join(lines) + "\n"


def write_report(text, day, folder="reports"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(str(folder), f"{day}.md")
    with open(path, "w") as f:
        f.write(text)
    return path
