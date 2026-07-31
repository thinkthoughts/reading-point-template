from pathlib import Path
from .dialogue_specification import DialogueSpecification
class DialogueRenderer:
    def render(self,specification:DialogueSpecification,output_path:Path):
        raise NotImplementedError("Move the current NotebookDialogueRenderer implementation here.")
def render_dialogue(*,specification:DialogueSpecification,output_path:Path,renderer=None):
    renderer=renderer or DialogueRenderer()
    return renderer.render(specification,output_path)
