from datetime import datetime

from .errors import InvalidEventError, InvalidTimestampError, MissingFieldError


def validate_event(event: dict) -> None:
    """ПРОВЕРКА СУЩЕСТВОВАНИЕ СТРОК"""
    if not isinstance(event, dict):
        raise InvalidEventError(
            "Событие должно быть JSON-объектом"
        )

    required_fields = {"timestamp", "level", "source", "message"}
    level_variables = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    missing_variables = required_fields - event.keys()

    if missing_variables:
        raise MissingFieldError(
            f"отсутствия поля {missing_variables}"
        )


    if not isinstance(event["level"], str):
        raise InvalidEventError(
            f"значение level {event['level']} не строка"
        )
    
    if event["level"] not in level_variables:
        raise InvalidEventError(
            f"некорректный уровень {event['level']}"
        )

    if not isinstance(event["timestamp"], str):
        raise InvalidTimestampError(
            f"значение timestamp {event['timestamp']} не строка"
        )

    try:
        datetime.fromisoformat(event["timestamp"])
    except ValueError:
        raise InvalidTimestampError(
            f"некорректный timestamp {event['timestamp']}"
        )
    
    
    if not isinstance(event["source"], str):
        raise InvalidEventError(
            f"значение source {event['source']} не строка"
        )
    if event["source"].strip() == "":
        raise InvalidEventError(
            "пустое значение source"
        )

    if not isinstance(event["message"], str):
        raise InvalidEventError(
            f"значение message {event['message']} не строка"
        )