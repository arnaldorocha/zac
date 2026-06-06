# Contributing to Zac

Thank you for your interest in contributing to Zac! We welcome all contributions.

## Code of Conduct

- Be respectful and inclusive
- Follow Python best practices (PEP 8, type hints)
- Write clear, descriptive commit messages
- Test your changes

## Development Setup

```bash
# Clone repository
git clone https://github.com/arnaldorocha/zac.git
cd zac

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8 mypy

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or for bugfixes
git checkout -b bugfix/issue-description
```

### 2. Make Changes
- Follow the existing code style
- Add type hints
- Write docstrings
- Update tests
- Add logging

### 3. Format Code

```bash
# Format with Black
black .

# Check with Flake8
flake8 .

# Type check with MyPy
mypy .
```

### 4. Write Tests

```bash
# Run existing tests
pytest tests/ -v

# Add new tests in tests/
# Use pytest fixtures
# Test both success and error cases
```

### 5. Commit Changes

```bash
git add .
git commit -m "Feature: Add awesome feature

- Description of what was added
- Why it was needed
- Any breaking changes"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a PR on GitHub with a clear description.

## Project Structure

```
zac/
├── core/              # Core logic
├── voice/             # Voice I/O
├── browser/           # Browser automation
├── sheets/            # Google Sheets
├── tasks/             # Task management
├── calendar/          # Calendar
├── memory/            # Memory storage
├── database/          # Data layer
├── api/               # REST API
└── tests/             # Tests
```

## Adding a New Feature

### Example: Adding Expense Tracking

1. **Create service**: `expense/expense_service.py`
2. **Add tests**: `tests/test_expense.py`
3. **Add to assistant**: Update `core/assistant.py`
4. **Add commands**: Update `core/command_router.py`
5. **Document**: Update README.md

### File Template

```python
"""
[Module name] - [Description]
"""
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class [ServiceName]:
    """[Class description]."""
    
    def __init__(self, db_manager):
        """Initialize."""
        self.db = db_manager
    
    def method_name(self, param: str) -> Optional[bool]:
        """
        Method description.
        
        Args:
            param: Parameter description
            
        Returns:
            Description of return value
        """
        try:
            # Implementation
            logger.info(f"Operation completed: {param}")
            return True
        except Exception as e:
            logger.error(f"Error: {e}")
            return False
```

## Testing Guidelines

```python
import pytest
from core.assistant import ZacAssistant

@pytest.fixture
def assistant():
    """Create test assistant."""
    return ZacAssistant(db_path="test.db")

def test_feature(assistant):
    """Test description."""
    result = assistant.some_method()
    assert result is not None
```

## Documentation Guidelines

- Add docstrings to all functions
- Use type hints
- Update README.md for user-facing changes
- Update API.md for API changes
- Add examples where helpful

## Issues and Bugs

### Reporting Issues

1. Check if issue already exists
2. Provide clear description
3. Include steps to reproduce
4. Include environment info:
   - Windows version
   - Python version
   - Relevant dependencies

### Requesting Features

1. Clearly describe the feature
2. Explain the use case
3. Provide examples
4. Consider the architecture impact

## Code Review Process

- Tests must pass
- Code must be formatted with Black
- No major type errors (MyPy)
- At least one approval required
- Contributions must follow SOLID principles

## Commit Guidelines

### Format

```
[Type]: [Subject]

[Body explaining what and why]

[References: Closes #123]
```

### Types

- `Feature`: New feature
- `Fix`: Bug fix
- `Docs`: Documentation
- `Refactor`: Code refactoring
- `Test`: Adding tests
- `Perf`: Performance improvement

### Examples

```
Feature: Add expense tracking

- Created expense service
- Added expense commands
- Integrated with Google Sheets
- Added tests

Closes #45
```

```
Fix: Correct Vosk initialization error

The Vosk model was not properly initialized on Windows systems.
Changed model loading to use absolute paths.

Closes #32
```

## Performance Considerations

- Use efficient algorithms
- Consider database indexing
- Profile code when necessary
- Use async/await where applicable
- Minimize blocking operations

## Security Considerations

- Don't commit credentials
- Validate user input
- Use parameterized queries (SQLite)
- Handle sensitive data carefully
- Keep dependencies updated

## Future Development Areas

Priority for contributions:

1. **High Priority**
   - Bug fixes
   - Performance improvements
   - Documentation
   - Unit tests coverage

2. **Medium Priority**
   - New voice commands
   - Additional services
   - API improvements
   - Error handling

3. **Interesting Future Work** (v2.0+)
   - LLM integration
   - Vision support
   - Multi-agent systems
   - Plugin architecture

## Help and Questions

- Open an issue for questions
- Check existing issues first
- Ask in discussions section
- Comment on related PRs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to making Zac better! 🚀
