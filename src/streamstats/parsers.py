def parse_csv(path: str) -> list:
    csv_output = []
    """Функция, которая принимает на вход строку csv-файла и разбивает её на отдельные поля

    Args:
        input_file (str): входная строка csv-файла

    Returns:
        list: отдельные поля, записаннные в список
    """
    with open(path, encoding="utf-8") as f:
        # header = f.readline().rstrip("\n").split(",")
        for event in f:
            parsed_event = event.rstrip("\n").split(",")
            csv_output.append(parsed_event)

    return csv_output
