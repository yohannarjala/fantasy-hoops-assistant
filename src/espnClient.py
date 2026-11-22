import os
import json
from dotenv import load_dotenv
from espn_api.basketball import League


def get_league():
    load_dotenv()
    return League(
        league_id=int(os.environ["ESPN_LEAGUE_ID"]),
        year=int(os.environ["ESPN_YEAR"]),
        espn_s2=os.environ.get("ESPN_S2"),
        swid=os.environ.get("ESPN_SWID"),
    )


def get_my_team(league):
    team_id = int(os.environ["ESPN_TEAM_ID"])
    for team in league.teams:
        if team.team_id == team_id:
            return team
    raise ValueError(f"No team with ID {team_id} in this league")

def player_to_dict(player, league):
    stats = getattr(player, "stats", {}) or {}
    schedule = getattr(player, "schedule", {}) or {}
    period = league.scoringPeriodId
    today_game = schedule.get(period) or schedule.get(str(period))

    def avg(key):
        return (stats.get(f"{league.year}_{key}") or {}).get("avg")

    return {
        "name": player.name,
        "id": getattr(player, "playerId", None),
        "pro_team": getattr(player, "proTeam", None),
        "position": getattr(player, "position", None),
        "eligible_slots": getattr(player, "eligibleSlots", []),
        "injury_status": getattr(player, "injuryStatus", None),
        "plays_today": today_game is not None,
        "opponent": str(today_game.get("team")) if isinstance(today_game, dict) else None,
        "avg_season": avg("total"),
        "avg_last_7": avg("last_7"),
        "avg_last_15": avg("last_15"),
        "avg_last_30": avg("last_30"),
        "percent_owned": getattr(player, "percent_owned", None),
    }


def get_roster(league, team):
    return [player_to_dict(p, league) for p in team.roster]


def get_free_agents(league, size=50):
    return [player_to_dict(p, league) for p in league.free_agents(size=size)]


def save_snapshot(roster, free_agents, path="data/cache/snapshot.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({"roster": roster, "free_agents": free_agents}, f, indent=2, default=str)


if __name__ == "__main__":
    league = get_league()
    team = get_my_team(league)
    roster = get_roster(league, team)
    free_agents = get_free_agents(league)
    save_snapshot(roster, free_agents)
    print(team.team_name, "-", len(roster), "players,", len(free_agents), "free agents")
    for p in roster:
        print(f" - {p['name']:<24} {str(p['injury_status']):<10} plays today: {p['plays_today']}")
