.PHONY: help install format format-check lint test test-coverage check clean

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install package and dependencies
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Installation complete!"

format: ## Format code with Black
	black stacked_seds/ tests/ *.py
	@echo "✅ Code formatting complete!"

format-check: ## Check code formatting without making changes
	black --check stacked_seds/ tests/ *.py
	@echo "✅ Code formatting check complete!"

lint: ## Run flake8 linting
	flake8 stacked_seds/ tests/
	@echo "✅ Linting complete!"

test: ## Run tests with pytest
	pytest -v
	@echo "✅ Tests complete!"

test-coverage: ## Run tests with coverage report
	pytest --cov=stacked_seds --cov-report=html --cov-report=term-missing --cov-report=xml -v
	@echo "✅ Tests with coverage complete! Check htmlcov/index.html for detailed report."

check: format-check lint test ## Run all quality checks (format + lint + test)
	@echo "✅ All quality checks passed!"

clean: ## Clean build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✅ Cleanup complete!"

# Development dependencies (optional - run manually if needed)
install-dev: ## Install development dependencies
	pip install black flake8 pytest pytest-cov pre-commit
	@echo "✅ Development dependencies installed!"

docs: ## Build documentation
	cd docs && make html
	@echo "✅ Documentation built! Open docs/build/html/index.html"

docs-clean: ## Clean documentation build
	cd docs && make clean
	@echo "✅ Documentation cleaned!"

docs-serve: ## Serve documentation locally
	cd docs/build/html && python -m http.server 8000
	@echo "📖 Documentation served at http://localhost:8000"
