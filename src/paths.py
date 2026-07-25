"""Repository path utilities for the sensors-becker package."""

from __future__ import annotations

from pathlib import Path
from typing import Final


# Package and repository locations

PACKAGE_DIR: Final[Path] = Path(__file__).resolve().parent
SRC_DIR: Final[Path] = PACKAGE_DIR.parent
REPOSITORY_ROOT: Final[Path] = SRC_DIR.parent


# Repository files

README_PATH: Final[Path] = REPOSITORY_ROOT / "README.md"
REQUIREMENTS_PATH: Final[Path] = REPOSITORY_ROOT / "requirements.txt"
PYPROJECT_PATH: Final[Path] = REPOSITORY_ROOT / "pyproject.toml"


# Engineering artifact locations

NOTEBOOKS_DIR: Final[Path] = REPOSITORY_ROOT / "notebooks"
DATA_DIR: Final[Path] = REPOSITORY_ROOT / "data"
OUTPUTS_DIR: Final[Path] = REPOSITORY_ROOT / "outputs"
FIGURES_DIR: Final[Path] = OUTPUTS_DIR / "figures"
TABLES_DIR: Final[Path] = OUTPUTS_DIR / "tables"
EXPORTS_DIR: Final[Path] = OUTPUTS_DIR / "exports"
SESSION_REPORTS_DIR: Final[Path] = REPOSITORY_ROOT / "session_reports"
ENGINEERING_REPORTS_DIR: Final[Path] = REPOSITORY_ROOT / "engineering_reports"


def repository_path(*parts: str) -> Path:
    """Return a path relative to the repository root."""

    return REPOSITORY_ROOT.joinpath(*parts)


def notebook_path(filename: str) -> Path:
    """Return the path for a notebook filename."""

    return NOTEBOOKS_DIR / filename


def data_path(filename: str) -> Path:
    """Return the path for a repository data file."""

    return DATA_DIR / filename


def output_path(filename: str) -> Path:
    """Return the path for a general notebook output."""

    return OUTPUTS_DIR / filename


def figure_path(filename: str) -> Path:
    """Return the path for a generated figure."""

    return FIGURES_DIR / filename


def table_path(filename: str) -> Path:
    """Return the path for a generated table."""

    return TABLES_DIR / filename


def export_path(filename: str) -> Path:
    """Return the path for an exported repository artifact."""

    return EXPORTS_DIR / filename


def reading_order_paths() -> tuple[Path, ...]:
    """Return Reading Order documents in filename order."""

    return tuple(sorted(REPOSITORY_ROOT.glob("RO_*.md")))


def engineering_statement_paths() -> tuple[Path, ...]:
    """Return Engineering Statement files in filename order."""

    markdown_paths = REPOSITORY_ROOT.glob("ES_*.md")
    yaml_paths = REPOSITORY_ROOT.glob("ES_*.yaml")
    yml_paths = REPOSITORY_ROOT.glob("ES_*.yml")

    return tuple(sorted((*markdown_paths, *yaml_paths, *yml_paths)))


def ensure_runtime_directories() -> tuple[Path, ...]:
    """Create and return the standard runtime directories."""

    directories = (
        NOTEBOOKS_DIR,
        DATA_DIR,
        OUTPUTS_DIR,
        FIGURES_DIR,
        TABLES_DIR,
        EXPORTS_DIR,
        SESSION_REPORTS_DIR,
        ENGINEERING_REPORTS_DIR,
    )

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    return directories


__all__ = [
    "PACKAGE_DIR",
    "SRC_DIR",
    "REPOSITORY_ROOT",
    "README_PATH",
    "REQUIREMENTS_PATH",
    "PYPROJECT_PATH",
    "NOTEBOOKS_DIR",
    "DATA_DIR",
    "OUTPUTS_DIR",
    "FIGURES_DIR",
    "TABLES_DIR",
    "EXPORTS_DIR",
    "SESSION_REPORTS_DIR",
    "ENGINEERING_REPORTS_DIR",
    "repository_path",
    "notebook_path",
    "data_path",
    "output_path",
    "figure_path",
    "table_path",
    "export_path",
    "reading_order_paths",
    "engineering_statement_paths",
    "ensure_runtime_directories",
]
