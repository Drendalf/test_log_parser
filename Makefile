include dev.env
export


venv:
	python3.12 -m venv venv
	./venv/bin/pip3 -q install --upgrade pip wheel
	./venv/bin/pip3 install -q -r ./src/requirements.txt

format: venv
	# Run checking and formatting sources.
	./venv/bin/bandit -q -r src/
	./venv/bin/pre-commit run -a

test: external
	# Build test image.
	docker build -q -t $(TEST_TAG) -f ./test.Dockerfile .
	# Run tests in container.
	docker compose -f test.compose.yml up --abort-on-container-exit --quiet-pull
	make stop

run: external
	# Run app in container.
	docker compose -f dev.compose.yml up --abort-on-container-exit
	make stop

all: test run
