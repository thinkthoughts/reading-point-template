"""Validation utilities for the sensors-becker engineering context."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import fields
from typing import Final

from sensors_becker.context import RepositoryContext


class ContextValidationError(ValueError):
    """Raised where a repository engineering context fails validation."""


REQUIRED_TEXT_FIELDS: Final[tuple[str, ...]] = (
    "repository",
    "initiated",
    "status",
    "engineering_object",
    "current_specification",
    "leading_specification",
    "footer",
)

REQUIRED_SEQUENCE_FIELDS: Final[tuple[str, ...]] = (
    "object_sequence",
    "engineering_paths",
    "measured_engineering_states",
    "engineering_constraints",
    "engineering_refinements",
)


def _validate_nonempty_text(name: str, value: object) -> None:
    if not isinstance(value, str):
        raise ContextValidationError(f"{name} must be a string")
    if not value.strip():
        raise ContextValidationError(f"{name} must contain text")


def _validate_string_tuple(
    name: str,
    value: object,
    *,
    allow_empty: bool,
) -> None:
    if not isinstance(value, tuple):
        raise ContextValidationError(f"{name} must be a tuple")
    if not allow_empty and not value:
        raise ContextValidationError(f"{name} must contain at least one item")

    normalized_items: list[str] = []

    for index, item in enumerate(value):
        if not isinstance(item, str):
            raise ContextValidationError(f"{name}[{index}] must be a string")

        normalized = item.strip()
        if not normalized:
            raise ContextValidationError(f"{name}[{index}] must contain text")

        normalized_items.append(normalized)

    if len(normalized_items) != len(set(normalized_items)):
        raise ContextValidationError(f"{name} must contain unique items")


def _validate_object_sequence(context: RepositoryContext) -> None:
    sequence = context.object_sequence

    if sequence[0] != context.engineering_object:
        raise ContextValidationError(
            "object_sequence must begin with engineering_object"
        )

    if context.current_specification not in sequence:
        raise ContextValidationError(
            "current_specification must appear in object_sequence"
        )


def _validate_repository_name(repository: str) -> None:
    allowed_characters = set("abcdefghijklmnopqrstuvwxyz0123456789-_")

    if any(character not in allowed_characters for character in repository):
        raise ContextValidationError(
            "repository may contain lowercase letters, digits, hyphens, "
            "and underscores only"
        )


def _validate_known_fields(context: RepositoryContext) -> None:
    available_fields = {field.name for field in fields(context)}
    expected_fields = set(REQUIRED_TEXT_FIELDS) | set(REQUIRED_SEQUENCE_FIELDS)
    missing_fields = expected_fields - available_fields

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ContextValidationError(
            f"context is missing required fields: {missing}"
        )


def validate_context(context: RepositoryContext) -> None:
    """Validate a repository engineering context."""

    if not isinstance(context, RepositoryContext):
        raise TypeError("context must be a RepositoryContext instance")

    _validate_known_fields(context)

    for name in REQUIRED_TEXT_FIELDS:
        _validate_nonempty_text(name, getattr(context, name))

    for name in REQUIRED_SEQUENCE_FIELDS:
        _validate_string_tuple(
            name,
            getattr(context, name),
            allow_empty=name
            in {"engineering_constraints", "engineering_refinements"},
        )

    _validate_repository_name(context.repository)
    _validate_object_sequence(context)


def validated_context(context: RepositoryContext) -> RepositoryContext:
    """Validate and return an engineering context."""

    validate_context(context)
    return context


def validate_text_items(
    values: Iterable[str],
    *,
    name: str = "values",
    allow_empty: bool = False,
) -> tuple[str, ...]:
    """Normalize and validate an iterable of text items."""

    normalized = tuple(value.strip() for value in values)
    _validate_string_tuple(name, normalized, allow_empty=allow_empty)
    return normalized


__all__ = [
    "ContextValidationError",
    "REQUIRED_SEQUENCE_FIELDS",
    "REQUIRED_TEXT_FIELDS",
    "validate_context",
    "validate_text_items",
    "validated_context",
]
