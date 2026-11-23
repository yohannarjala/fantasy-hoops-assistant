OUT_STATUSES = {"OUT", "SUSPENSION"}


def suggest_moves(roster, free_agents, scorer, min_gain=1.0, max_suggestions=3,
                  protected=(), out_statuses=OUT_STATUSES):
    """Pair the best free agents with the weakest droppable players.

    A swap is suggested only if the free agent's score beats the dropped player's
    score by at least min_gain. Injured free agents and protected players are skipped.
    """
    protected = {name.lower() for name in protected}
    droppable = sorted((p for p in roster if p["name"].lower() not in protected), key=scorer)
    targets = sorted((p for p in free_agents if p.get("injury_status") not in out_statuses),
                     key=scorer, reverse=True)

    moves = []
    for add, drop in zip(targets, droppable):
        gain = scorer(add) - scorer(drop)
        if gain < min_gain:
            break  # later pairs only get worse
        moves.append({"add": add, "drop": drop, "gain": gain})
        if len(moves) >= max_suggestions:
            break
    return moves
