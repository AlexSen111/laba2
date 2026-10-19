# from parsers import parse_csv
# from models import validation_mode_skip_invalid
def calculate_events(parsed_csv: list[dict]) -> dict:
    """Функция, получающая на вход отпарсенный csv-файл и обраюатывающая его для дальнейшего формирования json-отчёта

    Args:
        parsed_csv (list): Отпарсенный csv-файл

    Returns:
        list: Список, содержащий данные для дальнейшего формирования json-отчёта
    """
    parsed_csv: list = [list(event.values()) for event in parsed_csv]  # избавляемся от заголовка
    events_count: int = len(parsed_csv)
    debug_count: int = len([i for i in parsed_csv if i[1] == "DEBUG"])
    info_count: int = len([i for i in parsed_csv if i[1] == "INFO"])
    warning_count: int = len([i for i in parsed_csv if i[1] == "WARNING"])
    error_count: int = len([i for i in parsed_csv if i[1] == "ERROR"])
    critical_count: int = len([i for i in parsed_csv if i[1] == "CRITICAL"])
    sources: list = sorted(list(set([i[2] for i in parsed_csv])))
    source_counts: dict = [{source: len([i for i in parsed_csv if i[2] == source]) for source in sources}][0]
    error_counts: dict = [
        {
            source: len([i for i in parsed_csv if i[2] == source and (i[1] == "ERROR" or i[1] == "CRITICAL")])
            for source in sources
        }
    ][0]
    top5_errors: dict = dict(sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5])
    min_time: list = min([i for i in parsed_csv])
    max_time: list = max([i for i in parsed_csv])
    output: dict = {
        "Number of events": events_count,
        "Number of debug events": debug_count,
        "Number of info events": info_count,
        "Number of warnings": warning_count,
        "Number of errors": error_count,
        "Number of critical errors": critical_count,
        "Sources": source_counts,
        "Top 5 error sources": top5_errors,
        "First timestamp": min_time,
        "Last timestamp": max_time,
    }
    return output


"""a = parse_csv(r"src\streamstats\test_input.csv")
b = calculate_events(a)
c = b[-3]
print(dict(sorted(c.items(), key = lambda x: x[1], reverse=True)[:5]))
print(b)"""
