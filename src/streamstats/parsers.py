import csv
import json


def parse_csv(path: str) -> list[dict]:
    # csv_output = []
    """Функция, которая принимает на вход путь к csv-файлу и преобразует её в список словарей

    Args:
        path (str): путь к файлу

    Returns:
        list[dict]: список событий
    """
    with open(path, encoding="utf-8") as f:
        output = list(csv.DictReader(f))
        # header = f.readline().rstrip("\n").split(",")
        """for event in f:
            parsed_event = event.rstrip("\n").split(",")
            csv_output.append(parsed_event)"""

    return output


def parse_jsonl(path: str) -> list[dict]:
    """Функция, принимающая на вход путь к jsonl файлу и превращающая его в список словарей

    Args:
        path (str): путь к файлу

    Returns:
        list[dict]: список событий
    """
    jsonl_output: dict = []
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
