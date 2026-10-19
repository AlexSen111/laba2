import pytest

from streamstats.analysis import calculate_events
from streamstats.errors import EmptySourceError
from streamstats.errors import WrongEventError
from streamstats.errors import WrongLevelError
from streamstats.errors import WrongTimeError
from streamstats.models import validation
from streamstats.models import validation_mode_skip_invalid
from streamstats.parsers import parse_csv


def test_valid_csv(tmp_path):
    test_csv = tmp_path / "basic.csv"
    test_csv.write_text(
        "timestamp,level,source,message\n"
        "2024-01-15T08:00:01Z,DEBUG,sensor-01,Инициализация датчика завершена\n"
        "2024-01-15T08:00:15Z,INFO,sensor-01,Первое измерение получено\n",
        encoding="utf-8",
    )
    assert list(calculate_events(parse_csv(test_csv)).values())[0] == 2
    assert list(parse_csv(test_csv)[0].values())[1] == "DEBUG"
    assert list(parse_csv(test_csv)[1].values())[2] == "sensor-01"


def test_invalid_csv_level(tmp_path):
    test_csv = tmp_path / "basic.csv"
    test_csv.write_text(
        "timestamp,level,source,message\n" "2024-01-15T08:00:01Z,blabla,sensor-01,Инициализация датчика завершена\n",
        encoding="utf-8",
    )
    with pytest.raises(WrongLevelError):
        validation(parse_csv(test_csv))


def test_invalid_csv_event(tmp_path):
    test_csv = tmp_path / "basic.csv"
    test_csv.write_text(
        "timestamp,level,source,message\n"
        "2024-01-15T08:00:15Z,INFO,sensor-01\n"
        "2024-13-15T08:00:15Z,INFO,sensor-01,Первое измерение получено\n"
        "2024-01-15T08:00:15Z,INFO,,Первое измерение получено\n",
        encoding="utf-8",
    )
    with pytest.raises(WrongEventError):
        validation(parse_csv(test_csv))


def test_invalid_csv_timestamp(tmp_path):
    test_csv = tmp_path / "basic.csv"
    test_csv.write_text(
        "timestamp,level,source,message\n"
        "2024-13-15T08:00:15Z,INFO,sensor-01,Первое измерение получено\n"
        "2024-01-15T08:00:15Z,INFO,,Первое измерение получено\n",
        encoding="utf-8",
    )
    with pytest.raises(WrongTimeError):
        validation(parse_csv(test_csv))


def test_invalid_csv_source(tmp_path):
    test_csv = tmp_path / "basic.csv"
    test_csv.write_text(
        "timestamp,level,source,message\n" "2024-01-15T08:00:15Z,INFO,,Первое измерение получено\n",
        encoding="utf-8",
    )
    with pytest.raises(EmptySourceError):
        validation(parse_csv(test_csv))


def test_invalid_csv_skip_invalid(tmp_path):
    test_csv = tmp_path / "basic.csv"
    test_csv.write_text(
        "timestamp,level,source,message\n"
        "2024-01-15T08:00:01Z,blabla,sensor-01,Инициализация датчика завершена\n"
        "2024-01-15T08:00:15Z,INFO,sensor-01\n"
        "2024-13-15T08:00:15Z,INFO,sensor-01,Первое измерение получено\n"
        "2024-01-15T08:00:15Z,INFO,,Первое измерение получено\n",
        encoding="utf-8",
    )
    assert len(validation_mode_skip_invalid(parse_csv(test_csv))[0]) == 0
    assert validation_mode_skip_invalid(parse_csv(test_csv))[1] == 4


def test_empty_csv(tmp_path):
    test_csv = tmp_path / "basic.csv"
    test_csv.write_text(
        "timestamp,level,source,message\n",
        encoding="utf-8",
    )
    assert len(list(parse_csv(test_csv))) == 0
