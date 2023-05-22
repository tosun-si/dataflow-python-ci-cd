from dataclasses import dataclass


@dataclass
class TeamScorerRaw:
    scorerFirstName: str
    scorerLastName: str
    goals: int
    goalAssists: int
    games: int
