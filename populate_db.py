from db_handling import run_sql_query, setup_database, close_connection

setup_database()
run_sql_query(
    "INSERT INTO events (event_name, description, time_informal, year, relevance) VALUES ('The Big Bang', 'The universe was created', '13.8 billion years ago', -13800000000, 1)"
)
run_sql_query(
    "INSERT INTO events (event_name, description, time_informal, year, relevance) VALUES ('Test', 'Test2', '2010', 2010, 1)"
)
close_connection()