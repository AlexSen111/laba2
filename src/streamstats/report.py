import json
import os

from streamstats.analysis import calculate_events
from streamstats.models import validation_mode_skip_invalid

# from streamstats.parsers import parse_csv, parse_jsonl


def create_report(data, report):
    if os.path.exists(report) and os.path.getsize(report) > 0:
        with open(report, "r", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    result = validation_mode_skip_invalid(data)
    if len(data) > len(result[0]):
        current_report = calculate_events(result[0])
        current_report["WARNING: number of skipped strings"] = result[1]
    else:
        current_report = calculate_events(data)
    existing_data.append(current_report)
    with open(report, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)


"""a = parse_csv(r"src\streamstats\test_input.csv")
create_report(a, "test_report.json")
b = parse_jsonl(r"src\streamstats\test_input.jsonl")
create_report(b, "test_report.json")"""
