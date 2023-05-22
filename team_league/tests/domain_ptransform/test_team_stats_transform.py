import dataclasses
from typing import List, Dict

import apache_beam as beam
import pytest
from apache_beam import PCollection
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to
from dacite import from_dict
from toolz.curried import pipe, map

from team_league.domain.exception.team_stats_validation_exception import TeamStatsValidationException
from team_league.domain.team_stats import TeamStats
from team_league.domain.team_stats_raw import TeamStatsRaw, TEAM_NAME_EMPTY_ERROR
from team_league.domain_ptransform.team_stats_transform import TeamStatsTransform
from team_league.root import ROOT_DIR
from team_league.tests.testing_helper import log_element, load_file_as_dict


class TestTeamStatsTransform:

    def test_given_input_teams_stats_raw_without_error_when_transform_to_stats_domain_then_expected_output_in_result(
            self):
        with TestPipeline() as p:
            input_teams_stats_raw_file_path = f'{ROOT_DIR}/tests/files/input/input_teams_stats_raw_without_error.json'

            input_teams_stats_raw: List[TeamStatsRaw] = list(
                pipe(load_file_as_dict(input_teams_stats_raw_file_path),
                     map(lambda c: from_dict(data_class=TeamStatsRaw, data=c)))
            )

            # When.
            result_outputs: PCollection[TeamStats] = (
                    p
                    | beam.Create(input_teams_stats_raw)
                    | 'Team stats transform' >> TeamStatsTransform()
            )

            result_outputs_as_dict = (
                    result_outputs
                    | beam.Map(dataclasses.asdict)
            )

            print('################################')
            result_outputs_as_dict | "Print Outputs" >> beam.Map(log_element)

            expected_teams_stats_file_path = f'{ROOT_DIR}/tests/files/expected/expected_teams_stats_without_error.json'
            expected_outputs: List[Dict] = load_file_as_dict(expected_teams_stats_file_path)

            # Then.
            assert_that(result_outputs_as_dict, equal_to(expected_outputs), label='CheckResMatchExpected')

    def test_given_input_teams_stats_raw_with_one_error_when_transform_to_stats_domain_then_validation_exception_is_raised_with_expected_message(
            self):
        with pytest.raises(Exception) as exc_info:
            with TestPipeline() as p:
                input_teams_stats_raw_file_path = f'{ROOT_DIR}/tests/files/input/input_teams_stats_raw_with_one_error_one_good_output.json'

                input_teams_stats_raw: List[TeamStatsRaw] = list(
                    pipe(load_file_as_dict(input_teams_stats_raw_file_path),
                         map(lambda c: from_dict(data_class=TeamStatsRaw, data=c)))
                )

                # When.
                (p
                 | beam.Create(input_teams_stats_raw)
                 | 'Team stats transform' >> TeamStatsTransform())

        # Then.
        assert f"['{TEAM_NAME_EMPTY_ERROR}']" in str(exc_info.value)
        assert TeamStatsValidationException.__name__ in str(exc_info.value)
