from dataclasses import dataclass

@dataclass
class Player:
    id: int
    name: str
    position: str
    goals: int = 0
    assists: int = 0
    shots: int = 0
    toi: float = 0.0          # time on ice in minutes
    corsi_for: int = 0        # shot attempts for while on ice
    corsi_against: int = 0    # shot attempts against while on ice
    xg_for: float = 0.0       # expected goals for
    xg_against: float = 0.0   # expected goals against
    plus_minus: int = 0
    hits: int = 0
    blocked: int = 0
    penalties: int = 0

    @property
    def corsi_pct(self) -> float:
        total = self.corsi_for + self.corsi_against
        return (self.corsi_for / total * 100) if total > 0 else 50.0

    @property
    def xg_pct(self) -> float:
        total = self.xg_for + self.xg_against
        return (self.xg_for / total * 100) if total > 0 else 50.0

    @property
    def points(self) -> int:
        return self.goals + self.assists
