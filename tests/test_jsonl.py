import pytest

from streamstats.analysis import calculate_events
from streamstats.errors import EmptySourceError
from streamstats.errors import WrongEventError
from streamstats.errors import WrongLevelError
from streamstats.errors import WrongTimeError
from streamstats.models import validation
from streamstats.models import validation_mode_skip_invalid
from streamstats.parsers import parse_jsonl


def test_valid_jsonl(tmp_path):
    test_jsonl = tmp_path / "basic.jsonl"
    test_jsonl.write_text(
        '{"timestamp": "2024-01-15T08:00:01Z", "level": "DEBUG", "source": "sensor-01", "message": "Инициализация датчика завершена"}\n'
        '{"timestamp": "2024-01-15T08:00:15Z", "level": "INFO", "source": "sensor-01", "message": "Первое измерение получено"}\n',
        encoding="utf-8",
    )
    assert list(calculate_events(parse_jsonl(test_jsonl)).values())[0] == 2
    assert list(parse_jsonl(test_jsonl)[0].values())[1] == "DEBUG"
    assert list(parse_jsonl(test_jsonl)[1].values())[2] == "sensor-01"


def test_invalid_jsonl_level(tmp_path):
    test_jsonl = tmp_path / "basic.jsonl"
    test_jsonl.write_text(
        '{"timestamp": "2024-01-15T08:00:01Z", "level": "blabla", "source": "sensor-01", "message": "Инициализация датчика завершена"}\n',
        encoding="utf-8",
    )
    with pytest.raises(WrongLevelError):
        validation(parse_jsonl(test_jsonl))


def test_invalid_jsonl_event(tmp_path):
    test_jsonl = tmp_path / "basic.jsonl"
    test_jsonl.write_text(
        '{"timestamp": "2024-01-15T08:00:01Z", "level": "DEBUG", "source": "sensor-01"}\n',
        encoding="utf-8",
    )
    with pytest.raises(WrongEventError):
        validation(parse_jsonl(test_jsonl))


def test_invalid_jsonl_timestamp(tmp_path):
    test_jsonl = tmp_path / "basic.jsonl"
    test_jsonl.write_text(
        '{"timestamp": "2024-13-15T08:00:15Z", "level": "INFO", "source": "sensor-01", "message": "Первое измерение получено"}\n',
        encoding="utf-8",
    )
    with pytest.raises(WrongTimeError):
        validation(parse_jsonl(test_jsonl))


def test_invalid_jsonl_source(tmp_path):
    test_jsonl = tmp_path / "basic.jsonl"
    test_jsonl.write_text(
        '{"timestamp": "2024-01-15T08:00:15Z", "level": "INFO", "source": "", "message": "Первое измерение получено"}\n',
        encoding="utf-8",
    )
    with pytest.raises(EmptySourceError):
        validation(parse_jsonl(test_jsonl))


def test_invalid_jsonl_skip_invalid(tmp_path):
    test_jsonl = tmp_path / "basic.jsonl"
    test_jsonl.write_text(
        '{"timestamp": "2024-01-15T08:00:01Z", "level": "blabla", "source": "sensor-01", "message": "Инициализация датчика завершена"}\n'
        '{"timestamp": "2024-13-15T08:00:15Z", "level": "INFO", "source": "sensor-01", "message": "Первое измерение получено"}\n'
        '{"timestamp": "2024-01-15T08:00:01Z", "level": "DEBUG", "source": "", "message": "Инициализация датчика завершена"}\n'
        '{"timestamp": "2024-01-15T08:00:01Z", "level": "INFO", "source": "sensor-01"}\n',
        encoding="utf-8",
    )
    assert len(validation_mode_skip_invalid(parse_jsonl(test_jsonl))[0]) == 0
    assert validation_mode_skip_invalid(parse_jsonl(test_jsonl))[1] == 4


def test_empty_jsonl(tmp_path):
    test_jsonl = tmp_path / "basic.jsonl"
    test_jsonl.write_text("", encoding="utf-8")
    assert len(list(parse_jsonl(test_jsonl))) == 0
