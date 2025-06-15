# 🚀 Vibe Coding Template

A minimal Python starter template optimized for LLM-assisted development with modern tooling.

[![CI](https://github.com/darylkang/vibe-coding-template/workflows/CI/badge.svg)](https://github.com/darylkang/vibe-coding-template/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## ✨ What's Included

This template provides a clean foundation for modern Python development:

- **Modern Dependencies**: Hatch, Pydantic v2, Typer for CLIs
- **Type Safety**: Full type hints with mypy checking
- **Code Quality**: Ruff for linting and formatting
- **Testing**: pytest with basic coverage
- **Configuration**: Pydantic Settings with environment variables
- **LLM-Optimized**: Clean patterns that AI can understand and extend

## 🚀 Quick Start

1. **Clone and install**
   ```bash
   git clone https://github.com/darylkang/vibe-coding-template.git
   cd vibe-coding-template
   make install
   ```

2. **Try the CLI**
   ```bash
   hatch shell
   vibe process "hello world"
   vibe info
   ```

## 🧪 Development

```bash
# Run tests
make test

# Lint and format
make lint
make format

# Type check
make type-check

# Clean up
make clean
```

## 📁 Project Structure

```
├── src/my_package/          # Main package
│   ├── core.py              # Business logic
│   ├── cli.py               # Command-line interface
│   └── settings.py          # Configuration
├── tests/                   # Test suite
├── pyproject.toml           # Project configuration
└── Makefile                 # Development commands
```

## 🔧 Customization

1. **Rename the package**: Update `my_package` to your project name
2. **Modify core logic**: Edit `src/my_package/core.py`
3. **Add CLI commands**: Extend `src/my_package/cli.py`
4. **Configure settings**: Adjust `src/my_package/settings.py`
5. **Add dependencies**: Update `pyproject.toml`

## 📝 License

This is a private project.

## 🧠 Optional: Enable TaskMaster AI

Once you start a new project from this template, you can optionally enable [TaskMaster AI](https://task-master.dev) for structured task and subtask generation:

1. **Add API keys** to `.cursor/mcp.json`
2. **Enable in Cursor**:  
   Open the MCP tab in Cursor and activate `taskmaster-ai`
3. **Add a PRD**:  
   Create `.taskmaster/docs/prd.txt` and add your product requirements
4. **Prompt Cursor**:  
   Ask: `Initialize taskmaster-ai in my project`

TaskMaster will help structure your LLM-driven workflows and make Cursor more effective.

---

**Built for speed** ⚡ **LLM-friendly** 🤖 **Modern Python** 🐍
