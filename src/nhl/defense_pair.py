from dataclasses import dataclass
from src.nhl.player import Player

@dataclass
class DefensePair:
    pair_number: int
    ld: Player | None = None
    rd: Player | None = None

    @property
    def players(self) -> list[Player]:
        return [p for p in [self.ld, self.rd] if p]
