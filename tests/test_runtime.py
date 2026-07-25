"""Tests for the sensors-becker notebook runtime."""

from __future__ import annotations

from sensors_becker.runtime import initialize_notebook


def test_initialize_notebook(tmp_path) -> None:
    """A repository runtime should initialize from an explicit root."""

    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = \"runtime-test\"\nversion = \"0.0.0\"\n",
        encoding="utf-8",
    )

    runtime = initialize_notebook(start=tmp_path)

    assert runtime.repository_root == tmp_path.resolve()
    assert runtime.environment == "repository-runtime"
    assert runtime.context.repository == "sensors-becker"

    for directory in runtime.paths.runtime_directories():
        assert directory.exists()


def test_runtime_exports_and_verifies(tmp_path) -> None:
    """Runtime exports should be recorded and verified."""

    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = \"runtime-test\"\nversion = \"0.0.0\"\n",
        encoding="utf-8",
    )

    runtime = initialize_notebook(start=tmp_path)

    context_paths = runtime.export_context()
    figure_paths = runtime.export_figures()
    verified = runtime.verify_outputs()

    assert verified == (*context_paths, *figure_paths)
