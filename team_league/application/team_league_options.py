from apache_beam.options.pipeline_options import PipelineOptions


class TeamLeagueOptions(PipelineOptions):

    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument("--project_id", help="GCP Project ID", required=True)
        parser.add_argument("--input_json_file", help="Input Json file path", required=True)
        parser.add_argument("--team_league_dataset", help="Team league dataset", required=True)
        parser.add_argument("--team_stats_table", help="Team stats table", required=True)
