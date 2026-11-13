import pandas as pd
from openai import OpenAI
import json
import textwrap
from drill_analysis_model import DrillAnalysisModel
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


force_overwrite=True

def prepare_prompt(row:pd.Series):
    drill=row["Name"]
    category=row["Category"]
    ranks=row["Ranks"]
    steps=row["Steps"]
    instructor_focus=row["Instructor_Focus"]

    prompt=f'''
    Analyze the following drill. 

    The Drill
    Drill Name: {drill}
    Curricumum: {category}
    Target Ranks: {ranks}
    Steps: {steps}
    Instructor Focus: {instructor_focus}
    '''

    prompt=textwrap.dedent(prompt)
    return prompt

def save_data(analysis_list:list):
    analysis_df=pd.DataFrame.from_dict(analysis_list)
    print("SAVING DATA")
    print(f"Drills Analyzed: {len(analysis_list)}")

    analysis_df.to_excel("results/Analyzed Drills.xlsx",sheet_name="Results")

def generate_response(row:pd.Series)->dict:
    client = OpenAI()
    
    prompt=prepare_prompt(row)
    print(prompt)

    response = client.responses.parse(
        model="gpt-6-luna",
        input=prompt,
        text_format=DrillAnalysisModel,
    )

    
    print(response.output_text)

    #Load response text into a json dictionary
    response_dict=json.loads(response.output_text)
    usage=response.usage
    response_dict["Input_Tokens"]=usage.input_tokens
    response_dict["Output_Tokens"]=usage.output_tokens
    response_dict["Cost"]=(0.10*usage.input_tokens)/1000000+(0.50*usage.output_tokens)/1000000

    #Turn row into a dictionary
    row_dict=row.to_dict()

    #Merge row dictionary and response dictionary
    analysis_dict=row_dict | response_dict
    return analysis_dict

def main():
    drill_df=pd.read_excel("data/Drills.xlsx",sheet_name="Drills")
    analysis_list=[]

    previous_analysis_df=pd.read_excel("results/Analyzed Drills.xlsx",sheet_name="Results")
    previous_analysis_steps_list=previous_analysis_df["Steps"].to_list()

    for index,row in drill_df.iterrows():
        #Have the AI not interact with any drills that sound violent.
        if row["Sounds_Violent"]==True:
            analysis_list.append(row.to_dict())
            continue
        
        
        #Generate new results if we want to forcibly rewrite all data
        if force_overwrite:
            new_response=generate_response(row)
            analysis_list.append(new_response)
            continue

        #Fetch matching row if there is a match
        try:
            previous_match_index=previous_analysis_steps_list.index(row["Steps"])
            print("Using previously calculated results")
            analysis_list.append(previous_analysis_df.iloc[previous_match_index].to_dict())
        #Otherwise, generate new response.
        except ValueError:
            new_response=generate_response(row)
            analysis_list.append(new_response)
            

        #Save after every few rows to prevent data loss
        if(index%3==0):
            save_data(analysis_list)
    save_data(analysis_list)

if __name__=="__main__":
    main()