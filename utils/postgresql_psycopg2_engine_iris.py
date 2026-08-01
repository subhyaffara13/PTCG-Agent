
def postgresql_psycopg2_engine_iris(postgresql_psycopg2_engine, iris_path):
    create_and_load_iris(postgresql_psycopg2_engine, iris_path)
    create_and_load_iris_view(postgresql_psycopg2_engine)
    return postgresql_psycopg2_engine

