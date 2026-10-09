import argparse
import sys
from pathlib import Path

from .analysis import analyze_events, create_stats, final_stats
from .errors import StreamStatsError, UnsupportedFormatError
from .parser import read_csv, read_jsonl
from .report import write_report


def main() -> int:
    """CLI И ЗАПУСК ЧТЕНИЙ ФАЙЛОВ"""
    parser = argparse.ArgumentParser(
            prog="streamstats",
        description=(
            "StreamStats — анализатор событий из CSV и JSONL-файлов. "
            "Подсчитывает статистику по уровням логирования и источникам."
        ),
        epilog=(
            "Примеры:\n"
            "  python -m streamstats analyze events.jsonl "
            "--format jsonl --output report.json\n"
            "  python -m streamstats analyze first.csv second.csv "
            "--format csv --output report.json\n"
            "  python -m streamstats analyze events.jsonl "
            "--format jsonl --output report.json --skip-invalid"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparser = parser.add_subparsers(dest="command",
    title="Команды",
    metavar="COMMAND",
    required=True)

    analyze_parser = subparser.add_parser("analyze",     
        help="Анализировать события из файлов CSV или JSONL",
        description=(
            "Читает один или несколько файлов с событиями, "
            "подсчитывает статистику и сохраняет отчёт в JSON."
        ),
    )
    analyze_parser.add_argument("inputs", nargs="+")
    analyze_parser.add_argument("--format", required=True)
    analyze_parser.add_argument("--output", required=True)
    analyze_parser.add_argument("--skip-invalid", action="store_true")

    args = parser.parse_args()
    stats = create_stats()

    if args.command == "analyze":
        if args.format == "csv":

            # ФУНКЦИЯ ДЛЯ РАБОТЫ С CSV
            for i in args.inputs:
                events = read_csv(Path(i),
                skip_invalid = args.skip_invalid, 
                stats = stats)    
                
                for event in events:
                    analyze_events(event, stats)

        elif args.format == "jsonl":
            # ФУНКЦИЯ ДЛЯ JSONL
            for i in args.inputs:
                events = read_jsonl(Path(i),
                skip_invalid = args.skip_invalid,
                stats = stats)
                
                for event in events:
                    analyze_events(event, stats)
        else:
            raise UnsupportedFormatError(
                f"Неподдерживаемый формат: {args.format}"
            )
        stats_final = final_stats(stats)
        write_report(stats_final, Path(args.output))
    return 0
if __name__ == "__main__":
    try:
        sys.exit(main())
    except StreamStatsError as error:
        print(f"Ошибка: {error}")
        sys.exit(2)