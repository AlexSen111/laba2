from datetime import datetime

from errors import EmptySourceError
from errors import WrongEventError
from errors import WrongLevelError
from errors import WrongTimeError


def correct_timestamp(time: str):
    try:
        datetime.fromisoformat(time)
        return True
    except (ValueError, TypeError):
        return False


def validation(parsed_csv: list):
    events_count = 0
    correct_level = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    for event in parsed_csv[1:]:
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

    # надо написать так, чтобы для каждой строки csv-файла валидация была отдельной, либо обрабатывать построчно
    # pass


def validation_mode_skip_invalid(parsed_csv: list):
    skipped_count = 0
    correct_level = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    for event in parsed_csv[1:]:
        if correct_timestamp(event[0]) and event[1] in correct_level and len(event[2]) > 0 and len(event) == 4:
            continue
        elif not correct_timestamp(event[0]):
            parsed_csv.remove(event)
            skipped_count += 1
        elif event[1] not in correct_level:
            parsed_csv.remove(event)
            skipped_count += 1
        elif len(event[2]) == 0:
            parsed_csv.remove(event)
            skipped_count += 1
        elif len(event) != 4:
            parsed_csv.remove(event)
            skipped_count += 1
    return parsed_csv, skipped_count


"""a = parse_csv(r"src\streamstats\test_input.csv")
for i in a:
    print(i)
print(validation(a))
print(validation_mode_skip_invalid(a)[1])"""
