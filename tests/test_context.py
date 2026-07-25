"""Tests for the sensors-becker engineering context."""

from __future__ import annotations

import json

import yaml

from sensors_becker.context import RepositoryContext, default_context
from sensors_becker.export import export_context_bundle
from sensors_becker.figures import export_default_figures
from sensors_becker.validation import (
    ContextValidationError,
    validate_context,
)


def test_default_context_validates() -> None:
    """The default repository context should pass validation."""

    context = default_context()

    validate_context(context)


def test_default_context_identity() -> None:
    """The default context should preserve repository identity."""

    context = default_context()

    assert context.repository == "sensors-becker"
    assert context.engineering_object == "sensor development"
    assert context.current_specification == "microcalorimeter spectroscopy"


def test_object_sequence_relationships() -> None:
    """The object sequence should contain its broad and current objects."""

    context = default_context()

    assert context.object_sequence[0] == context.engineering_object
    assert context.current_specification in context.object_sequence


def test_context_as_dict_is_serializable() -> None:
    """The context dictionary should support JSON serialization."""

    context = default_context()
    data = context.as_dict()

    encoded = json.dumps(data)

    assert encoded
    assert data["repository"] == "sensors-becker"
    assert isinstance(data["object_sequence"], list)


def test_invalid_current_specification_fails() -> None:
    """A current specification outside the object sequence should fail."""

    context = RepositoryContext(
        current_specification="unsupported sensor specification"
    )

    try:
        validate_context(context)
    except ContextValidationError as error:
        assert "current_specification" in str(error)
    else:
        raise AssertionError(
            "validate_context should reject an unsupported specification"
        )


def test_context_bundle_exports_json_and_yaml(tmp_path) -> None:
    """The context bundle should export matching JSON and YAML files."""

    context = default_context()

    json_path, yaml_path = export_context_bundle(
        context,
        directory=tmp_path,
    )

    assert json_path.exists()
    assert yaml_path.exists()

    json_data = json.loads(json_path.read_text(encoding="utf-8"))
    yaml_data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))

    assert json_data == yaml_data
    assert json_data["repository"] == "sensors-becker"


def test_default_figures_export(tmp_path) -> None:
    """The default engineering figures should export successfully."""

    context = default_context()

    object_path, cycle_path = export_default_figures(
        context,
        directory=tmp_path,
    )

    assert object_path.exists()
    assert cycle_path.exists()
    assert object_path.stat().st_size > 0
    assert cycle_path.stat().st_size > 0
