"""Public package interface for sensors-becker."""

from .context import RepositoryContext, build_context
from .dialogue_renderer import (
    DialogueFigure,
    DialogueNode,
    DialogueRelation,
    NotebookDialogueRenderer,
    render_dialogue,
)
from .runtime import NotebookRuntime, initialize_notebook
from .validation import (
    ContextValidationError,
    validate_context,
)

__all__ = [
    "ContextValidationError",
    "DialogueFigure",
    "DialogueNode",
    "DialogueRelation",
    "NotebookDialogueRenderer",
    "NotebookRuntime",
    "RepositoryContext",
    "build_context",
    "initialize_notebook",
    "render_dialogue",
    "validate_context",
]
