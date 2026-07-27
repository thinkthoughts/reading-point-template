from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

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


@dataclass(frozen=True)
class DialogueRelation:
    """A semantic relationship between two positions in the dialogue field."""

    start: tuple[float, float]
    end: tuple[float, float]
    role: str
    directional: bool = False
    dashed: bool = False


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
    ) -> None:
        self.figsize = figsize
        self.dpi = dpi
        self.semantic_colors = dict(SEMANTIC_COLORS)
        if semantic_colors:
            self.semantic_colors.update(semantic_colors)

    def render(self, figure_spec: DialogueFigure, output_path: Path) -> Path:
        """Render one admitted dialogue specification to a PNG."""

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots(figsize=self.figsize)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        self._draw_page_scaffold(ax, figure_spec)

        for node in figure_spec.primary_nodes:
            self._draw_node(ax, node)

        for relation in figure_spec.primary_relations:
            self._draw_relation(ax, relation)

        for node in figure_spec.supporting_nodes:
            self._draw_node(ax, node)

        for relation in figure_spec.supporting_relations:
            self._draw_relation(ax, relation)

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
        )
        ax.add_patch(patch)
        ax.text(
            node.x,
            node.y,
            node.label,
            ha="center",
            va="center",
            fontsize=node.fontsize,
            fontweight="bold" if node.emphasis else "semibold",
        )

    def _draw_relation(self, ax, relation: DialogueRelation) -> None:
        color = self.semantic_colors[relation.role]
        ax.annotate(
            "",
            xy=relation.end,
            xytext=relation.start,
            arrowprops={
                "arrowstyle": "->" if relation.directional else "-",
                "linewidth": 1.8,
                "linestyle": "--" if relation.dashed else "-",
                "color": color,
            },
        )


def render_dialogue(
    *,
    figure_spec: DialogueFigure,
    output_path: Path,
    renderer: NotebookDialogueRenderer | None = None,
) -> Path:
    """Convenience function for notebook use."""

    active_renderer = renderer or NotebookDialogueRenderer()
    return active_renderer.render(figure_spec, output_path)
