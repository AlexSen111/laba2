from parsers import parse_csv


def calculate_events(parsed_csv: list) -> list:
    events_count = len(parsed_csv)
    debug_count = len([i for i in parsed_csv if i[1] == "DEBUG"])
    info_count = len([i for i in parsed_csv if i[1] == "INFO"])
    warning_count = len([i for i in parsed_csv if i[1] == "WARNING"])
    error_count = len([i for i in parsed_csv if i[1] == "ERROR"])
    critical_count = len([i for i in parsed_csv if i[1] == "CRITICAL"])
    sources = sorted(list(set([i[2] for i in parsed_csv])))
    source_counts = [{source: len([i for i in parsed_csv if i[2] == source])} for source in sources]
    output = [events_count, debug_count, info_count, warning_count, error_count, critical_count, source_counts]
    return output


a = parse_csv(r"src\streamstats\test_input.csv")
print(calculate_events(a))

"""with open(r"src\streamstats\test_input.csv", encoding="utf-8") as csv_input:
    header = parse_csv(csv_input.readline())
    for event in csv_input:
        parsed_event = parse_csv(event)
        print(parsed_event)"""
