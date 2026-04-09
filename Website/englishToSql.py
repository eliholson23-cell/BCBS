from groq import Groq
import os
from supabase import *
from infoClass import apiInfo
import json



client = Groq(
    api_key=r'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'
)



SUPABASE_URL = "https://ftrdkvzobzxogkoxfrjw.supabase.co"
SUPABASE_KEY = "sb_publishable_84vY_MTXJpyX7Ub9geHJNA_6nxqh0Xc"

DBClient = create_client(SUPABASE_URL, SUPABASE_KEY)



def genSQL(prompt = 'none', schema = None):
    schema = r"TABLE: users\nCOLUMNS: id,first_name,last_name,email,phone,city,state"
    sysPrompt = f"based on a user request about a data base, you output the columns to select in a json format. Schema: {schema}." + "IMPORTANT: only output json and nothing else. Never include reasoning Always format json as follows {\"columns\": [\"col_names)\"]}"
    

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": sysPrompt,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="groq/compound",
        
    )

    return chat_completion.choices[0].message.content


def readDB(dbInfo):


    #format llm output into a dict
    colsList = formatter(dbInfo)
    #print(f"COL LIST: {colsList}")

    colString = ""

    for x in range(len(colsList)):
        if x == 0:
            colString = colsList[x]
        else:
            colString = colString + ", " + colsList[x]
    #print(f"COLSTRING: {colString}")

    response = DBClient.table("Test1").select(colString).execute()

    data = response.data
    #print(data)
    printer(data)

#take llm json and turn it into usable struct
def formatter(json_string):
    
    #check if string can be formatted

    # Convert string to a Python dictionary
    data = json.loads(json_string)

    return data['columns']

def printer(data,limit = 20):
    
    
    if not data:
        print("No data")
        return

    total_rows = len(data)
    rows = data[:limit]

    # Use consistent column order (from first row)
    columns = list(data[0].keys())

    # Compute column widths (only from displayed rows)
    col_widths = {
        col: max(
            len(col),
            max(len(str(row.get(col, ""))) for row in rows)
        )
        for col in columns
    }

    # Header
    header = " | ".join(col.ljust(col_widths[col]) for col in columns)
    print(header)
    print("-" * len(header))

    # Rows
    for row in rows:
        print(" | ".join(str(row.get(col, "")).ljust(col_widths[col]) for col in columns))

    # Footer info
    if total_rows > limit:
        print(f"\nShowing {limit} of {total_rows} rows...")
    else:
        print(f"\nTotal rows: {total_rows}")
#=====================================================================================#
#==================================End of Functions===================================#
#=====================================================================================#


prompt = input("Enter a prompt: ")


#returns the cols to select in a json string
dbInfo = genSQL(prompt)

print(dbInfo)
print("\n=========================================================\n")

readDB(dbInfo)


#break down a.i prompt into supabase-py components
#readDB(dbInfo)
