from typing import Literal
from pydantic import BaseModel, Field

class DrillAnalysisModel(BaseModel):
    Learning_Potential:Literal[1,2,3,4,5,6,7,8,9,10] = Field(description="Rating from 1 to 10")
    Physical_Development:Literal[1,2,3,4,5,6,7,8,9,10] = Field(description="Rating from 1 to 10")
    Fun:Literal[1,2,3,4,5,6,7,8,9,10] = Field(description="Rating from 1 to 10")
    Reasoning:str=Field("The reasoning behind the learning_potential, physical_development and fun scores.")
    Advice:str=Field("Advice on how to improve the drill")