from __future__ import annotations

from dataclasses import dataclass, replace
from typing import List

from team_league.domain.team_best_passer_stats import TeamBestPasserStats
from team_league.domain.team_scorer_raw import TeamScorerRaw
from team_league.domain.team_stats_raw import TeamStatsRaw
from team_league.domain.team_top_scorer_stats import TeamTopScorerStats

TEAM_SLOGANS = {
    "PSG": "Paris est magique",
    "Real": "Hala Madrid"
}


@dataclass
class TeamStats:
    teamName: str
    teamScore: int
    teamTotalGoals: int
    teamSlogan: str
    topScorerStats: TeamTopScorerStats
    bestPasserStats: TeamBestPasserStats

    @staticmethod
    def compute_team_stats(team_stats_raw: TeamStatsRaw) -> TeamStats:
        team_scorers: List[TeamScorerRaw] = team_stats_raw.scorers
        top_scorer: TeamScorerRaw = max(team_scorers, key=lambda team_scorer: team_scorer.goals)
        best_passer: TeamScorerRaw = max(team_scorers, key=lambda team_scorer: team_scorer.goalAssists)

        team_total_goals: int = sum(map(lambda t: t.goals, team_scorers))

        top_scorer_stats = TeamTopScorerStats(
            firstName=top_scorer.scorerFirstName,
            lastName=top_scorer.scorerLastName,
            goals=top_scorer.goals,
            games=top_scorer.games
        )
        best_passer_stats = TeamBestPasserStats(
            firstName=best_passer.scorerFirstName,
            lastName=best_passer.scorerLastName,
            goalAssists=best_passer.goalAssists,
            games=best_passer.games
        )

        return TeamStats(
            teamName=team_stats_raw.teamName,
            teamScore=team_stats_raw.teamScore,
            teamSlogan='',
            teamTotalGoals=team_total_goals,
            topScorerStats=top_scorer_stats,
            bestPasserStats=best_passer_stats
        )

    def add_slogan_to_stats(self) -> TeamStats:
        team_slogan: str = TEAM_SLOGANS.get(self.teamName)

        if team_slogan is None:
            raise AttributeError(f'No slogan for team : {team_slogan}')

        return replace(self, teamSlogan=team_slogan)
