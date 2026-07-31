from dataclasses import dataclass, field
from typing import Literal
LineStyle=Literal["solid","dashed","dotted","dashdot"]
@dataclass(frozen=True)
class DialogueNode:
    label:str; x:float; y:float; width:float; height:float
    role:str="support"; emphasis:bool=False; fontsize:float=16; zorder:int=3
@dataclass(frozen=True)
class DialogueRelation:
    start:tuple[float,float]; end:tuple[float,float]; role:str
@dataclass(frozen=True)
class DialogueSpecification:
    title:str
    primary_nodes:tuple[DialogueNode,...]
    primary_relations:tuple[DialogueRelation,...]=field(default_factory=tuple)
    supporting_nodes:tuple[DialogueNode,...]=field(default_factory=tuple)
    supporting_relations:tuple[DialogueRelation,...]=field(default_factory=tuple)
    supporting_context:tuple[str,...]=field(default_factory=tuple)
    subtitle:str="Toward engineering specifications."
    footer:str="Admissible generalizations trail leading specifications."
