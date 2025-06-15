.PHONY: help install test lint format type-check clean

help: ## Show available commands
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install package in development mode
	@echo "🔧 Installing package..."
	hatch env create
	hatch run pip install -e .
	@echo "✅ Installation complete!"

test: ## Run tests
	@echo "🧪 Running tests..."
	hatch run test

lint: ## Lint code with ruff
	@echo "🔍 Linting code..."
	hatch run lint

format: ## Format code with ruff  
	@echo "🎨 Formatting code..."
	hatch run format

type-check: ## Type check with mypy
	@echo "🔍 Type checking..."
	hatch run type-check

clean: ## Clean build artifacts
	@echo "🧹 Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
