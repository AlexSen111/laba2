import json
import subprocess
import sys


def test_cli_valid_event(tmp_path):
    test_csv = tmp_path / "basic.csv"
    json_output = tmp_path / "test.json"
    test_csv.write_text(
        "timestamp,level,source,message\n"
        "2024-01-15T08:00:01Z,DEBUG,sensor-01,Инициализация датчика завершена\n"
        "2024-01-15T08:00:15Z,INFO,sensor-01,Первое измерение получено\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            "INPUT",
            str(test_csv),
            "--format",
            "csv",
            "--output",
            str(json_output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    report = json.loads(json_output.read_text(encoding="utf-8"))
    assert report[0]["Number of events"] == 2


def test_cli_invalid_event(tmp_path):
    test_csv = tmp_path / "basic.csv"
    json_output = tmp_path / "test.json"
    test_csv.write_text(
        "timestamp,level,source,message\n"
        "2024-01-15T08:00:01Z,blabla,sensor-01,Инициализация датчика завершена\n"
        "2024-01-15T08:00:15Z,INFO,sensor-01,Первое измерение получено\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            "INPUT",
            str(test_csv),
            "--format",
            "csv",
            "--output",
            str(json_output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert "Ошибка: неправильный уровень" in result.stderr


def test_cli_skip_invalid(tmp_path):
    test_csv = tmp_path / "basic.csv"
    json_output = tmp_path / "test.json"
    test_csv.write_text(
        "timestamp,level,source,message\n"
        "2024-01-15T08:00:01Z,blabla,sensor-01,Инициализация датчика завершена\n"
        "2024-01-15T08:00:01Z,DEBUG,sensor-01,Инициализация датчика завершена\n"
        "2024-13-15T08:00:15Z,INFO,sensor-01,Первое измерение получено\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            "INPUT",
            str(test_csv),
            "--format",
            "csv",
            "--skip-invalid",
            "--output",
            str(json_output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    report = json.loads(json_output.read_text(encoding="utf-8"))
    assert report[0]["Number of events"] == 1
    assert report[0]["WARNING: number of skipped strings"] == 2
