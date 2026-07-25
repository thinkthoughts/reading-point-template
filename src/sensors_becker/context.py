"""Engineering context models for the sensors-becker package."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final


DEFAULT_ENGINEERING_PATHS: Final[tuple[str, ...]] = (
    "hardware engineering",
    "software engineering",
    "experimental engineering",
)

DEFAULT_OBJECT_SEQUENCE: Final[tuple[str, ...]] = (
    "sensor development",
    "quantum sensing",
    "cryogenic sensing",
    "superconducting detectors",
    "transition-edge sensing",
    "microcalorimeter spectroscopy",
)


@dataclass(frozen=True, slots=True)
class RepositoryContext:
    """Typed engineering context for the sensors-becker repository."""

    repository: str = "sensors-becker"
    initiated: str = "2026-07"
    status: str = "developing"

    engineering_object: str = "sensor development"
    current_specification: str = "microcalorimeter spectroscopy"

    object_sequence: tuple[str, ...] = DEFAULT_OBJECT_SEQUENCE
    engineering_paths: tuple[str, ...] = DEFAULT_ENGINEERING_PATHS

    measured_engineering_states: tuple[str, ...] = (
        "sensor sensitivity",
        "energy resolution",
        "detector efficiency",
        "signal-to-noise ratio",
        "measurement repeatability",
        "calibration stability",
        "operating temperature",
        "detector response time",
        "readout performance",
        "system reliability",
    )

    engineering_constraints: tuple[str, ...] = field(default_factory=tuple)
    engineering_refinements: tuple[str, ...] = field(default_factory=tuple)

    leading_specification: str = (
        "Cryogenic quantum-sensor development connects hardware, "
        "software, and experimental engineering through measured "
        "engineering states, engineering constraints, and engineering "
        "refinements."
    )

    footer: str = (
        "Admissible generalizations trail leading specifications."
    )

    def as_dict(self) -> dict[str, object]:
        """Return the context as a serializable dictionary."""

        return {
            "repository": self.repository,
            "initiated": self.initiated,
            "status": self.status,
            "engineering_object": self.engineering_object,
            "current_specification": self.current_specification,
            "object_sequence": list(self.object_sequence),
            "engineering_paths": list(self.engineering_paths),
            "measured_engineering_states": list(
                self.measured_engineering_states
            ),
            "engineering_constraints": list(
                self.engineering_constraints
            ),
            "engineering_refinements": list(
                self.engineering_refinements
            ),
            "leading_specification": self.leading_specification,
            "footer": self.footer,
        }


def default_context() -> RepositoryContext:
    """Return the default repository engineering context."""

    return RepositoryContext()


__all__ = [
    "DEFAULT_ENGINEERING_PATHS",
    "DEFAULT_OBJECT_SEQUENCE",
    "RepositoryContext",
    "default_context",
]
