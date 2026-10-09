class StreamStatsError(Exception):
    """ОШИБКА ПРИ ВВОДЕ В CLI"""

class UnsupportedFormatError(StreamStatsError):
    """ОШИБКА НЕПОДДЕРЖИМОГО ФОРМАТА"""

class MissingFieldError(StreamStatsError):
    """ОШИБКА ОТСУСТВИЯ В ЛОГЕ ОДНОГО ИЗ ЗНАЕЧЕНИЙ"""

class InvalidEventError(StreamStatsError):
    """ОШИБКА ПРИ НЕ ВЕРНОМ ВВЕДЕНИИ В LEVEL"""

class InvalidTimestampError(StreamStatsError):
    """ОШИБКА ПРИ НЕВЕРНОМ ФОРМАТЕ ВРЕМЕНИ"""

class InvalidJSONError(StreamStatsError):
    """ОШИБКА JSON"""

class InputFileError(StreamStatsError):
    """ОШИБКА ЕСЛИ ФАЙЛА НЕТУ"""