from datetime import datetime

# from .parsers import parse_csv
from .errors import EmptySourceError
from .errors import WrongEventError
from .errors import WrongLevelError
from .errors import WrongTimeError


def correct_timestamp(time: str) -> bool:
    """Функция, проверяющая временную метку на соответствие стандарту

    Args:
        time (str): временная метка

    Returns:
        bool: соответствие стандарту
    """
    try:
        datetime.fromisoformat(time)
        return True
    except (ValueError, TypeError):
        return False


def validation(parsed_file: list[dict]):
    """Функция, проверяющая валидность входных данных

    Args:
        parsed_file (list[dict]): отпарсенный файл

    Raises:
        WrongTimeError: неправильная временная метка
        WrongLevelError: неправильный уровень
        EmptySourceError: пустой источник
        WrongEventError: нехватка поля
    """
    events_count: int = 0
    correct_level: list = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    for line in parsed_file:
        event: list = list(line.values())
        event: list = [i for i in event if i is not None]
        events_count += 1
        if correct_timestamp(event[0]) and event[1] in correct_level and len(event[2]) > 0 and len(event) == 4:
            continue
        elif not correct_timestamp(event[0]):
            raise WrongTimeError(f"Ошибка: время не в ISO 8601 в строке {events_count}")
        elif event[1] not in correct_level:
            raise WrongLevelError(f"Ошибка: неправильный уровень {event[1]} события в строке {events_count}")
        elif len(event[2]) == 0:
            raise EmptySourceError(f"Ошибка: пустой источник события в строке {events_count}")
        elif len(event) != 4:
            raise WrongEventError(
                f"Ошибка: в строке {events_count} событие состоит из {len(event)} полей, а должно состоять из 4"
            )


def validation_mode_skip_invalid(parsed_file: list[dict]):
    output = []
    # parsed_file = [list(i.values()) for i in parsed_file]
    skipped_count = 0
    correct_level = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    for line in parsed_file:
        # print(line)
        event = list(line.values())
        event = [i for i in event if i is not None]
        # print(event)
        if correct_timestamp(event[0]) and event[1] in correct_level and len(event[2]) > 0 and len(event) == 4:
            output.append(line)
        if len(event[2]) == 0:
            # print(True, event)
            # parsed_file.remove(event)
            skipped_count += 1
        if len(event) != 4:
            # print(True, event)
            # parsed_file.remove(event)
            skipped_count += 1
        if not correct_timestamp(event[0]):
            # print(True, event)
            # parsed_file.remove(event)
            skipped_count += 1
        if event[1] not in correct_level:
            # print(True, event)
            # parsed_file.remove(event)
            skipped_count += 1
    return output, skipped_count


# a = parse_csv(r"src\streamstats\test_input.csv")
"""for i in a:
    print(i)"""
# print(validation(a))
# print(a)
# print(validation_mode_skip_invalid(a))
