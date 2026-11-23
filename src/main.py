import datetime
from pathlib import Path

import yaml

from advisor import suggest_moves
from espnClient import get_free_agents, get_league, get_my_team, get_roster, save_snapshot
from lineup import DEFAULT_SLOTS, build_lineup
from report import build_report, write_report
from scoring import make_scorer

ROOT = Path(__file__).resolve().parent.parent


def main():
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text())
    league = get_league()
    team = get_my_team(league)
    roster = get_roster(league, team)
    free_agents = get_free_agents(league)
    save_snapshot(roster, free_agents, path=str(ROOT / "data" / "cache" / "snapshot.json"))

    scorer = make_scorer(roster + free_agents, mode=cfg["scoring_mode"])
    lineup = build_lineup(roster, cfg.get("lineup_slots", DEFAULT_SLOTS), scorer)
    moves = suggest_moves(roster, free_agents, scorer, cfg["min_gain"],
                          cfg["max_suggestions"], cfg["protected_players"])

    day = datetime.date.today().isoformat()
    text = build_report(team.team_name, day, lineup, moves, scorer)
    path = write_report(text, day, folder=ROOT / "reports")
    print(text)
    print(f"Saved to {path}")


if __name__ == "__main__":
    main()
