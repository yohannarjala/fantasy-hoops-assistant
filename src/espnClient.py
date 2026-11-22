import os
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


if __name__ == "__main__":
    league = get_league()
    team = get_my_team(league)
    print(team.team_name)
    for player in team.roster:
        print(" -", player.name)
