PROJECT_NAME ?= simple-service
VERSION = $(shell python3 setup.py --version | tr '+' '-')

all:
	@echo "clean			- Очистить файлы, созданные distutils"
	@echo "database         - Поднять базу данных и adminer к ней"
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
	# устанавливаем python 3.8 и venv
	sudo apt-get install -y python3.8
	sudo apt-get install -y python3.8-venv

devenv: install-python clean
	sudo rm -rf venv
	# создаем новое окружение
	sudo python3.8 -m venv venv
	# обновляем pip
	sudo venv/bin/pip install -U pip
	# устанавливаем основные + dev зависимости из extras_require (см. setup.py)
	sudo venv/bin/pip install -Ue '.[dev]'

lint:
	venv/bin/pylama app/api/ app/tests/

test:
	venv/bin/pytest

database:
	sudo docker-compose up

.PHONY: clean sdist install-python devenv test
