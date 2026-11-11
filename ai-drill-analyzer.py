import textwrap

import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    drill_df=pd.read_excel("data/Drills.xlsx",sheet_name="Drills")
    for index,row in drill_df.iterrows():
        #Do not send self defense drills to ChatGPT. Unsure about sending how to defend yourself from a weapon to AI.
        if "SELF" in str(row["Category"]).upper() or "DEFENSE" in str(row["Category"]).upper():
            continue

        client = OpenAI()

        drill=row["Name"]
        ranks=row["Ranks"]
        steps=row["Steps"]

        prompt=f'''
        Analyze the following drill. Return a Python dictionary that score the drill from 1 to 10 on 
        Learning Potential
        Physical Development
        Fun

        Drill:{drill}
        Target Ranks:{ranks}
        Steps:{steps}
        '''

        prompt=textwrap.dedent(prompt)

        print(prompt)
        break

        response = client.responses.create(
            model="gpt-6-luna",
            input=prompt,
        )

        print(response.output_text)
        break


if __name__=="__main__":
    main()