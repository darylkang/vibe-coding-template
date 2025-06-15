.PHONY: help install test test-watch test-cov test-file lint format type-check clean dev-setup tdd-demo

help: ## Show available commands
	@echo "🚀 Vibe Coding Template - Available Commands:"
	@echo ""
	@echo "📦 Setup & Installation:"
	@awk 'BEGIN {FS = ":.*?## "} /^install.*:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "🧪 TDD & Testing:"
	@awk 'BEGIN {FS = ":.*?## "} /^test.*:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "🔧 Code Quality:"
	@awk 'BEGIN {FS = ":.*?## "} /^(lint|format|type-check).*:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "🧹 Maintenance:"
	@awk 'BEGIN {FS = ":.*?## "} /^(clean|dev-setup).*:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "🎓 Learning:"
	@awk 'BEGIN {FS = ":.*?## "} /^tdd-demo.*:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install package in development mode
	@echo "🔧 Installing package..."
	hatch env create
	hatch run pip install -e .
	@echo "✅ Installation complete!"
	@echo ""
	@echo "🧪 Try the TDD workflow:"
	@echo "  make test-watch    # Start TDD watch mode"
	@echo "  make tdd-demo      # See TDD example"

# TDD & Testing Commands
test: ## Run all tests
	@echo "🧪 Running all tests..."
	hatch run test

test-watch: ## Run tests in watch mode for TDD (Red-Green-Refactor)
	@echo "🔄 Starting TDD watch mode..."
	@echo "💡 TDD Workflow: 🔴 Write failing test → 🟢 Make it pass → 🔄 Refactor"
	@echo "   Press Ctrl+C to stop"
	hatch run pytest --looponfail

test-cov: ## Run tests with coverage report
	@echo "📊 Running tests with coverage..."
	hatch run pytest --cov=src --cov-report=html --cov-report=term-missing
	@echo "📄 Coverage report available at: htmlcov/index.html"

test-file: ## Run specific test file (usage: make test-file FILE=tests/test_example.py)
	@echo "🎯 Running specific test file: $(FILE)"
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Please specify FILE=tests/test_example.py"; \
		exit 1; \
	fi
	hatch run pytest $(FILE) -v

# Code Quality Commands
lint: ## Lint code with ruff
	@echo "🔍 Linting code..."
	hatch run lint

format: ## Format code with ruff  
	@echo "🎨 Formatting code..."
	hatch run format

type-check: ## Type check with mypy
	@echo "🔍 Type checking..."
	hatch run type-check

# Development & Maintenance
dev-setup: install ## Complete development environment setup
	@echo "🛠️  Setting up complete development environment..."
	@echo "📋 Installing pre-commit hooks..."
	hatch run pip install pre-commit
	hatch run pre-commit install
	@echo "🧪 Running initial test suite..."
	$(MAKE) test
	@echo ""
	@echo "✅ Development environment ready!"
	@echo "🎯 Next steps:"
	@echo "  1. Run 'make tdd-demo' to see TDD in action"
	@echo "  2. Start coding with 'make test-watch'"
	@echo "  3. Check '.cursor/rules/' for TDD guidelines"

clean: ## Clean build artifacts and caches
	@echo "🧹 Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	@echo "✅ Cleanup complete!"

# TDD Learning & Demo
tdd-demo: ## Show TDD workflow example
	@echo "🎓 TDD (Test-Driven Development) Workflow Example"
	@echo "=================================================="
	@echo ""
	@echo "🔴 RED Phase: Write a failing test first"
	@echo "   def test_add_numbers():"
	@echo "       assert add_numbers(2, 3) == 5"
	@echo ""
	@echo "🟢 GREEN Phase: Write minimal code to pass"
	@echo "   def add_numbers(a, b):"
	@echo "       return a + b"
	@echo ""
	@echo "🔄 REFACTOR Phase: Improve code quality"
	@echo "   def add_numbers(a: int, b: int) -> int:"
	@echo "       \"\"\"Add two numbers and return the result.\"\"\""
	@echo "       return a + b"
	@echo ""
	@echo "💡 Key TDD Commands:"
	@echo "   make test-watch    # Continuous testing"
	@echo "   make test-cov      # Coverage analysis"
	@echo "   make test-file FILE=tests/test_module.py"
	@echo ""
	@echo "📚 Learn more: Check .cursor/rules/ for comprehensive TDD guidance"
