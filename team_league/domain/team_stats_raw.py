from __future__ import annotations

from dataclasses import dataclass
from typing import List

from team_league.domain.exception.team_stats_validation_exception import TeamStatsValidationException
from team_league.domain.team_scorer_raw import TeamScorerRaw

TEAM_NAME_EMPTY_ERROR = 'Team name should not be null or empty'


@dataclass
class TeamStatsRaw:
    teamName: str
    teamScore: int
    scorers: List[TeamScorerRaw]

    def validate_fields(self) -> TeamStatsRaw:
        if self.teamName is None or self.teamName == '':
            raise TeamStatsValidationException([TEAM_NAME_EMPTY_ERROR])

        return self
