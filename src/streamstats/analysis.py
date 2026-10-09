from datetime import datetime


def create_stats() -> dict:
    """ФУНКЦИЯ ДЛЯ СОХРАНЕНИЯ ЗНАЧЕНИЙ"""
    stats = {
        "total_events": 0,
        "count_level": {},
        "count_source": {},
        "error_source_count": {},
        "top_error_sources": [],
        "first_timestamp": "",
        "last_timestamp": "",
        "skipped": 0
        }
    return stats

def analyze_events(event: dict, stats: dict) -> dict:
    """ФУНКЦИЯ, ДЛЯ СОЗДАНИЯ ПЕРЕМЕННЫХ ДЛЯ REPORT"""

    # СЧЕТЧИК ДЛЯ ВСЕХ СОБЫТИЙ
    stats["total_events"] += 1
    time_event = datetime.fromisoformat(event["timestamp"])

    #СЧЕТЧИК ДЛЯ LEVEL
    if event["level"] in stats["count_level"]:
        stats["count_level"][event["level"]] += 1
    else: 
        stats["count_level"][event["level"]] = 1

    # СЧЕТЧИК ДЛЯ SOURCE
    if event["source"] in stats["count_source"]:
        stats["count_source"][event["source"]] += 1
    else:
        stats["count_source"][event["source"]] = 1
    
    # РАННЕЕ И ПОЗДНЕЕ ВРЕМЯ
    
    # ЕСЛИ НЕ БЫЛО НИКАКОГО ВРЕМЕНИ - СОЗДАЕМ 
    if stats["first_timestamp"] == "":
        stats["first_timestamp"] = time_event
    elif stats["first_timestamp"] >= time_event:
        # ДОБАВЛЯЕМ МИНИМАЛЬНОЕ ВРЕМЯ
        stats["first_timestamp"] = time_event

    if stats["last_timestamp"] == "":
        stats["last_timestamp"] = time_event
    elif stats["last_timestamp"] <= time_event:
        # ДОБАВЛЯЕМ МАКСИМАЛЬНОЕ ВРЕМЯ
        stats["last_timestamp"] = time_event
    
    # СОЗДАЕМ ТОП 5 ОШИБОК
    # ДОБАВЛЯЕМ ОШИБКИ И SOURCE К НИМ
    if event["level"] == "ERROR" or event["level"] == "CRITICAL":
        if event["source"] in stats["error_source_count"]:
            stats["error_source_count"][event["source"]] += 1
        else:
            stats["error_source_count"][event["source"]] = 1
    
    return stats

def final_stats(stats: dict) -> dict:
    """СОРТИРУЕТ TOP ОИШБОК И ОСТАВЛЯЕТ ТОЛЬКО 5"""
    stats["top_error_sources"] = sorted(stats["error_source_count"],
    key = lambda source: stats["error_source_count"][source], reverse = True)[:5]
    return stats