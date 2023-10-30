from flask import Flask, g, request
import sqlite3
from flask_cors import CORS
import sys
from chatgpt import generate_SQL

DATABASE = "timeline.db"
app = Flask(__name__)

# Configure CORS to allow requests from the React frontend server.
CORS(app, resources={r"/api/": {"origins": "http://localhost:3000"}})


@app.route("/api/", methods=["GET"])
def api():
    # query database and return results
    from_year = (
        request.headers.get("from_year")
        if request.headers.get("from_year") != None
        else 1900
    )
    to_year = (
        request.headers.get("to_year")
        if request.headers.get("to_year") != None
        else 2021
    )
    return get_relevant_events(from_year, to_year)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def run_sql_script(script_path):
    with app.app_context():
        db = get_db()
        with open(script_path, "r") as f:
            sql_script = f.read()
        db.executescript(sql_script)
        db.commit()


def run_sql_query(query):
    with app.app_context():
        db = get_db()
        cursor = db.execute(query)
        results = cursor.fetchall()
        db.commit()
        return results


database_schema = """Table: events, 
        Columns: 
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        time_informal TEXT,
        year INTEGER,
        relevance INTEGER"""


def setup_database():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        time_informal TEXT,
        year INTEGER,
        relevance INTEGER
    )
    """
    run_sql_query(create_table_sql)


# function that queries database for the relevant events that happened between from_time and to_time.
# The function return the results in a list of dictionaries, where each dictionary represents an event.
def get_relevant_events(from_time, to_time, limit=10):
    sql_query = f"""
            SELECT *
            FROM events
            WHERE year >= {from_time} AND year <= {to_time}
            ORDER BY relevance DESC
            LIMIT {limit}
        """
    results = formatify(run_sql_query(sql_query))

    return results


def formatify(results):
    # convert elements of results array to json
    keys = ["id", "name", "description", "time_informal", "year", "relevance"]
    dict_list = []
    for result_el in results:
        if len(result_el) == len(keys):
            dictionary = {keys[i]: result_el[i] for i in range(len(keys))}
            dict_list.append(dictionary)
        else:
            print(
                f"Skipping an inner array because it doesn't have {len(keys)} elements."
            )
    return dict_list


def populate_database():
    generate_SQL(database_schema)


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
    # if len(sys.argv) > 1 and sys.argv[1] == "generate":
    #     print("Generating an SQL file...")
    #     populate_database()
