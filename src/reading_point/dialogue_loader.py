from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import yaml

from .dialogue_specification import (
    DEFAULT_SUBTITLE,
    FOOTER,
    DialogueNode,
    DialogueRelation,
    DialogueSpecification,
)


def _mapping(value: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{context} must be a mapping")
    return value


def _pair(value: Any, context: str) -> tuple[float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"{context} must contain exactly two values")
    return float(value[0]), float(value[1])


def _node(value: Any, context: str) -> DialogueNode:
    item = _mapping(value, context)
    return DialogueNode(
        label=str(item["label"]),
        x=float(item["x"]),
        y=float(item["y"]),
        width=float(item["width"]),
        height=float(item["height"]),
        role=str(item.get("role", "support")),
        emphasis=bool(item.get("emphasis", False)),
        fontsize=float(item.get("fontsize", 16)),
        zorder=int(item.get("zorder", 3)),
    )


def _relation(value: Any, context: str) -> DialogueRelation:
    item = _mapping(value, context)
    return DialogueRelation(
        start=_pair(item["start"], f"{context}.start"),
        end=_pair(item["end"], f"{context}.end"),
        role=str(item["role"]),
        directional=bool(item.get("directional", False)),
        dashed=bool(item.get("dashed", False)),
        line_style=item.get("line_style"),
        linewidth=float(item.get("linewidth", 1.8)),
        alpha=float(item.get("alpha", 1.0)),
        curvature=float(item.get("curvature", 0.0)),
        zorder=int(item.get("zorder", 1)),
    )


def dialogue_from_mapping(
    value: Mapping[str, Any],
) -> DialogueSpecification:
    """Build a renderer-level DialogueSpecification from a mapping."""

    item = _mapping(value, "dialogue specification")

    primary_nodes = tuple(
        _node(node, f"primary_nodes[{index}]")
        for index, node in enumerate(item.get("primary_nodes", ()))
    )
    if not primary_nodes:
        raise ValueError("primary_nodes must contain at least one node")

    return DialogueSpecification(
        title=str(item["title"]),
        subtitle=str(item.get("subtitle", DEFAULT_SUBTITLE)),
        footer=str(item.get("footer", FOOTER)),
        primary_nodes=primary_nodes,
        primary_relations=tuple(
            _relation(relation, f"primary_relations[{index}]")
            for index, relation in enumerate(
                item.get("primary_relations", ())
            )
        ),
        supporting_nodes=tuple(
            _node(node, f"supporting_nodes[{index}]")
            for index, node in enumerate(
                item.get("supporting_nodes", ())
            )
        ),
        supporting_relations=tuple(
            _relation(relation, f"supporting_relations[{index}]")
            for index, relation in enumerate(
                item.get("supporting_relations", ())
            )
        ),
        supporting_context=tuple(
            str(label) for label in item.get("supporting_context", ())
        ),
    )


def reading_point_dialogue_from_mapping(
    value: Mapping[str, Any],
    *,
    engineering_object: str = "Engineering Object",
    engineering_direction: str = DEFAULT_SUBTITLE,
    footer: str = FOOTER,
) -> DialogueSpecification:
    """Build the canonical two-node figure from one RP dialogue entry."""

    item = _mapping(value, "reading-point dialogue")

    concept = str(item["concept"])
    first_label = str(item["first_label"])
    second_label = str(item["second_label"])

    title = str(
        item.get(
            "title",
            f"{concept} Trail: {engineering_object}s",
        )
    )

    return DialogueSpecification(
        title=title,
        subtitle=engineering_direction,
        footer=footer,
        primary_nodes=(
            DialogueNode(
                label=first_label,
                x=0.5,
                y=0.67,
                width=0.42,
                height=0.10,
                role="input",
            ),
            DialogueNode(
                label=second_label,
                x=0.5,
                y=0.46,
                width=0.42,
                height=0.12,
                role="primary",
                emphasis=True,
            ),
        ),
        primary_relations=(
            DialogueRelation(
                start=(0.5, 0.62),
                end=(0.5, 0.52),
                role="input",
                directional=True,
            ),
        ),
        supporting_context=tuple(
            str(label)
            for label in item.get("supporting_context", ())
        ),
    )


def load_dialogue(
    path: str | Path,
    *,
    dialogue_index: int | None = None,
) -> DialogueSpecification:
    """Load renderer-level YAML or one dialogue from an RP YAML file."""

    source_path = Path(path)
    data = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    root = _mapping(data, str(source_path))

    if "primary_nodes" in root:
        return dialogue_from_mapping(root)

    dialogues = root.get("dialogue")
    if not isinstance(dialogues, list) or not dialogues:
        raise ValueError(
            "YAML must be a renderer-level specification or contain "
            "a non-empty dialogue list"
        )

    if dialogue_index is None:
        if len(dialogues) != 1:
            raise ValueError(
                "dialogue_index is required when the RP YAML contains "
                "more than one dialogue"
            )
        dialogue_index = 0

    try:
        dialogue = dialogues[dialogue_index]
    except IndexError as exc:
        raise IndexError(
            f"dialogue_index {dialogue_index} is outside the dialogue list"
        ) from exc

    return reading_point_dialogue_from_mapping(
        dialogue,
        engineering_object=str(
            root.get("engineering_object", "Engineering Object")
        ),
        engineering_direction=str(
            root.get("engineering_direction", DEFAULT_SUBTITLE)
        ),
        footer=str(root.get("footer", FOOTER)),
    )


__all__ = [
    "dialogue_from_mapping",
    "reading_point_dialogue_from_mapping",
    "load_dialogue",
]
