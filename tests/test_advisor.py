from advisor import suggest_moves


def p(name, score, status="ACTIVE"):
    return {"name": name, "score": score, "injury_status": status}


def score(player):
    return player["score"]


def test_suggests_swap_when_gain_beats_threshold():
    moves = suggest_moves([p("Weak", 1), p("Good", 8)], [p("Hot", 6)], score, min_gain=2)
    assert len(moves) == 1
    assert moves[0]["add"]["name"] == "Hot"
    assert moves[0]["drop"]["name"] == "Weak"
    assert moves[0]["gain"] == 5


def test_no_suggestion_below_threshold():
    assert suggest_moves([p("Weak", 5)], [p("Meh", 6)], score, min_gain=2) == []


def test_injured_free_agent_is_ignored():
    assert suggest_moves([p("Weak", 1)], [p("Hurt", 9, "OUT")], score, min_gain=1) == []


def test_protected_player_is_never_dropped():
    moves = suggest_moves([p("Star", 1), p("Bench", 2)], [p("Hot", 9)], score,
                          min_gain=1, protected=["star"])
    assert moves[0]["drop"]["name"] == "Bench"


def test_max_suggestions_limits_output():
    roster = [p("A", 1), p("B", 2), p("C", 3)]
    fas = [p("X", 10), p("Y", 9), p("Z", 8)]
    assert len(suggest_moves(roster, fas, score, min_gain=1, max_suggestions=2)) == 2


def test_pairs_best_add_with_worst_drop():
    moves = suggest_moves([p("W1", 1), p("W2", 2)], [p("F1", 10), p("F2", 9)], score, min_gain=1)
    assert (moves[0]["add"]["name"], moves[0]["drop"]["name"]) == ("F1", "W1")
    assert (moves[1]["add"]["name"], moves[1]["drop"]["name"]) == ("F2", "W2")
