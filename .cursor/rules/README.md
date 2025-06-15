# Cursor Rules for Test-Driven Development

This directory contains Cursor rules that enforce Test-Driven Development (TDD) practices for all projects created from this template.

## Files Overview

### `development.mdc` - Core TDD Rules
- **Primary TDD methodology and workflow**
- Red-Green-Refactor cycle enforcement
- Comprehensive testing patterns and examples
- TDD anti-patterns to avoid
- Integration with project tooling

### `code-style.mdc` - Code Quality Standards
- Python coding conventions with TDD requirements
- Testing section emphasizes TDD-first approach
- Type hints, documentation, and structure guidelines
- LLM-friendly coding patterns

### `tdd-workflow.mdc` - Quick Reference
- Fast TDD workflow lookup
- Essential commands and checklist
- Visual indicators for TDD phases
- Common anti-patterns alert

## How TDD Rules Work

These rules are automatically attached to relevant files (`@src/**/*.py`, `@tests/**/*.py`, `@*.py`) and will:

1. **Prompt Cursor to write tests first** before any implementation
2. **Enforce the Red-Green-Refactor cycle** for all feature development
3. **Provide examples and patterns** for effective TDD
4. **Guide proper test structure** using AAA (Arrange-Act-Assert) pattern
5. **Ensure comprehensive test coverage** including edge cases

## For Template Users

When you create a new project from this template:

1. **All Cursor AI assistance will follow TDD principles**
2. **Tests will be written before implementation** automatically
3. **Code quality standards will be maintained** throughout development
4. **Examples and patterns will be readily available** for reference

## Testing Commands Available

From the project root, you can use:

```bash
# Quick test runs
make test                    # Run all tests
pytest tests/               # Direct pytest usage
pytest --looponfail        # Watch mode

# With coverage
pytest --cov=src --cov-report=html

# Specific tests
pytest tests/test_module.py::test_function -v
```

## Benefits of This Approach

- **Higher code quality** through test-first development
- **Better design** as tests drive implementation
- **Faster debugging** with comprehensive test coverage
- **Confident refactoring** with safety net of tests
- **Consistent development approach** across all template projects

## Customization

You can extend these rules by:
1. Adding project-specific patterns to `development.mdc`
2. Modifying test coverage requirements in `code-style.mdc`
3. Adding custom commands to `tdd-workflow.mdc`

The rules are designed to be generic and reusable across different project types while maintaining strict TDD discipline.

---

**Remember: Every feature starts with a failing test!** 🔴 → 🟢 → 🔄 