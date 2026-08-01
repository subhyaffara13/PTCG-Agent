
def postgresql_psycopg2_engine_types(postgresql_psycopg2_engine, types_data):
    create_and_load_types(postgresql_psycopg2_engine, types_data, "postgres")
    return postgresql_psycopg2_engine

