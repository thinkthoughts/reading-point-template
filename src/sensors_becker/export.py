"""Export utilities for the sensors-becker package."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from sensors_becker.context import RepositoryContext
from sensors_becker.paths import EXPORTS_DIR
from sensors_becker.validation import validate_context


def ensure_parent_directory(path: Path) -> Path:
    """Create the parent directory for an export path."""

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def context_to_dict(context: RepositoryContext) -> dict[str, object]:
    """Validate and convert an engineering context to a dictionary."""

    validate_context(context)
    return context.as_dict()


def write_json(data: Any, path: Path, *, indent: int = 2) -> Path:
    """Write JSON data to a file and return the resulting path."""

    ensure_parent_directory(path)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=indent,
            ensure_ascii=False,
            sort_keys=False,
        )
        file.write("\n")

    return path


def write_yaml(data: Any, path: Path) -> Path:
    """Write YAML data to a file and return the resulting path."""

    ensure_parent_directory(path)

    with path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(
            data,
            file,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )

    return path


def export_context_json(
    context: RepositoryContext,
    *,
    filename: str = "engineering_context.json",
    directory: Path = EXPORTS_DIR,
) -> Path:
    """Export an engineering context as JSON."""

    return write_json(context_to_dict(context), directory / filename)


def export_context_yaml(
    context: RepositoryContext,
    *,
    filename: str = "engineering_context.yaml",
    directory: Path = EXPORTS_DIR,
) -> Path:
    """Export an engineering context as YAML."""

    return write_yaml(context_to_dict(context), directory / filename)


def export_context_bundle(
    context: RepositoryContext,
    *,
    stem: str = "engineering_context",
    directory: Path = EXPORTS_DIR,
) -> tuple[Path, Path]:
    """Export an engineering context as matching JSON and YAML files."""

    json_path = export_context_json(
        context,
        filename=f"{stem}.json",
        directory=directory,
    )
    yaml_path = export_context_yaml(
        context,
        filename=f"{stem}.yaml",
        directory=directory,
    )
    return json_path, yaml_path


__all__ = [
    "context_to_dict",
    "ensure_parent_directory",
    "export_context_bundle",
    "export_context_json",
    "export_context_yaml",
    "write_json",
    "write_yaml",
]
