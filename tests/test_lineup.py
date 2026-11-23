from lineup import build_lineup


def player(name, score, slots, plays=True, status="ACTIVE"):
    return {"name": name, "score": score, "eligible_slots": slots,
            "plays_today": plays, "injury_status": status}


def score(p):
    return p["score"]


def names(result):
    return {p["name"] for _, p in result["starters"]}


def test_injured_player_is_skipped():
    roster = [player("Hurt", 10, ["UTIL"], status="OUT"), player("Fit", 5, ["UTIL"])]
    result = build_lineup(roster, ["UTIL"], score)
    assert names(result) == {"Fit"}
    assert [p["name"] for p in result["unavailable"]] == ["Hurt"]


def test_player_without_a_game_is_skipped():
    roster = [player("Off", 10, ["UTIL"], plays=False), player("On", 5, ["UTIL"])]
    assert names(build_lineup(roster, ["UTIL"], score)) == {"On"}


def test_position_rules_are_respected():
    roster = [player("Guard", 10, ["PG", "UTIL"]), player("Big", 9, ["C", "UTIL"])]
    result = build_lineup(roster, ["C", "UTIL"], score)
    assert dict((slot, p["name"]) for slot, p in result["starters"]) == {"C": "Big", "UTIL": "Guard"}


def test_a_starter_moves_to_make_room():
    star = player("Star", 10, ["C", "UTIL"])
    big = player("Big", 9, ["C"])
    result = build_lineup([star, big], ["C", "UTIL"], score)
    assert names(result) == {"Star", "Big"}


def test_extra_players_go_to_the_bench():
    roster = [player("A", 3, ["UTIL"]), player("B", 2, ["UTIL"]), player("C", 1, ["UTIL"])]
    result = build_lineup(roster, ["UTIL", "UTIL"], score)
    assert names(result) == {"A", "B"}
    assert [p["name"] for p in result["bench"]] == ["C"]


def test_unfillable_slots_are_reported():
    roster = [player("Guard", 5, ["PG", "UTIL"])]
    result = build_lineup(roster, ["PG", "C"], score)
    assert result["empty_slots"] == ["C"]
