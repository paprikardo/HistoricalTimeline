import sqlite3
from flask import g
from app import app

DATABASE = "timeline.db"

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


def setup_database():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        event_name TEXT,
        description TEXT,
        time_informal TEXT,
        year INTEGER,
        relevance INTEGER
    )
    """
    database_schema = """Table: events, 
        Columns: 
        id INTEGER PRIMARY KEY,
        event_name TEXT,
        description TEXT,
        time_informal TEXT,
        year INTEGER,
        relevance INTEGER"""
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
    results = run_sql_query(sql_query)
    return results
