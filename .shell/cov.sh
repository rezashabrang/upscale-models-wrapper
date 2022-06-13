#!/bin/bash
find . -name 'coverage.txt' -delete
poetry run pytest --cov-report term --cov upscale_wrapper tests/ >>.logs/coverage.txt
