# Contributing to Stacked SEDs

Thank you for your interest in contributing to Stacked SEDs! This document provides guidelines for contributing to the project.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

## Getting Started

### Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/stacked-seds.git
   cd stacked-seds
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**:
   ```bash
   make install-dev
   make install
   ```

4. **Run tests to verify setup**:
   ```bash
   make test
   ```

### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clear, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Run quality checks**:
   ```bash
   make check  # Runs formatting, linting, and tests
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

5. **Push and create a pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Standards

### Code Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
make format        # Format all code
make format-check  # Check formatting without changes
```

### Linting

We use [flake8](https://flake8.pycqa.org/) for linting:

```bash
make lint  # Run linting checks
```

### Testing

We use [pytest](https://pytest.org/) for testing:

```bash
make test           # Run all tests
make test-coverage  # Run tests with coverage report
```

**Testing Guidelines**:
- Write tests for all new functions
- Aim for >90% code coverage
- Use descriptive test function names
- Include both positive and negative test cases

### Documentation

#### Docstring Style

Use NumPy-style docstrings:

```python
def example_function(param1: int, param2: str) -> bool:
    """
    Brief description of the function.

    Longer description if needed, explaining what the function does,
    any important algorithms, or usage notes.

    Parameters
    ----------
    param1 : int
        Description of the first parameter.
    param2 : str
        Description of the second parameter.

    Returns
    -------
    bool
        Description of the return value.

    Raises
    ------
    ValueError
        Description of when this error is raised.

    Examples
    --------
    >>> result = example_function(42, "hello")
    >>> print(result)
    True
    """
    return True
```

#### Building Documentation

```bash
make docs        # Build documentation
make docs-serve  # Serve documentation locally
```

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

- **Environment**: Python version, OS, package versions
- **Reproduction steps**: Minimal code example
- **Expected vs. actual behavior**
- **Error messages**: Full traceback if applicable

### Feature Requests

For new features, please:

- **Check existing issues** to avoid duplicates
- **Describe the use case** and motivation
- **Provide examples** of how it would be used
- **Consider implementation** complexity and scope

### Code Contributions

We welcome contributions including:

- **Bug fixes**
- **New features**
- **Performance improvements**
- **Documentation improvements**
- **Test coverage improvements**

### Documentation Contributions

Documentation improvements are highly valued:

- **Tutorial improvements**
- **API documentation clarifications**
- **Example notebooks**
- **FAQ additions**

## Pull Request Process

1. **Ensure all tests pass** and code is properly formatted
2. **Update documentation** for any new features
3. **Add tests** for new functionality
4. **Update changelog** if significant changes
5. **Write clear commit messages** and PR description

### PR Description Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## Release Process

Releases are handled by maintainers and follow semantic versioning:

- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, backward compatible

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: ryan.trainor@fandm.edu for direct contact

## Recognition

Contributors are recognized in:

- **Changelog**: All contributions are documented
- **Authors file**: Significant contributors are listed
- **GitHub contributors page**: Automatic recognition

Thank you for contributing to Stacked SEDs!
