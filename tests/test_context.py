"""Figure utilities for the sensors-becker package."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.figure import Figure

from sensors_becker.context import RepositoryContext
from sensors_becker.paths import FIGURES_DIR
from sensors_becker.validation import validate_context


def ensure_figure_directory(directory: Path = FIGURES_DIR) -> Path:
    """Create and return the figure output directory."""

    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_figure(
    figure: Figure,
    filename: str,
    *,
    directory: Path = FIGURES_DIR,
    dpi: int = 200,
    close: bool = False,
) -> Path:
    """Save a Matplotlib figure and return the resulting path."""

    ensure_figure_directory(directory)
    path = directory / filename

    figure.savefig(
        path,
        dpi=dpi,
        bbox_inches="tight",
    )

    if close:
        plt.close(figure)

    return path


def create_sequence_figure(
    items: Sequence[str],
    *,
    title: str,
    figsize: tuple[float, float] = (8.0, 8.0),
) -> Figure:
    """Create a vertical sequence figure from ordered text items."""

    if not items:
        raise ValueError("items must contain at least one entry")

    figure, axis = plt.subplots(figsize=figsize)

    axis.set_xlim(0.0, 1.0)
    axis.set_ylim(-0.5, len(items) - 0.5)
    axis.axis("off")
    axis.set_title(title, pad=20)

    y_positions = list(reversed(range(len(items))))

    for index, (item, y_position) in enumerate(
        zip(items, y_positions, strict=True)
    ):
        axis.text(
            0.5,
            y_position,
            item,
            ha="center",
            va="center",
            bbox={
                "boxstyle": "round,pad=0.5",
                "facecolor": "white",
                "edgecolor": "black",
            },
        )

        if index < len(items) - 1:
            next_y_position = y_positions[index + 1]

            axis.annotate(
                "",
                xy=(0.5, next_y_position + 0.25),
                xytext=(0.5, y_position - 0.25),
                arrowprops={
                    "arrowstyle": "->",
                    "linewidth": 1.2,
                },
            )

    figure.tight_layout()
    return figure


def create_engineering_object_figure(
    context: RepositoryContext,
) -> Figure:
    """Create the repository engineering-object sequence figure."""

    validate_context(context)

    return create_sequence_figure(
        context.object_sequence,
        title="Engineering Object Sequence",
    )


def create_engineering_cycle_figure(
    context: RepositoryContext,
    *,
    figsize: tuple[float, float] = (9.0, 7.0),
) -> Figure:
    """Create a directed graph of the engineering development cycle."""

    validate_context(context)

    nodes = (
        "Engineering object",
        "Engineering system",
        "Measured engineering states",
        "Engineering constraints",
        "Engineering refinements",
        "Leading specifications",
    )

    graph = nx.DiGraph()

    graph.add_edges_from(
        zip(
            nodes,
            (*nodes[1:], nodes[0]),
            strict=True,
        )
    )

    figure, axis = plt.subplots(figsize=figsize)

    positions = nx.circular_layout(graph)

    nx.draw_networkx_nodes(
        graph,
        positions,
        ax=axis,
        node_size=3200,
    )
    nx.draw_networkx_edges(
        graph,
        positions,
        ax=axis,
        arrows=True,
        arrowsize=20,
        width=1.5,
    )
    nx.draw_networkx_labels(
        graph,
        positions,
        ax=axis,
        font_size=9,
    )

    axis.set_title(
        f"{context.repository}: Engineering Development Cycle",
        pad=20,
    )
    axis.axis("off")

    figure.tight_layout()
    return figure


def export_default_figures(
    context: RepositoryContext,
    *,
    directory: Path = FIGURES_DIR,
) -> tuple[Path, Path]:
    """Create and export the default Notebook 00 figures."""

    object_figure = create_engineering_object_figure(context)
    cycle_figure = create_engineering_cycle_figure(context)

    object_path = save_figure(
        object_figure,
        "engineering_object_sequence.png",
        directory=directory,
        close=True,
    )
    cycle_path = save_figure(
        cycle_figure,
        "engineering_development_cycle.png",
        directory=directory,
        close=True,
    )

    return object_path, cycle_path


__all__ = [
    "create_engineering_cycle_figure",
    "create_engineering_object_figure",
    "create_sequence_figure",
    "ensure_figure_directory",
    "export_default_figures",
    "save_figure",
]
