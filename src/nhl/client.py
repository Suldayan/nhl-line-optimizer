"""
NHL API client using zmalski's nhl-api-py package.
Docs: https://github.com/zmalski/nhl-api-py
"""

from datetime import date
from nhlpy import NHLClient

client = NHLClient()

def get_live_games() -> list[dict]:
    """Return all games happening today with basic info."""
    today = date.today().strftime("%Y-%m-%d")
    schedule = client.schedule.get_schedule(date=today)

    games = []
    game_week = schedule.get("gameWeek", [])
    for day in game_week:
        for game in day.get("games", []):
            state = game.get("gameState", "")
            if state in ("LIVE", "CRIT", "PRE"):
                games.append({
                    "game_id": game["id"],
                    "state":      state,
                    "period":     game.get("periodDescriptor", {}).get("number", 0),
                    "home":       game["homeTeam"]["abbrev"],
                    "home_score": game["homeTeam"].get("score", 0),
                    "away":       game["awayTeam"]["abbrev"],
                    "away_score": game["awayTeam"].get("score", 0),
                    "venue":      game.get("venue", {}).get("default", "Unknown"),
                })

    return games

def get_game_boxscore(game_id: int) -> dict:
    """Fetch full boxscore for a game (includes rosters, on-ice, stats)."""
    return client.game_center.boxscore(game_id=game_id)

def get_game_play_by_play(game_id: int) -> dict:
    """Fetch play-by-play for a game (shot attempts, goals, penalties)."""
    return client.game_center.play_by_play(game_id=game_id)

def get_player_stats(player_id: int, season: str = "20242025") -> dict:
    """Get season stats for a player."""
    try:
        stats = client.stats.player_career_stats(player_id=player_id)
        # Find the matching season in career stats
        for entry in stats.get("regularSeason", {}).get("subSeasons", []):
            if entry.get("season") == int(season):
                return entry
        # fallback: return most recent season
        seasons = stats.get("regularSeason", {}).get("subSeasons", [])
        return seasons[-1] if seasons else {}
    except Exception:
        return {}

def get_roster(team_abbrev: str) -> list[dict]:
    """Get current season roster for a team."""
    try:
        roster = client.teams.roster(team_abbrev=team_abbrev, season="20242025")
        players = []
        for group in ("forwards", "defensemen", "goalies"):
            for p in roster.get(group, []):
                players.append({
                    "id":       p["id"],
                    "name":     f"{p['firstName']['default']} {p['lastName']['default']}",
                    "position": p.get("positionCode", "?"),
                    "sweater":  p.get("sweaterNumber", "?"),
                })
        return players
    except Exception:
        return []