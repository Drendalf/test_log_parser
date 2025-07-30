import subprocess

import pytest


@pytest.mark.parametrize(
    "params",
    [
        {
            "good_params": ["file", "report", "date"],
            "bad_params": ["fileZ", "reportZ", "dateZ"],
        }
    ],
)
def test_params(params):
    report = subprocess.run(
        [
            "python",
            "../src/main.py",
            f"--{params['good_params'][0]}",
            "./logs/example1.log",
            f"--{params['good_params'][1]}",
            "average",
            f"--{params['good_params'][2]}",
            "2025-06-22",
        ]
    )
    assert report.returncode == 0
    report = subprocess.run(
        [
            "python",
            "../src/main.py",
            f"--{params['bad_params'][0]}",
            "./logs/example1.log",
            f"--{params['bad_params'][0]}",
            "average",
            f"--{params['bad_params'][0]}",
            "2025-06-22",
        ]
    )
    assert report.returncode != 0


@pytest.mark.parametrize(
    "arguments",
    [
        {
            "good_arguments": ["./logs/example1.log", "average", "2025-06-22"],
            "bad_arguments": ["fileZ", "reportZ", "dateZ"],
        }
    ],
)
def test_arguments(arguments, caplog):
    report = subprocess.run(
        [
            "python",
            "../src/main.py",
            "--file",
            f"{arguments['good_arguments'][0]}",
            "--report",
            f"{arguments['good_arguments'][1]}",
            "--date",
            f"{arguments['good_arguments'][2]}",
        ]
    )
    assert report.returncode == 0

    report = subprocess.run(
        [
            "python",
            "../src/main.py",
            "--file",
            f"{arguments['bad_arguments'][0]}",
            "--report",
            f"{arguments['bad_arguments'][1]}",
            "--date",
            f"{arguments['bad_arguments'][2]}",
        ]
    )
    assert report.returncode != 0
