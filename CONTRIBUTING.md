# Contributing to Catawiki Scraper

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Catawiki-Scraper.git
   cd Catawiki-Scraper
   ```
3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow the existing code style
   - Add docstrings to functions/classes
   - Update tests if needed

3. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

4. **Check code quality:**
   ```bash
   # Format code
   black src/ tests/
   
   # Check style
   flake8 src/ tests/
   
   # Type checking
   mypy src/
   ```

5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

6. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style Guidelines

### Python

- **PEP 8** compliance
- **Type hints** on all functions
- **Docstrings** (Google style) for all public functions/classes
- **Line length:** Max 100 characters
- **Naming:**
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### Example:

```python
"""
Module docstring explaining purpose.
"""
from typing import List, Optional


class MyClass:
    """
    Class docstring with description.
    
    Attributes:
        attribute_name: Description of attribute
    """
    
    def my_method(self, param: str) -> Optional[int]:
        """
        Method docstring.
        
        Args:
            param: Description of parameter
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When something is invalid
        """
        pass
```

## Commit Message Guidelines

Follow **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

### Examples:
```
feat(analyzer): add deal scoring algorithm

Implemented a scoring system that rates deals from 0.0 (best) to 1.0 (worst)
based on price ratio to estimated value.

Closes #123
```

## Testing Guidelines

- **Write tests** for new features
- **Maintain coverage** above 80%
- **Use pytest** fixtures for common setup
- **Mock external services** (Telegram, Selenium)

### Example Test:

```python
def test_feature():
    """Test that feature works correctly."""
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = my_function(input_data)
    
    # Assert
    assert result == expected_value
```

## Pull Request Process

1. **Ensure all tests pass**
2. **Update documentation** if needed
3. **Add entry to CHANGELOG** (if exists)
4. **Request review** from maintainers
5. **Address review comments**
6. **Squash commits** if requested

### PR Title Format:
```
feat: add new feature
fix: resolve bug in analyzer
docs: update installation guide
```

## Reporting Issues

When reporting bugs, please include:

1. **Description** of the issue
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Environment details:**
   - OS and version
   - Python version
   - Chrome/Chromium version
6. **Relevant logs** or error messages

## Feature Requests

We welcome feature suggestions! Please:

1. **Check existing issues** first
2. **Describe the feature** clearly
3. **Explain the use case**
4. **Provide examples** if possible

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on what's best for the project
- Show empathy towards others

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!** 🎉
