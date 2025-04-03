# LOG_ANALYZER
Парсер логов, с дальнейшим формированием отчета в html-файл. Работает как с raw-файлами, так и с .gz-архивами
## Pre-requisities:
1) установить зависимости в окружение (./requirements.txt / pyproject.toml)
2) доступна настройка для:
- __report_template_path__ - путь до шаблона (default: "./report.html")
- __report_size__ - количество URL'ов в отчете (default: "1000")
- __report_dir__ - директория для отчетов (default: "./REPORT_DIR")
- __log_dir__ - директория для логов (default: "./LOG_DIR")
- __app_log_path__ (опционально) - файл для записи логов приложения (default: stdout)
- __./default_config.ini__ - конфиг файл по умолчанию. Возможно изменение стандартных параметров через внешний файл (__--config $ВНЕШНИЙ_ФАЙЛ__ как аргумент запуска)
3) Нейминг необходимых лог-файлов и формат обрабатываемых логов управляются через __FILE_NAME_REGEX/LOG_LINE_REGEX__ в src/app/log_stuff.py
## Getting started:
- запустить
> python3 log_analyzer.py (--config $PATH_TO_EXTERNAL_CONFIG)
- подождать
- забрать готовый отчет в __$report_dir__
### Stack:
1. Python 3.9+
2. Structlog
3. Pytest
### Contributors:
Mustafin A.: pupenkinvas@yandex.ru