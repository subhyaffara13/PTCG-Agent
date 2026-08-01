
def postgresql_psycopg2_conn_types(postgresql_psycopg2_engine_types):
    with postgresql_psycopg2_engine_types.connect() as conn:
        yield conn

