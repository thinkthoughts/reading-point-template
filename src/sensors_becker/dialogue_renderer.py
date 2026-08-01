from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from .dialogue_specification import (
    DialogueFigure,
    DialogueNode,
    DialogueRelation,
    DialogueSpecification,
)


SEMANTIC_COLORS = {
    "primary": "#111111",
    "input": "#1f77b4",
    "coupling": "#ff7f0e",
    "output": "#2ca02c",
    "constraint": "#d62728",
    "support": "#7f7f7f",
}


class DialogueRenderer:
    """Canonical renderer for engineering-dialogue figures.

    This class preserves the validated layout and rendering behavior of the
    former NotebookDialogueRenderer while removing notebook-specific identity
    from the implementation.
    """

    def __init__(
        self,
        *,
        figsize: tuple[float, float] = (12, 8),
        dpi: int = 180,
        semantic_colors: dict[str, str] | None = None,
        validate_layout: bool = True,
        overlap_tolerance: float = 0.002,
        support_box_width: float = 0.30,
        support_box_height: float = 0.07,
    ) -> None:
        self.figsize = figsize
        self.dpi = dpi
        self.validate_layout = validate_layout
        self.overlap_tolerance = overlap_tolerance
        self.support_box_width = support_box_width
        self.support_box_height = support_box_height
        self.semantic_colors = dict(SEMANTIC_COLORS)

        if semantic_colors:
            self.semantic_colors.update(semantic_colors)

    def render(
        self,
        specification: DialogueSpecification,
        output_path: Path,
    ) -> Path:
        """Render one dialogue specification to a PNG."""

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        resolved_supporting_nodes = self._resolve_supporting_nodes(specification)

        if self.validate_layout:
            self._validate_figure(
                specification,
                supporting_nodes=resolved_supporting_nodes,
            )

        fig, ax = plt.subplots(figsize=self.figsize)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        self._draw_page_scaffold(ax, specification)

        # Relations render first so node boxes cover endpoints cleanly.
        for relation in specification.supporting_relations:
            self._draw_relation(ax, relation)

        for relation in specification.primary_relations:
            self._draw_relation(ax, relation)

        for node in resolved_supporting_nodes:
            self._draw_node(ax, node)

        for node in specification.primary_nodes:
            self._draw_node(ax, node)

        fig.savefig(output_path, dpi=self.dpi, bbox_inches="tight")
        plt.close(fig)

        return output_path

    def _draw_page_scaffold(
        self,
        ax,
        specification: DialogueSpecification,
    ) -> None:
        """Draw the fixed page rhythm."""

        ax.text(
            0.5,
            0.94,
            specification.title,
            ha="center",
            va="center",
            fontsize=24,
            fontweight="bold",
        )
        ax.text(
            0.5,
            0.885,
            specification.subtitle,
            ha="center",
            va="center",
            fontsize=15,
            style="italic",
        )
        ax.text(
            0.5,
            0.80,
            "Primary Dialogue",
            ha="center",
            va="center",
            fontsize=13,
            fontweight="semibold",
        )

        ax.text(
            0.5,
            0.155,
            "Supporting Context",
            ha="center",
            va="center",
            fontsize=12,
            fontweight="semibold",
        )

        ax.text(
            0.5,
            0.025,
            specification.footer,
            ha="center",
            va="center",
            fontsize=13,
            style="italic",
        )

    def _draw_node(self, ax, node: DialogueNode) -> None:
        linewidth = 3.0 if node.emphasis else 1.8

        patch = FancyBboxPatch(
            (node.x - node.width / 2, node.y - node.height / 2),
            node.width,
            node.height,
            boxstyle="round,pad=0.012,rounding_size=0.025",
            facecolor="white",
            edgecolor=self.semantic_colors["primary"],
            linewidth=linewidth,
            zorder=node.zorder,
        )
        ax.add_patch(patch)

        ax.text(
            node.x,
            node.y,
            node.label,
            ha="center",
            va="center",
            fontsize=self._fit_fontsize(node),
            fontweight="bold" if node.emphasis else "semibold",
            zorder=node.zorder + 1,
        )

    def _draw_relation(self, ax, relation: DialogueRelation) -> None:
        try:
            color = self.semantic_colors[relation.role]
        except KeyError as exc:
            raise ValueError(
                f"Unknown relation role: {relation.role!r}"
            ) from exc

        linestyle = relation.line_style or (
            "dashed" if relation.dashed else "solid"
        )

        ax.annotate(
            "",
            xy=relation.end,
            xytext=relation.start,
            zorder=relation.zorder,
            arrowprops={
                "arrowstyle": "->" if relation.directional else "-",
                "linewidth": relation.linewidth,
                "linestyle": linestyle,
                "color": color,
                "alpha": relation.alpha,
                "connectionstyle": f"arc3,rad={relation.curvature}",
                "shrinkA": 0,
                "shrinkB": 0,
            },
        )

    def _resolve_supporting_nodes(
        self,
        specification: DialogueSpecification,
    ) -> tuple[DialogueNode, ...]:
        """Resolve the noun-only support API into fixed slots."""

        if specification.supporting_context and specification.supporting_nodes:
            raise ValueError(
                "Use either supporting_context or supporting_nodes, not both."
            )

        if specification.supporting_nodes:
            return specification.supporting_nodes

        labels = specification.supporting_context

        if not labels:
            return ()

        if len(labels) > 3:
            raise ValueError(
                "DialogueRenderer supports at most three "
                "supporting-context nouns per figure."
            )

        slots = self._support_slots(len(labels))

        return tuple(
            DialogueNode(
                label=label,
                x=x,
                y=0.09,
                width=self.support_box_width,
                height=self.support_box_height,
                role="support",
                fontsize=14,
            )
            for label, x in zip(labels, slots)
        )

    @staticmethod
    def _support_slots(count: int) -> tuple[float, ...]:
        """Return canonical equal-width support slots."""

        if count == 1:
            return (0.5,)
        if count == 2:
            return (0.30, 0.70)
        if count == 3:
            return (0.18, 0.50, 0.82)

        return ()

    def _fit_fontsize(self, node: DialogueNode) -> float:
        """Reduce long labels enough to remain inside equal-width boxes."""

        capacity = max(8.0, node.width * 48.0)
        ratio = capacity / max(len(node.label), 1)

        if ratio >= 1.0:
            return node.fontsize

        return max(10.0, node.fontsize * ratio)

    def _validate_figure(
        self,
        specification: DialogueSpecification,
        *,
        supporting_nodes: Sequence[DialogueNode],
    ) -> None:
        nodes = (*specification.primary_nodes, *supporting_nodes)

        for node in nodes:
            self._validate_node_bounds(node)

        for index, first in enumerate(nodes):
            for second in nodes[index + 1 :]:
                if self._nodes_overlap(first, second):
                    raise ValueError(
                        "Dialogue nodes overlap: "
                        f"{first.label!r} and {second.label!r}. "
                        "Move the primary node, reduce its dimensions, or "
                        "use the canonical supporting_context API."
                    )

        for relation in (
            *specification.primary_relations,
            *specification.supporting_relations,
        ):
            if relation.role not in self.semantic_colors:
                raise ValueError(
                    f"Unknown relation role: {relation.role!r}"
                )

    def _validate_node_bounds(self, node: DialogueNode) -> None:
        left = node.x - node.width / 2
        right = node.x + node.width / 2
        bottom = node.y - node.height / 2
        top = node.y + node.height / 2

        if left < 0 or right > 1 or bottom < 0 or top > 1:
            raise ValueError(
                f"Dialogue node {node.label!r} extends outside figure bounds."
            )

    def _nodes_overlap(
        self,
        first: DialogueNode,
        second: DialogueNode,
    ) -> bool:
        tolerance = self.overlap_tolerance

        first_left = first.x - first.width / 2 + tolerance
        first_right = first.x + first.width / 2 - tolerance
        first_bottom = first.y - first.height / 2 + tolerance
        first_top = first.y + first.height / 2 - tolerance

        second_left = second.x - second.width / 2 + tolerance
        second_right = second.x + second.width / 2 - tolerance
        second_bottom = second.y - second.height / 2 + tolerance
        second_top = second.y + second.height / 2 - tolerance

        horizontal_overlap = (
            first_left < second_right and second_left < first_right
        )
        vertical_overlap = (
            first_bottom < second_top and second_bottom < first_top
        )

        return horizontal_overlap and vertical_overlap


# Compatibility class name for existing notebooks.
NotebookDialogueRenderer = DialogueRenderer


def render_dialogue(
    *,
    specification: DialogueSpecification | None = None,
    figure_spec: DialogueFigure | None = None,
    output_path: Path,
    renderer: DialogueRenderer | None = None,
) -> Path:
    """Render a dialogue using the new or compatibility argument name."""

    active_specification = specification or figure_spec
    if active_specification is None:
        raise TypeError(
            "render_dialogue requires specification= or figure_spec="
        )

    active_renderer = renderer or DialogueRenderer()
    return active_renderer.render(active_specification, output_path)


__all__ = [
    "SEMANTIC_COLORS",
    "DialogueRenderer",
    "NotebookDialogueRenderer",
    "render_dialogue",
]
