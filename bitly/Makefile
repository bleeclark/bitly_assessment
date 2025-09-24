# Bitly Backend Engineer Coding Challenge - Makefile
#
# This Makefile provides convenient commands for running the click counter solution,
# running tests, and managing the development environment.

# Variables
PYTHON := python3
PIP := pip3
DOCKER_IMAGE := bitly-click-counter
DOCKER_CONTAINER := bitly-click-counter-container

# Default target
.DEFAULT_GOAL := help

# Help target - shows available commands
.PHONY: help
help:
	@echo "Bitly Backend Engineer Coding Challenge - Available Commands:"
	@echo ""
	@echo "  make run          - Run the click counter with sample data"
	@echo "  make test         - Run unit tests"
	@echo "  make test-verbose - Run unit tests with verbose output"
	@echo "  make clean        - Clean up temporary files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run application in Docker container"
	@echo "  make docker-test  - Run tests in Docker container"
	@echo "  make docker-clean - Remove Docker image and containers"
	@echo "  make validate     - Validate data files exist and are readable"
	@echo "  make install      - Install dependencies (none required)"
	@echo "  make help         - Show this help message"
	@echo ""

# Run the click counter application
.PHONY: run
run:
	@echo "Running Bitly Click Counter..."
	@echo "=============================="
	$(PYTHON) click_counter.py

# Run unit tests
.PHONY: test
test:
	@echo "Running Unit Tests..."
	@echo "===================="
	$(PYTHON) test_click_counter.py

# Run unit tests with verbose output
.PHONY: test-verbose
test-verbose:
	@echo "Running Unit Tests (Verbose)..."
	@echo "==============================="
	$(PYTHON) test_click_counter.py -v

# Validate that data files exist and are readable
.PHONY: validate
validate:
	@echo "Validating Data Files..."
	@echo "========================"
	@if [ -f "encodes.csv" ]; then \
		echo "✓ encodes.csv exists"; \
		head -1 encodes.csv | grep -q "long_url" && echo "✓ encodes.csv has correct header" || echo "✗ encodes.csv missing required header"; \
	else \
		echo "✗ encodes.csv not found"; \
	fi
	@if [ -f "decodes.json" ]; then \
		echo "✓ decodes.json exists"; \
		$(PYTHON) -c "import json; json.load(open('decodes.json'))" 2>/dev/null && echo "✓ decodes.json is valid JSON" || echo "✗ decodes.json is not valid JSON"; \
	else \
		echo "✗ decodes.json not found"; \
	fi

# Install dependencies (none required, but useful for documentation)
.PHONY: install
install:
	@echo "Installing Dependencies..."
	@echo "=========================="
	@echo "No external dependencies required!"
	@echo "This solution uses only Python standard library modules."
	@echo ""
	@echo "Required Python modules (built-in):"
	@echo "  - csv"
	@echo "  - json"
	@echo "  - logging"
	@echo "  - collections"
	@echo "  - datetime"
	@echo "  - typing"
	@echo "  - sys"
	@echo "  - os"
	@echo "  - unittest"
	@echo "  - tempfile"

# Clean up temporary files
.PHONY: clean
clean:
	@echo "Cleaning up temporary files..."
	@echo "=============================="
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type f -name "*.tmp" -delete
	@echo "Cleanup complete!"

# Docker commands
.PHONY: docker-build
docker-build:
	@echo "Building Docker Image..."
	@echo "========================"
	docker build -t $(DOCKER_IMAGE) .

.PHONY: docker-run
docker-run:
	@echo "Running in Docker Container..."
	@echo "=============================="
	docker run --rm -v $(PWD)/data:/app/data $(DOCKER_IMAGE)

.PHONY: docker-test
docker-test:
	@echo "Running Tests in Docker Container..."
	@echo "===================================="
	docker run --rm $(DOCKER_IMAGE) $(PYTHON) test_click_counter.py

.PHONY: docker-clean
docker-clean:
	@echo "Cleaning Docker Images and Containers..."
	@echo "========================================"
	docker rmi $(DOCKER_IMAGE) 2>/dev/null || echo "Docker image not found"
	docker container prune -f
	docker image prune -f

# Development commands
.PHONY: dev-setup
dev-setup: install validate
	@echo "Development Environment Setup Complete!"
	@echo "======================================"
	@echo "You can now run:"
	@echo "  make run          - Run the application"
	@echo "  make test         - Run tests"
	@echo "  make validate     - Check data files"

# Show Python version and environment info
.PHONY: info
info:
	@echo "Environment Information:"
	@echo "======================="
	@echo "Python version: $(shell $(PYTHON) --version)"
	@echo "Python executable: $(shell which $(PYTHON))"
	@echo "Working directory: $(PWD)"
	@echo "Files in directory:"
	@ls -la *.py *.csv *.json 2>/dev/null || echo "No Python/CSV/JSON files found"

# Full test suite with validation
.PHONY: full-test
full-test: validate test
	@echo "Full Test Suite Completed!"
	@echo "=========================="

# Quick development cycle
.PHONY: dev
dev: clean test run
	@echo "Development cycle complete!"

# Show file sizes and basic stats
.PHONY: stats
stats:
	@echo "Project Statistics:"
	@echo "=================="
	@echo "Python files:"
	@wc -l *.py
	@echo "Data files:"
	@wc -l *.csv *.json 2>/dev/null || echo "No data files found"
	@echo "Documentation files:"
	@wc -l *.md 2>/dev/null || echo "No documentation files found"
