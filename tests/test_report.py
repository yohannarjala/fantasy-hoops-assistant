from report import build_report


def player(name, status="ACTIVE"):
    return {"name": name, "injury_status": status}


def scorer(p):
    return 5.0


def lineup(starters=(), bench=(), unavailable=(), empty=()):
    return {"starters": list(starters), "bench": list(bench),
            "unavailable": list(unavailable), "empty_slots": list(empty)}


def test_report_shows_team_date_and_starters():
    text = build_report("Los Patos", "2026-11-23", lineup([("PG", player("Kyrie"))]), [], scorer)
    assert "Los Patos" in text and "2026-11-23" in text
    assert "| PG | Kyrie | 5.00 | ACTIVE |" in text


def test_no_moves_message():
    text = build_report("T", "d", lineup(), [], scorer)
    assert "No moves above the threshold today." in text


def test_moves_are_listed():
    move = {"add": player("Hot"), "drop": player("Cold"), "gain": 2.5}
    text = build_report("T", "d", lineup(), [move], scorer)
    assert "Add Hot, drop Cold (+2.50)" in text


def test_unavailable_players_show_a_reason():
    out = [player("Hurt", "OUT"), player("Rested", "ACTIVE")]
    text = build_report("T", "d", lineup(unavailable=out), [], scorer)
    assert "Hurt: OUT" in text
    assert "Rested: no game today" in text


def test_unfilled_slots_are_flagged():
    text = build_report("T", "d", lineup(empty=["C"]), [], scorer)
    assert "Could not fill: C" in text
