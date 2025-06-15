# 🚀 Vibe Coding Template

A minimal Python starter template optimized for LLM-assisted development with **Test-Driven Development (TDD)** enforcement and modern tooling.

[![CI](https://github.com/darylkang/vibe-coding-template/workflows/CI/badge.svg)](https://github.com/darylkang/vibe-coding-template/actions)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![TDD Enforced](https://img.shields.io/badge/TDD-enforced-green.svg)](https://github.com/darylkang/vibe-coding-template)

## ✨ What's Included

This template provides a clean foundation for modern Python development with **mandatory Test-Driven Development**:

### 🧪 **TDD-First Development**
- **Enforced Red-Green-Refactor cycle** via Cursor rules
- **Test-first methodology** for all new features
- **Comprehensive testing patterns** and examples
- **pytest** with coverage reporting and watch mode

### 🛠️ **Modern Development Stack**
- **Hatch** for project management and virtual environments
- **Pydantic v2** for data validation and settings
- **Typer** for beautiful CLI interfaces
- **Type Safety** with full mypy checking
- **Code Quality** with Ruff linting and formatting

### 🤖 **LLM-Optimized Workflow**
- **Cursor rules** that enforce TDD and code quality
- **TaskMaster AI integration** for structured task management
- **Clean patterns** that AI can understand and extend

## 🚀 Quick Start

1. **Clone and install**
   ```bash
   git clone https://github.com/darylkang/vibe-coding-template.git
   cd vibe-coding-template
   make install
   ```

2. **Verify TDD setup**
   ```bash
   make test          # Run existing tests
   make test-watch    # Start TDD watch mode
   ```

3. **Try the CLI**
   ```bash
   hatch run vibe process "hello world"
   hatch run vibe info
   ```

## 🧪 TDD Development Workflow

This template **enforces Test-Driven Development** through Cursor rules:

### 🔴 RED → 🟢 GREEN → 🔄 REFACTOR

```bash
# 1. Write a failing test first
pytest tests/test_new_feature.py::test_feature -v  # Should FAIL

# 2. Write minimal code to pass
pytest tests/test_new_feature.py::test_feature -v  # Should PASS  

# 3. Refactor and run all tests
make test  # All tests should PASS
```

### Available TDD Commands

```bash
# Core TDD workflow
make test-watch    # Continuous testing for TDD
make test          # Run all tests
make test-cov      # Run tests with coverage
make test-file     # Run specific test file

# Development cycle
make lint          # Check code quality
make format        # Auto-format code
make type-check    # Static type checking
make clean         # Clean build artifacts
```

## 📁 Project Structure

```
├── .cursor/                    # Cursor AI configuration
│   ├── rules/                  # TDD and code quality rules
│   │   ├── development.mdc     # Core TDD methodology
│   │   ├── tdd-workflow.mdc    # Quick TDD reference
│   │   └── code-style.mdc      # Python code standards
│   └── mcp.json                # TaskMaster AI configuration
├── src/my_package/             # Main package
│   ├── core.py                 # Business logic
│   ├── cli.py                  # Command-line interface
│   └── settings.py             # Configuration
├── tests/                      # Test suite (pytest)
├── .taskmaster/                # TaskMaster AI integration
├── .env.example                # Environment variables template
├── pyproject.toml              # Project configuration
├── Makefile                    # Development commands
└── README.md                   # You are here
```

## 🔧 Customization Guide

### 1. **Rename the Package**
```bash
# Update package name throughout
find . -name "*.py" -o -name "*.toml" -o -name "*.md" | xargs sed -i 's/my_package/your_package/g'
mv src/my_package src/your_package
```

### 2. **Add New Features (TDD Style)**
```python
# Always start with a test
def test_new_feature():
    result = new_feature("input")
    assert result == "expected_output"

# Then implement minimal code to pass
def new_feature(input_data):
    return "expected_output"
```

### 3. **Extend CLI Commands**
```python
# In src/my_package/cli.py
@app.command()
def new_command():
    """Add your new CLI command."""
    pass
```

### 4. **Configure Settings**
```python
# In src/my_package/settings.py
class Settings(BaseSettings):
    new_setting: str = "default_value"
```

## 🤖 TaskMaster AI Integration

Enable structured task management for LLM-driven development:

### 1. **Setup TaskMaster** (Optional)
```bash
# 1. Copy environment template and add your API keys
cp .env.example .env
# Edit .env and add your actual API keys:
# ANTHROPIC_API_KEY=your_actual_key_here
# OPENAI_API_KEY=your_actual_key_here
# PERPLEXITY_API_KEY=your_actual_key_here

# 2. Install TaskMaster AI
npm install -g task-master-ai

# 3. In Cursor, activate the taskmaster-ai MCP server
# The .cursor/mcp.json file will automatically use your .env variables
```

### 2. **Initialize TaskMaster**
```bash
# In Cursor, ask: "Initialize taskmaster-ai in my project"
# This will set up task management structure
```

### 3. **Add Project Requirements**
```bash
# Create .taskmaster/docs/prd.txt with your requirements
# Then ask Cursor: "Parse my PRD and generate initial tasks"
```

### 4. **TDD + TaskMaster Workflow**
```bash
# Get next task to implement
# Ask Cursor: "What's the next task I should work on?"

# For each task, follow TDD:
# 1. Write failing tests
# 2. Implement minimal code
# 3. Refactor
# 4. Update task status
```

## 📊 Code Quality Standards

- **Test Coverage**: Minimum 50% (configured in pyproject.toml)
- **Type Safety**: Full type hints required (mypy enforcement)
- **Code Style**: Ruff formatting and linting
- **TDD Compliance**: All features must start with tests

## 🔍 Monitoring & CI

- **GitHub Actions**: Automated testing, linting, and type checking on Python 3.13
- **Pre-commit hooks**: Code quality checks before commits
- **Coverage reporting**: HTML reports in `htmlcov/`

## 📚 Template Philosophy

This template is built around these principles:

1. **🧪 Test-First Development**: Every feature starts with a failing test
2. **🤖 LLM-Friendly**: Clean patterns that AI assistants can understand
3. **⚡ Speed**: Fast development with modern tooling
4. **🛡️ Quality**: Enforced standards through tooling and rules
5. **📈 Scalable**: Structure that grows with your project

## 🎯 Next Steps

After creating your project:

1. **Follow the TDD workflow** - Cursor will guide you
2. **Customize the package** name and structure
3. **Add your business logic** with tests first
4. **Optionally enable TaskMaster** for structured development
5. **Set up CI/CD** for your repository

## 📝 License

This template is provided as-is for development use.

---

**🔴 Test First** • **🟢 Make It Work** • **🔄 Make It Better**

Built with ❤️ for modern Python development
