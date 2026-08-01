"""Figure utilities for the sensors-becker package."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from reading_point.context import RepositoryContext
from reading_point.paths import FIGURES_DIR
from reading_point.validation import validate_context


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


def _title_case_label(value: str) -> str:
    """Return a display label while preserving technical hyphenation."""

    return value.title()


def create_sequence_figure(
    items: Sequence[str],
    *,
    title: str,
    subtitle: str | None = None,
    current_item: str | None = None,
    figsize: tuple[float, float] = (8.0, 8.0),
) -> Figure:
    """Create a vertical sequence figure from ordered text items."""

    if not items:
        raise ValueError("items must contain at least one entry")

    figure, axis = plt.subplots(figsize=figsize)

    axis.set_xlim(0.0, 1.0)
    axis.set_ylim(-0.6, len(items) - 0.35)
    axis.axis("off")

    figure.suptitle(
        title,
        y=0.98,
        fontsize=16,
    )

    if subtitle:
        axis.set_title(
            subtitle,
            pad=14,
            fontsize=10,
        )

    y_positions = list(reversed(range(len(items))))

    for index, (item, y_position) in enumerate(
        zip(items, y_positions, strict=True)
    ):
        is_current = item == current_item

        axis.text(
            0.5,
            y_position,
            _title_case_label(item),
            ha="center",
            va="center",
            fontsize=11,
            bbox={
                "boxstyle": "round,pad=0.62",
                "facecolor": "white",
                "edgecolor": "black",
                "linewidth": 2.0 if is_current else 1.4,
            },
        )

        if is_current:
            axis.text(
                0.5,
                y_position - 0.34,
                "Current Specification",
                ha="center",
                va="top",
                fontsize=8,
            )

        if index < len(items) - 1:
            next_y_position = y_positions[index + 1]

            axis.annotate(
                "",
                xy=(0.5, next_y_position + 0.30),
                xytext=(0.5, y_position - 0.30),
                arrowprops={
                    "arrowstyle": "->",
                    "linewidth": 1.6,
                    "shrinkA": 0,
                    "shrinkB": 0,
                },
            )

    figure.tight_layout(rect=(0.03, 0.03, 0.97, 0.95))
    return figure


def create_engineering_object_figure(
    context: RepositoryContext,
) -> Figure:
    """Create the repository engineering-object sequence figure."""

    validate_context(context)

    return create_sequence_figure(
        context.object_sequence,
        title="Engineering Object Sequence",
        subtitle="Increasing Engineering Specification",
        current_item=context.current_specification,
        figsize=(8.0, 8.5),
    )


def create_engineering_cycle_figure(
    context: RepositoryContext,
    *,
    figsize: tuple[float, float] = (8.5, 9.0),
) -> Figure:
    """Create the engineering-development trail and continuation path."""

    validate_context(context)

    stages = (
        "Engineering Object",
        "Engineering System",
        "Measured Engineering States",
        "Engineering Constraints",
        "Leading Specifications",
        "Engineering Refinements",
        "Next Engineering Session",
    )

    figure, axis = plt.subplots(figsize=figsize)

    axis.set_xlim(0.0, 1.0)
    axis.set_ylim(-0.75, len(stages) - 0.15)
    axis.axis("off")

    figure.suptitle(
        "Engineering Development Cycle",
        y=0.985,
        fontsize=16,
    )

    axis.set_title(
        "Measured states connect the engineering system "
        "to continued refinement.",
        pad=12,
        fontsize=10,
    )

    y_positions = list(reversed(range(len(stages))))
    x_position = 0.46

    for index, (stage, y_position) in enumerate(
        zip(stages, y_positions, strict=True)
    ):
        is_leading_specification = stage == "Leading Specifications"
        is_next_session = stage == "Next Engineering Session"

        axis.text(
            x_position,
            y_position,
            stage,
            ha="center",
            va="center",
            fontsize=10.5,
            bbox={
                "boxstyle": "round,pad=0.58",
                "facecolor": "white",
                "edgecolor": "black",
                "linewidth": (
                    2.0
                    if is_leading_specification
                    else 1.4
                ),
                "linestyle": "--" if is_next_session else "-",
            },
        )

        if index < len(stages) - 1:
            next_y_position = y_positions[index + 1]

            axis.annotate(
                "",
                xy=(x_position, next_y_position + 0.30),
                xytext=(x_position, y_position - 0.30),
                arrowprops={
                    "arrowstyle": "->",
                    "linewidth": 1.6,
                    "shrinkA": 0,
                    "shrinkB": 0,
                },
            )

    first_y = y_positions[0]
    final_y = y_positions[-1]

    axis.annotate(
        "",
        xy=(x_position + 0.18, first_y),
        xytext=(x_position + 0.18, final_y),
        arrowprops={
            "arrowstyle": "->",
            "linewidth": 1.4,
            "connectionstyle": "arc3,rad=-0.34",
        },
    )

    axis.text(
        0.82,
        (first_y + final_y) / 2,
        "Continued Engineering Development",
        rotation=90,
        ha="center",
        va="center",
        fontsize=9,
    )

    axis.text(
        0.46,
        -0.48,
        context.footer,
        ha="center",
        va="center",
        fontsize=8,
        style="italic",
    )

    figure.tight_layout(rect=(0.04, 0.04, 0.96, 0.95))
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
