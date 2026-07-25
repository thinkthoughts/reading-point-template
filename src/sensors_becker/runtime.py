"""Notebook runtime coordination for the sensors-becker package."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from sensors_becker.context import RepositoryContext, default_context
from sensors_becker.export import export_context_bundle
from sensors_becker.figures import export_default_figures
from sensors_becker.paths import RepositoryPaths, paths_for_root
from sensors_becker.validation import validate_context


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

        exported_paths = export_context_bundle(
            self.context,
            directory=self.paths.exports,
        )
        self._record(exported_paths)
        return exported_paths

    def export_figures(self) -> tuple[Path, Path]:
        """Export the default engineering figures."""

        exported_paths = export_default_figures(
            self.context,
            directory=self.paths.figures,
        )
        self._record(exported_paths)
        return exported_paths

    def verify_outputs(self) -> tuple[Path, ...]:
        """Verify that recorded outputs exist and contain data."""

        for path in self.outputs:
            if not path.exists():
                raise FileNotFoundError(
                    f"Missing runtime output: {path}"
                )

            if path.stat().st_size <= 0:
                raise ValueError(
                    f"Runtime output is empty: {path}"
                )

        return tuple(self.outputs)

    def relative_path(self, path: Path) -> Path:
        """Return a path relative to the runtime repository root."""

        return path.resolve().relative_to(
            self.repository_root.resolve()
        )

    def _record(self, paths: tuple[Path, ...]) -> None:
        """Record output paths once, preserving creation order."""

        for path in paths:
            if path not in self.outputs:
                self.outputs.append(path)


def find_repository_root(start: Path) -> Path:
    """Find a repository root containing pyproject.toml."""

    current = start.resolve()

    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate

    raise FileNotFoundError(
        "Could not locate repository root containing pyproject.toml"
    )


def initialize_notebook(
    *,
    start: Path | None = None,
    context: RepositoryContext | None = None,
    environment: str = "repository-runtime",
) -> NotebookRuntime:
    """Initialize a validated engineering-notebook runtime.

    The package must already be installed or otherwise importable.

    For Google Colab, run the notebook bootstrap cell first so the
    repository package is installed before calling this function.
    """

    repository_root = find_repository_root(
        start or Path.cwd()
    )

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
    "find_repository_root",
    "initialize_notebook",
]
