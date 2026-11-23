DEFAULT_SLOTS = ["PG", "SG", "SF", "PF", "C", "G", "F", "UTIL", "UTIL", "UTIL"]
OUT_STATUSES = {"OUT", "SUSPENSION"}


def is_available(player, out_statuses=OUT_STATUSES):
    """A player can start only if he has a game today and is not ruled out."""
    return bool(player.get("plays_today")) and player.get("injury_status") not in out_statuses


def build_lineup(roster, slots, scorer, out_statuses=OUT_STATUSES):
    """Choose the best legal starters.

    Players are tried from best score to worst. Each one takes an open slot he is
    eligible for, or bumps an earlier starter into a different open slot. This
    never drops a starter once placed, so the best legal group wins.
    """
    candidates = [p for p in roster if is_available(p, out_statuses)]
    candidates.sort(key=scorer, reverse=True)
    owner = {}  # slot index -> candidate index

    def try_place(i, seen):
        for s, slot in enumerate(slots):
            if slot in candidates[i].get("eligible_slots", []) and s not in seen:
                seen.add(s)
                if s not in owner or try_place(owner[s], seen):
                    owner[s] = i
                    return True
        return False

    for i in range(len(candidates)):
        try_place(i, set())

    started = set(owner.values())
    return {
        "starters": [(slots[s], candidates[i]) for s, i in sorted(owner.items())],
        "bench": [p for i, p in enumerate(candidates) if i not in started],
        "unavailable": [p for p in roster if not is_available(p, out_statuses)],
        "empty_slots": [slots[s] for s in range(len(slots)) if s not in owner],
    }
