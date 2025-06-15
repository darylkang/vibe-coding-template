.PHONY: install dev-install test test-cov coverage lint lint-fix format format-check type-check run run-example clean notebook build publish pre-commit ci help all

# Default target
all: install lint format type-check test ## Install, lint, format, type-check, and test

install: ## Install package in development mode
	@echo "🔧 Installing package in development mode..."
	hatch env create
	@echo "✅ Installation complete! Run 'hatch shell' to activate."

dev-install: ## Install with all development dependencies  
	@echo "🔧 Installing with development dependencies..."
	hatch env create
	hatch run pip install -e ".[dev,jupyter]"

test: ## Run tests with pytest
	@echo "🧪 Running tests..."
	hatch run test

test-cov: ## Run tests with coverage
	@echo "🧪 Running tests with coverage..."
	hatch run test-cov

coverage: ## Generate coverage reports
	@echo "📊 Generating coverage report..."
	hatch run cov-report
	hatch run cov-html
	@echo "📊 Coverage report generated! Open htmlcov/index.html to view."

lint: ## Lint code with ruff
	@echo "🔍 Linting code with ruff..."
	hatch run lint

lint-fix: ## Lint and fix code with ruff
	@echo "🔧 Linting and fixing code with ruff..."
	hatch run lint-fix

format: ## Format code with ruff
	@echo "🎨 Formatting code with ruff..."
	hatch run format

format-check: ## Check code formatting without making changes
	@echo "🎨 Checking code formatting..."
	hatch run format-check

type-check: ## Type check with mypy
	@echo "🔍 Type checking with mypy..."
	hatch run type-check

run: ## Run the CLI application (example)
	@echo "🚀 Running application..."
	hatch run python -m my_package.cli --help

run-example: ## Run example CLI command
	@echo "🚀 Running example CLI command..."
	hatch run vibe run "hello world"

clean: ## Clean build artifacts and cache
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

notebook: ## Start Jupyter notebook with project environment
	@echo "📓 Starting Jupyter notebook..."
	hatch run --env jupyter jupyter notebook --notebook-dir=.

build: ## Build package for distribution
	@echo "📦 Building package..."
	hatch build

publish: ## Publish package to PyPI (requires authentication)
	@echo "📤 Publishing package to PyPI..."
	hatch publish

pre-commit: lint format type-check test ## Run all pre-commit checks

ci: install lint format-check type-check test coverage ## Run full CI pipeline

help: ## Show this help message
	@echo "🛠️  Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
