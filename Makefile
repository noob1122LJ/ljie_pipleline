.PHONY: check-python run-python run-r smoke-python test-python

check-python:
	python3 -m compileall python/src python/scripts python/tests

run-python:
	python3 python/scripts/run_python_pipeline.py --config configs/project.example.yaml

run-r:
	Rscript R/scripts/run_r_pipeline.R configs/project.example.yaml

smoke-python: check-python test-python run-python

test-python:
	PYTHONPATH=python/src python3 -m unittest discover -s python/tests -p 'test_*.py'
