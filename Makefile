PYPI_USER=thingwala

# setup:
# 	pip install -r requirements.txt
# 	pip install -r requirements.dev.txt
# 	pip install -r requirements.test.txt
# 	pre-commit install

# check:
# 	flake8 ./thingwala/geyserwala/connect --ignore E501
# 	find ./thingwala/geyserwala/connect -name '*.py' \
# 	| xargs pylint -d invalid-name \
# 	               -d missing-docstring \
# 	               -d line-too-long \

# style:
# 	black ./thingwala/geyserwala/connect

# test:
# 	pytest ./tests/ -vvv \
# 		--junitxml=./reports/unittest-results.xml \
# 		--cov=./thingwala/geyserwala/connect --cov-report=html:reports

# coverage:
# 	open reports/index.html

to_pypi:
	pip install build twine

to_pypi_test: test
	python -m build
	TWINE_USERNAME=${PYPI_USER} twine upload -r testpypi dist/thingwala_geyserwala-$(shell cat ./version)*

to_pypi_live: test
	python -m build
	TWINE_USERNAME=${PYPI_USER} twine upload -r pypi dist/thingwala_geyserwala-$(shell cat ./version)*
