import json
import logging
from typing import Dict

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.options.pipeline_options import PipelineOptions

from team_league.application.team_league_options import TeamLeagueOptions
from team_league.application.team_stats_mapper import deserialize, to_team_stats_bq
from team_league.domain.team_stats import TeamStats


def to_dict(team_stats_raw_as_str: str) -> Dict:
    return json.loads(team_stats_raw_as_str)


def main() -> None:
    logging.getLogger().setLevel(logging.INFO)

    team_league_options = PipelineOptions().view_as(TeamLeagueOptions)
    pipeline_options = PipelineOptions()

    with beam.Pipeline(options=pipeline_options) as p:
        (p
         | 'Read Json file' >> ReadFromText(team_league_options.input_json_file)
         | 'Map str message to Dict' >> beam.Map(to_dict)
         | 'Deserialize to domain dataclass' >> beam.Map(deserialize)
         | 'Validate raw fields' >> beam.Map(lambda t_raw: t_raw.validate_fields())
         | 'Compute team stats' >> beam.Map(TeamStats.compute_team_stats)
         | 'Add slogan to team stats' >> beam.Map(lambda t_stats: t_stats.add_slogan_to_stats())
         | 'Map to team stats bq dicts' >>
         beam.Map(to_team_stats_bq)
         | 'Write team stats to BQ' >> beam.io.WriteToBigQuery(
                    project=team_league_options.project_id,
                    dataset=team_league_options.team_league_dataset,
                    table=team_league_options.team_stats_table,
                    method=beam.io.WriteToBigQuery.Method.FILE_LOADS,
                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                    create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER))


if __name__ == "__main__":
    main()
