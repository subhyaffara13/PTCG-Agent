
def postgresql_psycopg2_conn_iris(postgresql_psycopg2_engine_iris):
    with postgresql_psycopg2_engine_iris.connect() as conn:
        yield conn

