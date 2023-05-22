import apache_beam as beam
from apache_beam import PCollection

from team_league.domain.team_stats import TeamStats
from team_league.domain.team_stats_raw import TeamStatsRaw


class TeamStatsTransform(beam.PTransform):
    def __init__(self):
        super().__init__()

    def expand(self, inputs: PCollection[TeamStatsRaw]) -> PCollection[TeamStats]:
        return (inputs
                | 'Validate raw fields' >> beam.Map(lambda t_raw: t_raw.validate_fields())
                | 'Compute team stats' >> beam.Map(TeamStats.compute_team_stats)
                | 'Add slogan to team stats' >> beam.Map(lambda t_stats: t_stats.add_slogan_to_stats()))
