"""Repository path utilities for the sensors-becker package."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final


PACKAGE_DIR: Final[Path] = Path(__file__).resolve().parent
SRC_DIR: Final[Path] = PACKAGE_DIR.parent
REPOSITORY_ROOT: Final[Path] = SRC_DIR.parent

README_PATH: Final[Path] = REPOSITORY_ROOT / "README.md"
REQUIREMENTS_PATH: Final[Path] = REPOSITORY_ROOT / "requirements.txt"
PYPROJECT_PATH: Final[Path] = REPOSITORY_ROOT / "pyproject.toml"

NOTEBOOKS_DIR: Final[Path] = REPOSITORY_ROOT / "notebooks"
DATA_DIR: Final[Path] = REPOSITORY_ROOT / "data"
OUTPUTS_DIR: Final[Path] = REPOSITORY_ROOT / "outputs"
FIGURES_DIR: Final[Path] = OUTPUTS_DIR / "figures"
TABLES_DIR: Final[Path] = OUTPUTS_DIR / "tables"
EXPORTS_DIR: Final[Path] = OUTPUTS_DIR / "exports"
SESSION_REPORTS_DIR: Final[Path] = REPOSITORY_ROOT / "session_reports"
ENGINEERING_REPORTS_DIR: Final[Path] = REPOSITORY_ROOT / "engineering_reports"


@dataclass(frozen=True, slots=True)
class RepositoryPaths:
    """Resolved repository paths exposed to engineering notebooks."""

    repository_root: Path
    notebooks: Path
    data: Path
    outputs: Path
    figures: Path
    tables: Path
    exports: Path
    session_reports: Path
    engineering_reports: Path

    @classmethod
    def from_root(cls, repository_root: Path) -> "RepositoryPaths":
        """Create repository paths from a resolved repository root."""

        root = repository_root.resolve()
        outputs = root / "outputs"

        return cls(
            repository_root=root,
            notebooks=root / "notebooks",
            data=root / "data",
            outputs=outputs,
            figures=outputs / "figures",
            tables=outputs / "tables",
            exports=outputs / "exports",
            session_reports=root / "session_reports",
            engineering_reports=root / "engineering_reports",
        )

    def runtime_directories(self) -> tuple[Path, ...]:
        """Return directories created for notebook execution."""

        return (
            self.notebooks,
            self.data,
            self.outputs,
            self.figures,
            self.tables,
            self.exports,
            self.session_reports,
            self.engineering_reports,
        )

    def ensure_runtime_directories(self) -> tuple[Path, ...]:
        """Create and return standard runtime directories."""

        directories = self.runtime_directories()

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        return directories


DEFAULT_PATHS: Final[RepositoryPaths] = RepositoryPaths.from_root(REPOSITORY_ROOT)


def repository_path(*parts: str) -> Path:
    """Return a path relative to the installed repository root."""

    return REPOSITORY_ROOT.joinpath(*parts)


def paths_for_root(repository_root: Path) -> RepositoryPaths:
    """Return repository paths for an explicit repository root."""

    return RepositoryPaths.from_root(repository_root)


def reading_order_paths(
    repository_root: Path = REPOSITORY_ROOT,
) -> tuple[Path, ...]:
    """Return Reading Order documents in filename order."""

    return tuple(sorted(repository_root.glob("RO_*.md")))


def engineering_statement_paths(
    repository_root: Path = REPOSITORY_ROOT,
) -> tuple[Path, ...]:
    """Return Engineering Statement files in filename order."""

    paths = (
        *repository_root.glob("ES_*.md"),
        *repository_root.glob("ES_*.yaml"),
        *repository_root.glob("ES_*.yml"),
    )
    return tuple(sorted(paths))


def ensure_runtime_directories() -> tuple[Path, ...]:
    """Create standard directories for the installed repository."""

    return DEFAULT_PATHS.ensure_runtime_directories()


__all__ = [
    "DATA_DIR",
    "DEFAULT_PATHS",
    "ENGINEERING_REPORTS_DIR",
    "EXPORTS_DIR",
    "FIGURES_DIR",
    "NOTEBOOKS_DIR",
    "OUTPUTS_DIR",
    "PACKAGE_DIR",
    "PYPROJECT_PATH",
    "README_PATH",
    "REPOSITORY_ROOT",
    "REQUIREMENTS_PATH",
    "RepositoryPaths",
    "SESSION_REPORTS_DIR",
    "SRC_DIR",
    "TABLES_DIR",
    "engineering_statement_paths",
    "ensure_runtime_directories",
    "paths_for_root",
    "reading_order_paths",
    "repository_path",
]
