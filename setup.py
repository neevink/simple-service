from setuptools import setup, find_packages

setup(
    name='simple-service',
    author='Kirill Neevin',
    author_email='neevin-kirill@mail.ru',
    description='My first simple service on Python',
    packages=find_packages(exclude=['tests']),
    version='0.0.1',
    install_requires=['aiohttp'],
)
