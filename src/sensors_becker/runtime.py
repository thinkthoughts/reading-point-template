"""Notebook runtime coordination for the sensors-becker package."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

from sensors_becker.context import RepositoryContext, default_context
from sensors_becker.export import export_context_bundle
from sensors_becker.figures import export_default_figures
from sensors_becker.paths import RepositoryPaths, paths_for_root
from sensors_becker.validation import validate_context


REPOSITORY_URL: Final[str] = (
    "https://github.com/thinkthoughts/sensors-becker.git"
)


@dataclass(slots=True)
class NotebookRuntime:
    """Initialized runtime shared by engineering notebooks."""

    repository_root: Path
    paths: RepositoryPaths
    context: RepositoryContext
    environment: str
    outputs: list[Path] = field(default_factory=list)

    def validate(self) -> None:
        """Validate the current engineering context."""

        validate_context(self.context)

    def export_context(self) -> tuple[Path, Path]:
        """Export the current engineering context."""

        paths = export_context_bundle(
            self.context,
            directory=self.paths.exports,
        )
        self._record(paths)
        return paths

    def export_figures(self) -> tuple[Path, Path]:
        """Export the default engineering figures."""

        paths = export_default_figures(
            self.context,
            directory=self.paths.figures,
        )
        self._record(paths)
        return paths

    def verify_outputs(self) -> tuple[Path, ...]:
        """Verify recorded outputs exist and contain data."""

        for path in self.outputs:
            if not path.exists():
                raise FileNotFoundError(f"Missing runtime output: {path}")
            if path.stat().st_size <= 0:
                raise ValueError(f"Runtime output is empty: {path}")

        return tuple(self.outputs)

    def relative_path(self, path: Path) -> Path:
        """Return a path relative to the runtime repository root."""

        return path.resolve().relative_to(self.repository_root.resolve())

    def _record(self, paths: tuple[Path, ...]) -> None:
        for path in paths:
            if path not in self.outputs:
                self.outputs.append(path)


def _in_colab() -> bool:
    """Return whether execution occurs in Google Colab."""

    return "google.colab" in sys.modules


def _find_repository_root(start: Path) -> Path:
    """Find a repository root containing pyproject.toml."""

    current = start.resolve()

    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate

    raise FileNotFoundError(
        "Could not locate repository root containing pyproject.toml"
    )


def _prepare_colab_repository(
    *,
    repository_url: str,
    destination: Path,
) -> Path:
    """Clone and install the repository in Google Colab."""

    if not destination.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                repository_url,
                str(destination),
            ],
            check=True,
        )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--quiet",
            "--editable",
            str(destination),
        ],
        check=True,
    )

    return destination.resolve()


def initialize_notebook(
    *,
    start: Path | None = None,
    context: RepositoryContext | None = None,
    repository_url: str = REPOSITORY_URL,
    colab_destination: Path = Path("/content/sensors-becker"),
) -> NotebookRuntime:
    """Initialize a validated notebook runtime.

    In Google Colab, the public repository is cloned and installed.
    In a local or VPS environment, the current repository is located
    from ``start`` or the active working directory.
    """

    if _in_colab():
        repository_root = _prepare_colab_repository(
            repository_url=repository_url,
            destination=colab_destination,
        )
        environment = "google-colab"
    else:
        repository_root = _find_repository_root(start or Path.cwd())
        environment = "repository-runtime"

    paths = paths_for_root(repository_root)
    paths.ensure_runtime_directories()

    repository_context = context or default_context()
    validate_context(repository_context)

    return NotebookRuntime(
        repository_root=repository_root,
        paths=paths,
        context=repository_context,
        environment=environment,
    )


__all__ = [
    "NotebookRuntime",
    "REPOSITORY_URL",
    "initialize_notebook",
]
