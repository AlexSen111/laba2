# ЛР №2. Streamstats

Выполнил Сенаторов Алексей, М8О-103БВ-26
# Использование
Команды для использования:

python -m streamstats analyze INPUT "path-to-file" --format csv|jsonl --output "output-file.json"
python -m streamstats analyze INPUT "path-to-file" --format csv|jsonl --skip-invalid --output "output-file.json"

Если не следовать этим командам, пакет не заработает

# Зависимости
Пакет использует библиотеку pytest. Необходимо её скачать с помощью pip install pytest
# Входные данные
Входные данные должны соответстовать образцу:
timestamp: ISO 8601

level: DEBUG | INFO | WARNING | ERROR | CRITICAL

source: непустая строка

message: строка
# Обработка ошибок
В случае ошибки программа выведет сообщение в stderr и завершится с кодом 2