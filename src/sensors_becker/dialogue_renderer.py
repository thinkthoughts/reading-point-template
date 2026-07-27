from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


FOOTER = "Admissible generalizations trail leading specifications."
DEFAULT_SUBTITLE = "Toward next-generation microcalorimeters."

SEMANTIC_COLORS = {
    "primary": "#111111",
    "input": "#1f77b4",
    "coupling": "#ff7f0e",
    "output": "#2ca02c",
    "constraint": "#d62728",
    "support": "#7f7f7f",
}

LineStyle = Literal["solid", "dashed", "dotted", "dashdot"]


@dataclass(frozen=True)
class DialogueNode:
    """A named engineering noun placed in the notebook dialogue field."""

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
    """A semantic relationship between two positions in the dialogue field."""

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
class DialogueFigure:
    """Complete specification for one notebook dialogue realization."""

    title: str
    primary_nodes: tuple[DialogueNode, ...]
    primary_relations: tuple[DialogueRelation, ...] = field(default_factory=tuple)
    supporting_nodes: tuple[DialogueNode, ...] = field(default_factory=tuple)
    supporting_relations: tuple[DialogueRelation, ...] = field(default_factory=tuple)
    subtitle: str = DEFAULT_SUBTITLE
    footer: str = FOOTER


class NotebookDialogueRenderer:
    """Canonical renderer for notebook engineering-dialogue figures."""

    def __init__(
        self,
        *,
        figsize: tuple[float, float] = (12, 8),
        dpi: int = 180,
        semantic_colors: dict[str, str] | None = None,
        validate_layout: bool = True,
        overlap_tolerance: float = 0.002,
    ) -> None:
        self.figsize = figsize
        self.dpi = dpi
        self.validate_layout = validate_layout
        self.overlap_tolerance = overlap_tolerance
        self.semantic_colors = dict(SEMANTIC_COLORS)

        if semantic_colors:
            self.semantic_colors.update(semantic_colors)

    def render(self, figure_spec: DialogueFigure, output_path: Path) -> Path:
        """Render one admitted dialogue specification to a PNG."""

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if self.validate_layout:
            self._validate_figure(figure_spec)

        fig, ax = plt.subplots(figsize=self.figsize)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        self._draw_page_scaffold(ax, figure_spec)

        # Relations are drawn first. Nodes then cover line ends and prevent
        # connectors from crossing labels or appearing on top of boxes.
        for relation in figure_spec.supporting_relations:
            self._draw_relation(ax, relation)

        for relation in figure_spec.primary_relations:
            self._draw_relation(ax, relation)

        for node in figure_spec.supporting_nodes:
            self._draw_node(ax, node)

        for node in figure_spec.primary_nodes:
            self._draw_node(ax, node)

        fig.savefig(output_path, dpi=self.dpi, bbox_inches="tight")
        plt.close(fig)

        return output_path

    def _draw_page_scaffold(self, ax, figure_spec: DialogueFigure) -> None:
        ax.text(
            0.5,
            0.94,
            figure_spec.title,
            ha="center",
            va="center",
            fontsize=24,
            fontweight="bold",
        )
        ax.text(
            0.5,
            0.885,
            figure_spec.subtitle,
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
            0.17,
            "Supporting Context",
            ha="center",
            va="center",
            fontsize=12,
            fontweight="semibold",
        )
        ax.text(
            0.5,
            0.04,
            figure_spec.footer,
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
        color = self.semantic_colors[relation.role]
        linestyle = relation.line_style or ("dashed" if relation.dashed else "solid")

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

    def _fit_fontsize(self, node: DialogueNode) -> float:
        """Reduce long labels enough to remain inside their assigned box."""

        # Approximate character capacity from normalized box width.
        capacity = max(8.0, node.width * 48.0)
        ratio = capacity / max(len(node.label), 1)

        if ratio >= 1.0:
            return node.fontsize

        return max(10.0, node.fontsize * ratio)

    def _validate_figure(self, figure_spec: DialogueFigure) -> None:
        nodes = (*figure_spec.primary_nodes, *figure_spec.supporting_nodes)

        for node in nodes:
            self._validate_node_bounds(node)

        for index, first in enumerate(nodes):
            for second in nodes[index + 1 :]:
                if self._nodes_overlap(first, second):
                    raise ValueError(
                        "Dialogue nodes overlap: "
                        f"{first.label!r} and {second.label!r}. "
                        "Move the supporting node, reduce its width, or use a "
                        "different supporting-context slot."
                    )

        for relation in (
            *figure_spec.primary_relations,
            *figure_spec.supporting_relations,
        ):
            if relation.role not in self.semantic_colors:
                raise ValueError(f"Unknown relation role: {relation.role!r}")

    def _validate_node_bounds(self, node: DialogueNode) -> None:
        left = node.x - node.width / 2
        right = node.x + node.width / 2
        bottom = node.y - node.height / 2
        top = node.y + node.height / 2

        if left < 0 or right > 1 or bottom < 0 or top > 1:
            raise ValueError(
                f"Dialogue node {node.label!r} extends outside the figure bounds."
            )

    def _nodes_overlap(self, first: DialogueNode, second: DialogueNode) -> bool:
        tolerance = self.overlap_tolerance

        first_left = first.x - first.width / 2 + tolerance
        first_right = first.x + first.width / 2 - tolerance
        first_bottom = first.y - first.height / 2 + tolerance
        first_top = first.y + first.height / 2 - tolerance

        second_left = second.x - second.width / 2 + tolerance
        second_right = second.x + second.width / 2 - tolerance
        second_bottom = second.y - second.height / 2 + tolerance
        second_top = second.y + second.height / 2 - tolerance

        horizontal_overlap = first_left < second_right and second_left < first_right
        vertical_overlap = first_bottom < second_top and second_bottom < first_top

        return horizontal_overlap and vertical_overlap


def render_dialogue(
    *,
    figure_spec: DialogueFigure,
    output_path: Path,
    renderer: NotebookDialogueRenderer | None = None,
) -> Path:
    """Convenience function for notebook use."""

    active_renderer = renderer or NotebookDialogueRenderer()
    return active_renderer.render(figure_spec, output_path)
