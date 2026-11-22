import os
from dotenv import load_dotenv
from espn_api.basketball import League


def get_league():
    load_dotenv()
    return League(
        league_id=int(os.environ["1353429738"]),
        year=int(os.environ["2027"]),
        espn_s2=os.environ.get("AEBFPjazABdriaE1h6%2BqjB%2FfFkIgUnorxwgyV7BOjsknlGchmmlULkpRdwi2UAh5XGOF0n4YS9e4%2F0f2rP8wke3bDDM9wdDomhqfY7Ep4%2FYZhUs7zJYiF9WWfnmF%2FRtAT%2By%2B0xu67dxgHosTX3xzPJYhCFijmep2oxX3SNka4Cii6qzZt0%2FxPsJur3WRKNaxEvW2WjyZOkByKDsrcDXcEDWVegVLpC91snIJA5Yjl721lHmvT9E7McfeyGoUt5f0j7gDyrWVoanmIPNL9DDostZkxNxWtj9h%2B6Wn7CjpOh%2FAFQ%3D%3D"),
        swid=os.environ.get("{841A2AA4-A53A-4C27-AECA-DE636C4C2EFE}"),
    )


def get_my_team(league):
    team_id = int(os.environ["24"])
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