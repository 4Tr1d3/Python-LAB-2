import json
from pathlib import Path

from .errors import InputFileError


def write_report(stats: dict, output_path: Path) -> None:
    final_stats = stats.copy()

    # ПЕЕРВОДИМ ИЗ ВРЕМЕНИ В СТРОКУ, ИСКЛЮЧАЕМ СТРОКИ БЕЗ ВРЕМЕНИ
    if final_stats["first_timestamp"] != "":
        final_stats["first_timestamp"] = final_stats["first_timestamp"].isoformat()
    if final_stats["last_timestamp"] != "":
        final_stats["last_timestamp"] = final_stats["last_timestamp"].isoformat()
    
    
    try:
        with output_path.open("w", encoding = "utf-8") as file:
            json.dump(final_stats, file, ensure_ascii = False, indent = 4)
        # ПЕРЕДАЕМ ЗНАЧЕНИЯ, ФАЙЛ ДЛЯ ЗАПИСИ, РАЗРЕШАЕМ РУССКИЙ ТЕКСТ И ДЕЛАЕМ ТАБУЛЯЦИЮ
    except OSError as error:
        raise InputFileError(
            f"Не удалось записать отчёт в файл {output_path}: {error}"
        ) from error