def calculate_events(parsed_csv: list) -> list:
    """Функция, получающая на вход отпарсенный csv-файл и обраюатывающая его для дальнейшего формирования json-отчёта

    Args:
        parsed_csv (list): Отпарсенный csv-файл

    Returns:
        list: Список, содержащий данные для дальнейшего формирования json-отчёта
    """
    parsed_csv: list = parsed_csv[1:]  # избавляемся от заголовка
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
    min_time: list = min([i for i in parsed_csv])
    max_time: list = max([i for i in parsed_csv])
    output: list = [
        events_count,
        debug_count,
        info_count,
        warning_count,
        error_count,
        critical_count,
        source_counts,
        error_counts,
        min_time,
        max_time,
    ]
    return output


"""a = parse_csv(r"src\streamstats\test_input.csv")
b = calculate_events(a)
c = b[-3]
print(dict(sorted(c.items(), key = lambda x: x[1], reverse=True)[:5]))
print(b)"""
