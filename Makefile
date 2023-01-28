SHELL := /bin/bash

.PHONY: help format test
.DEFAULT: help

help:
	@echo "Usage: make <target>"
	@echo
	@echo "Available targets:"
	@echo "  help: Show this help"
	@echo "  format: Run type checking and code styling inplace"
	@echo "  test: Run all tests"

format:
	isort .
	black .
	ruff .
	mypy .

test:
	pytest -n auto
