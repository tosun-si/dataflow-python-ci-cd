from typing import List


class TeamStatsValidationException(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__(self.errors)
