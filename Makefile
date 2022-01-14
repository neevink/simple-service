PROJECT_NAME ?= simple-service
VERSION = $(shell python3 setup.py --version | tr '+' '-')

all:
	@echo "clean			- Очистить файлы, созданные distutils"
	@echo "sdist			- Создать исходник"
	@echo "devenv			- Пересоздать переменную окружения и заново установить зависимости"
	@echo "lint				- Запустить линковщик"
	@echo "test				- Запустить тесты"
	@exit 0

clean:
	sudo rm -fr *.egg-info dist

sdist: clean
	# официальный способ дистрибуции python-модулей
	python3 setup.py sdist

install-python:
	# устанавливаем python 3.9 и venv
	sudo apt-get install -y python3.9
	sudo apt-get install -y python3.9-venv

devenv: install-python clean
	sudo rm -rf venv
	# создаем новое окружение
	sudo python3.9 -m venv venv
	# обновляем pip
	sudo venv/bin/pip install -U pip
	# устанавливаем основные + dev зависимости из extras_require (см. setup.py)
	sudo venv/bin/pip install -Ue '.[dev]'

lint:
	venv/bin/pylama app/api/ app/tests/

test:
	venv/bin/pytest

.PHONY: clean sdist install-python devenv test
