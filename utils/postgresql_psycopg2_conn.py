
def postgresql_psycopg2_conn(postgresql_psycopg2_engine):
    with postgresql_psycopg2_engine.connect() as conn:
        yield conn

