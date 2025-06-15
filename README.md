# 🚀 Vibe Coding Template

A modern Python starter kit optimized for LLM-assisted development with Cursor, featuring best practices for rapid prototyping and production-ready applications.

[![CI](https://github.com/yourusername/vibe-coding-template/workflows/CI/badge.svg)](https://github.com/yourusername/vibe-coding-template/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

## ✨ Features

This template provides a complete foundation for modern Python development:

### 🏗️ Project Structure
- **Clean Architecture**: Well-organized `src/` layout following Python packaging best practices
- **Modern Dependencies**: Hatch, Pydantic v2, Typer, Rich for beautiful CLIs
- **Type Safety**: Full type hints with mypy checking
- **Configuration Management**: Pydantic Settings with environment variable support

### 🔧 Development Tools
- **Hatch**: Modern Python project management and virtual environments
- **Ruff**: Lightning-fast linting and formatting (replaces Black, isort, flake8)
- **pytest**: Comprehensive testing with coverage reporting
- **mypy**: Static type checking for better code quality

### 🎨 User Experience
- **Rich CLI**: Beautiful command-line interfaces with colors, tables, and progress bars
- **Error Handling**: Graceful error handling with user-friendly messages
- **Logging**: Structured logging with Rich integration

### 🤖 LLM-Optimized
- **Cursor Integration**: Custom rules and guidelines for AI-assisted development
- **Clear Patterns**: Consistent code patterns that LLMs can understand and extend
- **Documentation**: Comprehensive docstrings and inline guidance

## 📦 Installation

### Requirements
- Python 3.10+
- [Hatch](https://hatch.pypa.io/) for project management

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/vibe-coding-template.git
   cd vibe-coding-template
   ```

2. **Install the project**
   ```bash
   make install
   # or manually:
   pip install hatch
   hatch env create
   ```

3. **Activate the environment**
   ```bash
   hatch shell
   ```

4. **Verify installation**
   ```bash
   vibe --help
   ```

## 🚀 Usage

### Command Line Interface

The template includes a fully-featured CLI built with Typer and Rich:

```bash
# Basic text processing
vibe run "hello world" --transform uppercase
vibe run "HELLO WORLD" --transform lowercase

# Batch processing from file
echo -e "hello\nworld\ntest" > input.txt
vibe batch input.txt --transform title --output results.txt

# View available transformations
vibe transforms

# Get package information
vibe info
```

### Python API

```python
from my_package import MyPackage

# Initialize with custom settings
app = MyPackage(verbose=True)

# Process single item
result = app.process("hello world", transform_type="title")
print(result.output_data)  # "Hello World"
print(result.metadata)     # Processing metadata

# Batch processing
results = app.batch_process(
    ["hello", "world", "python"],
    transform_type="uppercase"
)

# Get application statistics
stats = app.get_stats()
```

### Configuration

The application uses Pydantic Settings for configuration management:

```python
from my_package.settings import Settings

# Load from environment variables (APP_* prefix)
settings = Settings()

# Or provide custom values
settings = Settings(
    debug=True,
    log_level="DEBUG",
    max_batch_size=50
)
```

Environment variables:
```bash
export APP_DEBUG=true
export APP_LOG_LEVEL=DEBUG
export APP_MAX_BATCH_SIZE=200
export APP_DEFAULT_TRANSFORM=lowercase
```

## 🧪 Development

### Development Setup

```bash
# Install with development dependencies
make dev-install

# Run the full development pipeline
make ci
```

### Common Commands

```bash
# Testing
make test              # Run tests
make test-cov          # Run tests with coverage
make coverage          # Generate coverage reports

# Code Quality
make lint              # Lint with ruff
make format            # Format with ruff
make type-check        # Type check with mypy

# Utilities
make clean             # Clean build artifacts
make build             # Build package
make notebook          # Start Jupyter notebook
```

### Project Structure

```
vibe-coding-template/
├── src/my_package/           # Main package source
│   ├── __init__.py          # Package exports
│   ├── core.py              # Business logic
│   ├── cli.py               # Command-line interface
│   └── settings.py          # Configuration management
├── tests/                   # Test suite
│   ├── conftest.py         # Shared test fixtures
│   ├── test_core.py        # Core functionality tests
│   └── test_settings.py    # Settings tests
├── .cursor/rules/          # Cursor AI guidelines
├── .github/workflows/      # CI/CD pipelines
├── pyproject.toml         # Project configuration
├── Makefile              # Development commands
└── README.md            # This file
```

### Adding New Features

When adding new functionality:

1. **Define data models** using Pydantic in appropriate modules
2. **Implement core logic** in `src/my_package/core.py`
3. **Add CLI commands** in `src/my_package/cli.py`
4. **Write tests** in `tests/` with appropriate fixtures
5. **Update documentation** as needed

Example of adding a new transformation:

```python
# In core.py - add to _apply_transformation method
transformations = {
    # ... existing transformations
    "slugify": lambda x: x.lower().replace(" ", "-"),
}

# In cli.py - transformation will be automatically available
# Tests will automatically cover the new transformation via parametrize
```

## 🔧 Customization

### Renaming the Package

To customize this template for your project:

1. **Rename the package directory**: `src/my_package` → `src/your_package`
2. **Update imports** throughout the codebase
3. **Modify `pyproject.toml`**: Update name, description, and entry points
4. **Update CLI command name** in `pyproject.toml` scripts section

### Configuration Options

Key settings in `pyproject.toml`:

```toml
[project]
name = "your-project-name"
description = "Your project description"

[project.scripts]
your-cli = "your_package.cli:app"

[tool.hatch.version]
path = "src/your_package/__init__.py"
```

## 🤖 Cursor Integration

This template is optimized for Cursor AI development:

- **Custom Rules**: `.cursor/rules/` contains guidelines for consistent code generation
- **Clear Patterns**: Consistent code patterns that AI can understand and extend
- **Comprehensive Docstrings**: Rich documentation for context-aware completions
- **INSTRUCTIONS FOR CURSOR**: Inline comments guide AI suggestions

### Using with Cursor

1. Open the project in Cursor
2. The custom rules will automatically apply
3. Use comments like `# CURSOR: Add a method to handle CSV export` for targeted assistance
4. Leverage the existing patterns for consistent code generation

## 📊 Testing

The template includes comprehensive testing:

- **Unit Tests**: Individual function/method testing
- **Integration Tests**: End-to-end workflow testing
- **Fixtures**: Reusable test data and setup
- **Parametrized Tests**: Multiple input scenarios
- **Mocking**: External dependency isolation

```bash
# Run specific test categories
pytest tests/test_core.py::TestMyPackage -v
pytest tests/ -k "test_batch" -v

# Coverage reporting
pytest --cov=my_package --cov-report=html
```

## 🚀 Deployment

### Building for Distribution

```bash
# Build package
make build

# Check package
twine check dist/*

# Upload to PyPI (configure credentials first)
make publish
```

### Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install hatch
RUN hatch build
RUN pip install dist/*.whl

CMD ["vibe", "--help"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the full test suite: `make ci`
5. Commit and push your changes
6. Create a Pull Request

## 📝 License

This is a private project.

## 🙏 Acknowledgments

- **Hatch** for modern Python project management
- **Pydantic** for data validation and settings
- **Typer** for beautiful CLI creation
- **Rich** for terminal formatting
- **Cursor** for AI-assisted development

---

**Built with ❤️ for the Python community and optimized for AI-assisted development**
