import csv
import json
from collections.abc import Iterator
from pathlib import Path

from .errors import InputFileError, InvalidJSONError, StreamStatsError
from .models import validate_event


def read_jsonl(path: Path, skip_invalid: bool, stats: dict) -> Iterator[dict]:
    """ЧТЕНИЕ JSONL"""
    # ЛОВИМ ОШИБКУ ОТСУТВИЯ ФАЙЛА
    try:
        with path.open("r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start = 1):
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    error = InvalidJSONError(
                        f"Некорректный JSON: {path}, строка {line_num}"
                    )

                    if skip_invalid:
                        print(f"WARNING: {error}")
                        stats["skipped"] += 1
                        continue

                    raise error
#ОШИБКИ ИЗ VALIDATE ВЫВОЯДТСЯ С ИМЕНЕМ ФАЙЛА И СТРОКОЙ
                try: 
                    validate_event(event)
                except StreamStatsError as error:
                    
                    if skip_invalid:
                        print(f"WARNING: {error}")
                        stats["skipped"] += 1
                        continue
                    else:
                        raise type(error)(
                            f"{path}, строка {line_num}: {error}"
                        ) from error
                yield event
    except FileNotFoundError as error:
        raise InputFileError(
            f"Входной файл не найден: {path}"
        ) from error

def read_csv(path: Path, skip_invalid: bool, stats: dict) -> Iterator[dict]:
    try:
        with path.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for event in reader:
                line_num = reader.line_num
                try:
                    validate_event(event)
                except StreamStatsError as error:
                    if skip_invalid:
                        print(f"WARNING: {error}")
                        stats["skipped"] += 1
                        continue        
                    else:
                        raise type(error)(
                            f"{path}, строка {line_num}: {error}"
                        ) from error
                yield event
    except FileNotFoundError as error:
        raise InputFileError(
            f"Входной файл не найден: {path}"
        ) from error