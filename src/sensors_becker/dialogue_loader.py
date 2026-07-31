from pathlib import Path
from .dialogue_specification import DialogueSpecification
def load_dialogue(path:str|Path)->DialogueSpecification:
    raise NotImplementedError("Implement YAML loading after renderer migration.")
