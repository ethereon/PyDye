test:
	python -c "import tests; tests.run()"

install:
	python setup.py install
	$(MAKE) clean

clean:
	python setup.py clean --all
	rm -rf dist
	rm -rf *.egg-info
	find . -name '*.pyc' -delete