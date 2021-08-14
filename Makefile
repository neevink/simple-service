PROJECT_NAME ?= simple-service
VERSION = $(shell python3 setup.py --version | tr '+' '-')

all:
	@echo "devenv			- Пересоздать переменную окружения и заново установить зависимости"
	@echo "lint				- Запустить линковщик"
	@echo "clean			- Очистить файлы, созданные distutils"
	@exit 0

clean:
	rm -fr *.egg-info dist

devenv:
	rm -rf venv
	# создаем новое окружение
	python3.9 -m venv venv
	# обновляем pip
	venv/bin/pip install -U pip
	# устанавливаем основные + dev зависимости из extras_require (см. setup.py)
	venv/bin/pip install -Ue '.[dev]'

lint:
	venv/bin/pylama api/ tests/

test:
	venv/bin/pytest
