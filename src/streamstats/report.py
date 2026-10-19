import json

from .analysis import calculate_events
from .models import validation_mode_skip_invalid


def create_report(data, report):
    with open(report, "w", encoding="utf-8") as file:
        if len(data) > len(validation_mode_skip_invalid(data)[0]):
            json.dump(
                calculate_events(validation_mode_skip_invalid(data)[0])
                | {"WARNING: number of skipped strings": validation_mode_skip_invalid(data)[1]},
                file,
                ensure_ascii=False,
                indent=4,
            )
        else:
            json.dump(calculate_events(data), file, ensure_ascii=False, indent=4)


"""a = r"src\streamstats\test_input.csv"
create_report_csv(a, "test_report.json")
b = r"src\streamstats\test_input.jsonl"
create_report_jsonl(b, "test_report.json")"""
