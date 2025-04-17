# Makefile for running tests and code checks in the TA_log-analyzer project

# Variables
POETRY := poetry
PYTEST := $(POETRY) run pytest
FLAKE8 := $(POETRY) run flake8
SRC_DIR := src
TESTS_DIR := tests
COV_REPORT := html

# Default target: install dependencies, run lint and tests
.PHONY: all
all: install lint test

# Install dependencies using poetry
.PHONY: install
install:
	@echo "Installing dependencies..."
	$(POETRY) install

# Run flake8 to check code style
.PHONY: lint
lint:
	@echo "Running flake8 linting..."
	$(FLAKE8) $(SRC_DIR) $(TESTS_DIR) --max-line-length=120 --extend-ignore=E203

# Run tests with coverage report
.PHONY: test
test:
	@echo "Running tests with coverage..."
	$(PYTEST) --cov=$(SRC_DIR) --cov-report=$(COV_REPORT)

# Clean up generated files (e.g. coverage reports)
.PHONY: clean
clean:
	@echo "Cleaning up generated files..."
	rm -rf htmlcov .pytest_cache
