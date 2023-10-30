import os
import openai
from datetime import datetime

GPT_MODEL = "gpt-3.5-turbo"
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_gpt(query, database_schema):
    messages = []
    messages.append(
        {
            "role": "system",
            "content": "Populate a database with important historic events of the world and of human history. Do this by generating SQL INSERT statements strictly following this database schema: {database_schema}. Do not specify the id column. Include the name of the event in the name column. Include a short description of the event in the description column. Include some informal text about when this happened in the time_informal column. Include an positive or negative integer which is the specific year when this event happened in the year column. Years that are before BCE are negative. Also include a relevance number in the range of 0 to 100 about how important this event was in the history of humanity and of the world. Generate statements that can be directly executed in SQLite3. Please omit any leading or following text. ",
        }
    )
    messages.append({"role": "user", "content": query})
    assistant_message = openai.ChatCompletion.create(
        model=GPT_MODEL, messages=messages, temperature=0
    )["choices"][0]["message"]["content"]
    messages.append(assistant_message)
    return assistant_message


def write_sql_to_file(sql_statements, file_name="sql_file.sql"):
    # Write the SQL statements to the file
    with open(file_name, "w") as file:
        file.write(sql_statements)
    print(f"SQL statements have been written to {file_name}")


def generate_SQL(database_schema,from_year=None, to_year=None):
    query = (
        f"Only generate the queries for events that happened between year {from_year} and year {to_year}."
    ) if from_year and to_year else "Generate at least 50 events. Do not generate the same event twice."
    response = call_gpt(query, database_schema)
    write_sql_to_file(response, f"sql/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}_from_{from_year}_to_{to_year}.sql")
