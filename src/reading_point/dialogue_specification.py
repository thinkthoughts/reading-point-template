from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


FOOTER = "Admissible generalizations trail leading specifications."
DEFAULT_SUBTITLE = "Toward engineering specifications."

LineStyle = Literal["solid", "dashed", "dotted", "dashdot"]


@dataclass(frozen=True)
class DialogueNode:
    """A named engineering noun placed in a dialogue field."""

    label: str
    x: float
    y: float
    width: float
    height: float
    role: str = "support"
    emphasis: bool = False
    fontsize: float = 16
    zorder: int = 3


@dataclass(frozen=True)
class DialogueRelation:
    """A semantic relationship between two positions in a dialogue field."""

    start: tuple[float, float]
    end: tuple[float, float]
    role: str
    directional: bool = False
    dashed: bool = False
    line_style: LineStyle | None = None
    linewidth: float = 1.8
    alpha: float = 1.0
    curvature: float = 0.0
    zorder: int = 1


@dataclass(frozen=True)
class DialogueSpecification:
    """Complete specification for one engineering-dialogue realization."""

    title: str
    primary_nodes: tuple[DialogueNode, ...]
    primary_relations: tuple[DialogueRelation, ...] = field(default_factory=tuple)

    # Explicit layout controls for specialized figures.
    supporting_nodes: tuple[DialogueNode, ...] = field(default_factory=tuple)
    supporting_relations: tuple[DialogueRelation, ...] = field(default_factory=tuple)

    # Preferred API: nouns only; the renderer owns support placement.
    supporting_context: tuple[str, ...] = field(default_factory=tuple)

    subtitle: str = DEFAULT_SUBTITLE
    footer: str = FOOTER


# Compatibility name for notebooks generated before the package refactor.
DialogueFigure = DialogueSpecification


__all__ = [
    "FOOTER",
    "DEFAULT_SUBTITLE",
    "LineStyle",
    "DialogueNode",
    "DialogueRelation",
    "DialogueSpecification",
    "DialogueFigure",
]
