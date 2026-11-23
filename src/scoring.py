import statistics

DEFAULT_WEIGHTS = {
    "avg_last_7": 0.4,
    "avg_last_15": 0.3,
    "avg_last_30": 0.2,
    "avg_season": 0.1,
}

# Standard 9-category league. Edit to match your league's Scoring settings.
DEFAULT_CATEGORIES = ["PTS", "REB", "AST", "STL", "BLK", "3PM", "FG%", "FT%", "TO"]

# Placeholder for a points league. Copy the real values from your Scoring settings.
DEFAULT_POINT_VALUES = {"PTS": 1, "REB": 1, "AST": 1, "STL": 1, "BLK": 1, "TO": -1, "3PM": 1}


def blended_stats(player, weights=None):
    """Blend the recent-window stat dicts into one dict, weighting recent games more.
    A window that is missing for a player is skipped and the weights are renormalized."""
    weights = weights or DEFAULT_WEIGHTS
    totals, used = {}, {}
    for window, weight in weights.items():
        stats = player.get(window)
        if not isinstance(stats, dict):
            continue
        for key, value in stats.items():
            if isinstance(value, (int, float)):
                totals[key] = totals.get(key, 0.0) + weight * value
                used[key] = used.get(key, 0.0) + weight
    return {key: totals[key] / used[key] for key in totals}


def score_points(player, point_values, weights=None):
    stats = blended_stats(player, weights)
    return sum(stats.get(stat, 0.0) * pts for stat, pts in point_values.items())


def make_category_scorer(pool, categories, weights=None):
    """Score a player by summing z-scores across categories, measured against a pool of players."""
    pool_stats = [blended_stats(p, weights) for p in pool]

    def total(key):
        return sum(s.get(key, 0.0) for s in pool_stats)

    fg_pct = total("FGM") / max(total("FGA"), 1e-9)
    ft_pct = total("FTM") / max(total("FTA"), 1e-9)

    def raw(stats, cat):
        # Percentages are weighted by attempts: makes above or below the pool average.
        if cat == "FG%":
            return stats.get("FGM", 0.0) - fg_pct * stats.get("FGA", 0.0)
        if cat == "FT%":
            return stats.get("FTM", 0.0) - ft_pct * stats.get("FTA", 0.0)
        return stats.get(cat, 0.0)

    mean, std = {}, {}
    for cat in categories:
        values = [raw(s, cat) for s in pool_stats]
        mean[cat] = statistics.fmean(values)
        std[cat] = statistics.pstdev(values)

    def scorer(player):
        stats = blended_stats(player, weights)
        score = 0.0
        for cat in categories:
            if std[cat] == 0:
                continue
            z = (raw(stats, cat) - mean[cat]) / std[cat]
            score += -z if cat == "TO" else z  # fewer turnovers is better
        return score

    return scorer


def make_scorer(pool, mode="categories", categories=None, point_values=None, weights=None):
    """Return a function that maps a player dict to one number. Steps 5 and 6 use this."""
    if mode == "points":
        values = point_values or DEFAULT_POINT_VALUES
        return lambda player: score_points(player, values, weights)
    return make_category_scorer(pool, categories or DEFAULT_CATEGORIES, weights)
