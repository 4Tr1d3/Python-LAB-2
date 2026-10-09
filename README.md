# StreamStats

StreamStats — консольная утилита для потокового анализа событий из файлов CSV и JSONL. Программа обрабатывает данные построчно, собирает статистику и сохраняет результат в формате JSON.

## Возможности

- Обработка файлов CSV и JSONL.
- Анализ одного или нескольких входных файлов за один запуск.
- Подсчёт общего количества событий.
- Подсчёт событий по уровням логирования.
- Подсчёт событий по источникам.
- Поиск пяти источников с наибольшим количеством событий уровней ERROR и CRITICAL.
- Определение времени первого и последнего события.
- Пропуск некорректных записей с помощью параметра `--skip-invalid`.
- Сохранение отчёта в JSON.
- Вывод справки по командам через `--help`.

## Установка

Клонируйте репозиторий или скачайте исходный код проекта. Перейдите в каталог проекта и установите его вместе с инструментами разработки:

```bash
python -m pip install -e ".[dev]"
```

## Использование

Общий список доступных команд:

```bash
python -m streamstats --help
```

Справка по анализу файлов:

```bash
python -m streamstats analyze --help
```

### Анализ JSONL-файла

```bash
python -m streamstats analyze events.jsonl --format jsonl --output report.json
```

### Анализ CSV-файла

```bash
python -m streamstats analyze events.csv --format csv --output report.json
```

### Анализ нескольких файлов

```bash
python -m streamstats analyze first.jsonl second.jsonl --format jsonl --output report.json
```

### Пропуск некорректных записей

```bash
python -m streamstats analyze events.jsonl --format jsonl --output report.json --skip-invalid
```

Без параметра `--skip-invalid` некорректная запись приводит к ошибке обработки. При использовании этого параметра программа предупреждает о некорректной записи, пропускает её и продолжает анализ.

## Формат входных данных

Каждое событие должно содержать следующие поля:

| Поле | Описание |
|---|---|
| `timestamp` | Дата и время события в формате ISO 8601 |
| `level` | Уровень логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR` или `CRITICAL` |
| `source` | Непустая строка с названием источника |
| `message` | Текст сообщения |

### Пример JSONL

Каждая строка содержит отдельный JSON-объект:

```json
{"timestamp":"2026-10-08T10:00:00","level":"INFO","source":"auth","message":"User logged in"}
{"timestamp":"2026-10-08T10:05:00","level":"ERROR","source":"database","message":"Connection failed"}
{"timestamp":"2026-10-08T10:10:00","level":"WARNING","source":"api","message":"Slow response"}
```

### Пример CSV

```csv
timestamp,level,source,message
2026-10-08T10:00:00,INFO,auth,User logged in
2026-10-08T10:05:00,ERROR,database,Connection failed
2026-10-08T10:10:00,WARNING,api,Slow response
```

## Формат отчёта

Программа сохраняет статистику в указанный JSON-файл. Отчёт включает общее количество обработанных событий, распределение по уровням логирования и источникам, список источников с наибольшим количеством ошибок, временные границы событий и количество пропущенных записей.

Точная структура отчёта определяется реализацией программы.

## Тестирование

Запуск всех тестов:

```bash
python -m pytest
```

Проверка кода с помощью Ruff:

```bash
ruff check .
```

## Структура проекта

```text
LAB 2/
├── src/
│   └── streamstats/
│       ├── __init__.py
│       ├── __main__.py
│       ├── models.py
│       ├── parser.py
│       ├── analysis.py
│       ├── report.py
│       └── errors.py
├── tests/
├── pyproject.toml
└── README.md
```

## Обработка ошибок

При обнаружении некорректных данных или другой ошибки программа выводит диагностическое сообщение. Для ошибок обработки входных данных предусмотрен код завершения `2`.