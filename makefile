all: compile test checkstyle

compile:
	python3 -m py_compile ultrastar_table/*.py

test:
	python3 -m unittest discover -s tests

checkstyle:
	flake8 ultrastar_table/*.py
	flake8 tests/*.py

clean:
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf ultrastar_table/__pycache__
	rm -f *.pyc
