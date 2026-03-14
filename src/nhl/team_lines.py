from dataclasses import dataclass, field
from src.nhl.player import Player
from src.nhl.forward_line import ForwardLine
from src.nhl.defense_pair import DefensePair

@dataclass
class TeamLines:
    team_abbrev: str
    team_name: str
    forward_lines: list[ForwardLine] = field(default_factory=list)
    defense_pairs: list[DefensePair] = field(default_factory=list)
    goalie: Player | None = None

    @property
    def all_forwards(self) -> list[Player]:
        players = []
        for line in self.forward_lines:
            players.extend(line.players)
        return players

    @property
    def all_defensemen(self) -> list[Player]:
        players = []
        for pair in self.defense_pairs:
            players.extend(pair.players)
        return players
