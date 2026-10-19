import sys

from .errors import EmptySourceError
from .errors import WrongEventError
from .errors import WrongLevelError
from .errors import WrongTimeError
from .models import validation

# from .analysis import calculate_events
from .parsers import parse_csv
from .parsers import parse_jsonl
from .report import create_report


def main():
    if len(sys.argv) < 8:
        print("Ошибка: недостаточно входных данных", file=sys.stderr)
        sys.exit(2)
    command = sys.argv[1].lower()
    if command == "analyze":
        path = sys.argv[3]
        format = sys.argv[5]
        if sys.argv[2].upper() == "INPUT":
            if sys.argv[4] == "--format":
                if format == "jsonl" and path[-5:] == "jsonl":
                    parsed_file = parse_jsonl(path)
                    if sys.argv[6] == "--skip-invalid":
                        output = sys.argv[8]
                        create_report(parsed_file, output)
                    elif sys.argv[6] == "--output":
                        output = sys.argv[7]
                        try:
                            validation(parsed_file)
                            create_report(parsed_file, output)
                        except WrongTimeError as e:
                            print(f"{e}", file=sys.stderr)
                            sys.exit(2)
                        except WrongLevelError as e:
                            print(f"{e}", file=sys.stderr)
                            sys.exit(2)
                        except EmptySourceError as e:
                            print(f"{e}", file=sys.stderr)
                            sys.exit(2)
                        except WrongEventError as e:
                            print(f"{e}", file=sys.stderr)
                            sys.exit(2)
                    else:
                        print(
                            f"Ошибка: неизвестная команда {sys.argv[6]}, должно быть '--output' или '--skip-invalid'",
                            file=sys.stderr,
                        )
                        sys.exit(2)
                elif format == "csv" and path[-3:] == "csv":
                    parsed_file = parse_csv(path)
                    if sys.argv[6] == "--skip-invalid":
                        output = sys.argv[8]
                        create_report(parsed_file, output)
                    elif sys.argv[6] == "--output":
                        output = sys.argv[7]
                        try:
                            validation(parsed_file)
                            create_report(parsed_file, output)
                        except WrongTimeError as e:
                            print(f"{e}", file=sys.stderr)
                            sys.exit(2)
                        except WrongLevelError as e:
                            print(f"{e}", file=sys.stderr)
                            sys.exit(2)
                        except EmptySourceError as e:
                            print(f"{e}", file=sys.stderr)
                            sys.exit(2)
                        except WrongEventError as e:
                            print(f"{e}", file=sys.stderr)
                            sys.exit(2)
                else:
                    print(
                        f"Ошибка: неподдерживаемый формат файла или несоотвествие формата {path} с форматом {format}",
                        file=sys.stderr,
                    )
                    sys.exit(2)
            else:
                print(f"Ошибка: неизвестная команда {sys.argv[4]} вместо '--format'", file=sys.stderr)
                sys.exit(2)
        else:
            print(f"Ошибка: неизвестная команда {sys.argv[2]} вместо 'INPUT'", file=sys.stderr)
            sys.exit(2)
    else:
        print(f"Ошибка: неизвестная команда {command} вместо 'analyze'", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
