from dataclasses import dataclass


@dataclass
class TeamBestPasserStats:
    firstName: str
    lastName: str
    goalAssists: int
    games: int
