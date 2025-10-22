import pytest

from src.processing import filter_by_state, sort_by_date

@pytest.mark.parametrize(
    "input_data, state, output_data",
    [
        (input_data, 'EXECUTED', data_executed),
        (input_data, 'CANCELED', data_canceled),
    ],
)
def test_filter_by_state(input_data, state, output_data):
    assert filter_by_state(input_data, state) == output_data