import csv
import json


def parse_csv(path: str) -> dict:
    # csv_output = []
    """Функция, которая принимает на вход строку csv-файла и разбивает её на отдельные поля

    Args:
        input_file (str): входная строка csv-файла

    Returns:
        list: отдельные поля, записаннные в список
    """
    with open(path, encoding="utf-8") as f:
        output = list(csv.DictReader(f))
        # header = f.readline().rstrip("\n").split(",")
        """for event in f:
            parsed_event = event.rstrip("\n").split(",")
            csv_output.append(parsed_event)"""

    return output


def parse_jsonl(path: str) -> list:
    jsonl_output = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            event: dict = json.loads(line)
            jsonl_output.append(event)
    return jsonl_output


# a = r"src\streamstats\test_input.csv"
# b = r"src\streamstats\test_input.jsonl"
# print(parse_csv(a))
# print(parse_jsonl(b))
