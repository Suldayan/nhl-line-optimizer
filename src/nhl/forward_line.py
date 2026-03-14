from dataclasses import dataclass
from src.nhl.player import Player

@dataclass
class ForwardLine:
    line_number: int
    lw: Player | None = None
    center: Player | None = None
    rw: Player | None = None

    @property
    def players(self) -> list[Player]:
        return [p for p in [self.lw, self.center, self.rw] if p]

    @property
    def combined_toi(self) -> float:
        return sum(p.toi for p in self.players)

    @property
    def combined_corsi_pct(self) -> float:
        cf = sum(p.corsi_for for p in self.players)
        ca = sum(p.corsi_against for p in self.players)
        return (cf / (cf + ca) * 100) if (cf + ca) > 0 else 50.0

    @property
    def combined_xg_pct(self) -> float:
        xgf = sum(p.xg_for for p in self.players)
        xga = sum(p.xg_against for p in self.players)
        return (xgf / (xgf + xga) * 100) if (xgf + xga) > 0 else 50.0

    @property
    def combined_points(self) -> int:
        return sum(p.points for p in self.players)
