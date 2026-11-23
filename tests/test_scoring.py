import pytest
from scoring import make_scorer, score_points


def test_recent_form_beats_season_average_in_points_mode():
    hot = {"avg_season": {"PTS": 30}, "avg_last_7": {"PTS": 40}}
    cold = {"avg_season": {"PTS": 30}, "avg_last_7": {"PTS": 20}}
    assert score_points(hot, {"PTS": 1}) > score_points(cold, {"PTS": 1})


def test_missing_windows_are_skipped():
    rookie = {"avg_season": {"PTS": 20}, "avg_last_7": None}
    assert score_points(rookie, {"PTS": 1}) == pytest.approx(20)


def test_no_data_scores_zero():
    assert score_points({}, {"PTS": 1}) == 0.0


def test_category_scorer_ranks_star_above_bench():
    star = {"avg_season": {"PTS": 30, "REB": 8, "AST": 7, "STL": 1.5, "BLK": 1, "3PM": 3,
                           "FGM": 10, "FGA": 20, "FTM": 6, "FTA": 7, "TO": 3}}
    mid = {"avg_season": {"PTS": 20, "REB": 5, "AST": 4, "STL": 1, "BLK": 0.5, "3PM": 2,
                          "FGM": 7, "FGA": 15, "FTM": 4, "FTA": 5, "TO": 2}}
    bench = {"avg_season": {"PTS": 10, "REB": 3, "AST": 2, "STL": 0.5, "BLK": 0.2, "3PM": 1,
                            "FGM": 4, "FGA": 10, "FTM": 2, "FTA": 3, "TO": 1}}
    scorer = make_scorer([star, mid, bench])
    assert scorer(star) > scorer(mid) > scorer(bench)


def test_turnovers_hurt_in_category_mode():
    careful = {"avg_season": {"PTS": 20, "TO": 1}}
    sloppy = {"avg_season": {"PTS": 20, "TO": 4}}
    scorer = make_scorer([careful, sloppy], categories=["PTS", "TO"])
    assert scorer(careful) > scorer(sloppy)
