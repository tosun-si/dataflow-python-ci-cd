from dataclasses import dataclass


@dataclass
class TeamTopScorerStats:
    firstName: str
    lastName: str
    goals: int
    games: int
