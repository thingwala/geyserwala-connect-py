from setuptools import setup, find_namespace_packages

setup(
    name='thingwala-geyserwala-connect',
    description="Python bindings to the Geyserwala Connect REST API",
    author="Thingwala",
    url="https://github.com/thingwala/geyserwala-connect-py",
    license="MIT",
    packages=find_namespace_packages(include=['thingwala.geyserwala.connect']),
    version=open('version', 'rt', encoding="utf8").read().strip(),
    install_requires=open('requirements.txt', encoding="utf8").readlines(),
    tests_require=open('requirements_dev.txt', encoding="utf8").readlines(),
    entry_points={
        "console_scripts": [
            "geyserwala-connect=thingwala.geyserwala.connect.aio.cli:cli",
        ]
    },
)
