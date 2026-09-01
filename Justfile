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

# Check lint, formatting, types, and workflows without modifying any files
[group('test')]
lint:
  uv run ruff check
  uv run ruff format --check
  uv run pyright
  uv run zizmor .github/workflows

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

# Check, test, and build the distributions that CI will publish
[group('deploy')]
build: lint test
  #!/usr/bin/env bash
  set -euo pipefail
  uv build --clear
  # The same check the release workflow runs before it uploads, so that a
  # packaging mistake surfaces here rather than on a tag that cannot be undone.
  #
  # --isolated is what makes the environment the wheel lands in a clean one.
  # Without it uv layers the --with packages over the project's own .venv,
  # where every dependency is already installed, and a distribution that
  # failed to declare one would still import here.
  uv run --isolated --no-project --with dist/*.whl \
    python scripts/smoke_test_wheel.py "$(uv version --short)"

# Check, test, build, and publish to PyPI
[group('deploy')]
deploy: build
  #!/usr/bin/env bash
  set -euo pipefail
  if [ -n "$(git status --porcelain)" ]; then
    echo "Working tree is dirty" >&2; exit 1
  fi
  uv publish
