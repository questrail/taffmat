# List the available justfile recipes
[group('general')]
@default:
  just --list --unsorted

# List the lines of code in the project
[group('general')]
loc:
  scc --remap-unknown "-*- Justfile -*-":"justfile"

# Search pydoc for given term
[group('general')]
doc term:
  uv run python -m pydoc {{term}}

# Check lint, formatting, and types without modifying any files
[group('test')]
lint:
  uv run ruff check
  uv run ruff format --check
  uv run pyright

# Lint and format code and apply changes
[group('test')]
fix:
  uv run ruff check --fix
  uv run ruff format

# Test code using pytest
[group('test')]
test *args:
  uv run pytest {{args}}

# Test code and report coverage
[group('test')]
cov *args:
  uv run pytest --cov --cov-report=term --cov-report=html {{args}}

# Add dependency
[group('dependencies')]
add dep:
  uv add {{dep}}

# Add dependency to the development group
[group('dependencies')]
dev dep:
  uv add --dev {{dep}}

# Update dependency in the project dependencies or any group
[group('dependencies')]
up dep:
  uv lock -P {{dep}}
  uv sync

# Update all dependencies
[group('dependencies')]
up-all:
  uv lock --upgrade
  uv sync

# List the outdated dependencies
[group('dependencies')]
out:
  uv pip list --outdated

# Lock/freeze dependencies
[group('dependencies')]
lock:
  uv lock

# Build the sdist and wheel from a clean dist/
[group('deploy')]
build:
  # Clearing dist/ leaves uv publish exactly the current version to upload,
  # rather than every build the directory has ever collected.
  rm -rf dist
  uv build

# Check, test, build, and publish to PyPI
[group('deploy')]
deploy: lint test
  @test -z "$(git status --porcelain)" || { echo "Working tree is dirty"; exit 1; }
  just build
  uv publish
