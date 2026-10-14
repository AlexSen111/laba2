def parse_csv(input_file: str) -> list:
    """Функция, которая принимает на вход строку csv-файла и разбивает её на отдельные поля

    Args:
        input_file (str): входная строка csv-файла

    Returns:
        list: отдельные поля, записаннные в список
    """
    input_fields: list = input_file.rstrip("\n").split(",")
    return input_fields
