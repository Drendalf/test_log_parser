
venv:
	python3.12 -m venv venv
	./venv/bin/pip3 -q install --upgrade pip wheel
	./venv/bin/pip3 install -q -r ./src/requirements.txt

format:
	# Run checking and formatting sources.
	./venv/bin/bandit -q -r src/
	./venv/bin/pre-commit run -a
