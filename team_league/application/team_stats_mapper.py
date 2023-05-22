import dataclasses
from datetime import datetime
from typing import Dict

from team_league.domain.team_stats import TeamStats
from team_league.domain.team_stats_raw import TeamStatsRaw


def deserialize(team_stats_raw_as_dict: Dict) -> TeamStatsRaw:
    from dacite import from_dict
    return from_dict(
        data_class=TeamStatsRaw,
        data=team_stats_raw_as_dict
    )


def to_team_stats_bq(team_stats: TeamStats) -> Dict:
    team_stats_as_dict = dataclasses.asdict(team_stats)
    team_stats_as_dict.update({'ingestionDate': datetime.utcnow().isoformat()})

    return team_stats_as_dict
