#!/usr/bin/env bash
set -e

# Install uv if not present
if ! command -v uv &> /dev/null; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# Sync dependencies (creates venv and installs from pyproject.toml if needed)
uv sync

# run the project
uv run python mail_craft.py
