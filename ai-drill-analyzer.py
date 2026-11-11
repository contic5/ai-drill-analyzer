import pandas as pd
from openai import OpenAI
import json

from typing import Literal
from pydantic import BaseModel, Field

import textwrap
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class DrillAnalysisModel(BaseModel):
    Learning_Potential:Literal[1,2,3,4,5,6,7,8,9,10] = Field(description="Rating from 1 to 10")
    Physical_Development:Literal[1,2,3,4,5,6,7,8,9,10] = Field(description="Rating from 1 to 10")
    Fun:Literal[1,2,3,4,5,6,7,8,9,10] = Field(description="Rating from 1 to 10")
    Reasoning:str=Field("The reasoning behind the learning_potential, physical_development and fun scores.")

def main():
    drill_df=pd.read_excel("data/Drills.xlsx",sheet_name="Drills")
    analysis_arr=[]

    for index,row in drill_df.iterrows():
        #Do not send self defense drills to ChatGPT. Unsure about sending how to defend yourself from a weapon to AI.
        if "SELF" in str(row["Category"]).upper() or "DEFENSE" in str(row["Category"]).upper():
            continue

        client = OpenAI()

        drill=row["Name"]
        category=row["Category"]
        ranks=row["Ranks"]
        steps=row["Steps"]

        prompt=f'''
        Analyze the following drill. 

        The Drill
        Drill Name: {drill}
        Curricumum: {category}
        Target Ranks: {ranks}
        Steps: {steps}
        '''

        prompt=textwrap.dedent(prompt)

        print(prompt)

        response = client.responses.parse(
            model="gpt-6-luna",
            input=prompt,
            text_format=DrillAnalysisModel,
        )

        print(response)
        print(response.output_text)
        response_dict=json.loads(response.output_text)

        row_dict=row.to_dict()

        #Merge row data and response data
        analysis_dict=row_dict | response_dict
        analysis_arr.append(analysis_dict)
        break

    analysis_df=pd.DataFrame.from_dict(analysis_arr)
    print(analysis_df.head())

    analysis_df.to_excel("results/Analyzed Drills.xlsx")


if __name__=="__main__":
    main()