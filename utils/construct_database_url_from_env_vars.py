
def construct_database_url_from_env_vars() -> Optional[str]:
    """
    Construct a DATABASE_URL from individual environment variables.
    Returns:
        Optional[str]: The constructed DATABASE_URL or None if required variables are missing
    """
    import urllib.parse

    # Check if all required variables are provided
    database_host = os.getenv("DATABASE_HOST")
    database_username = os.getenv("DATABASE_USERNAME")
    database_password = os.getenv("DATABASE_PASSWORD")
    database_name = os.getenv("DATABASE_NAME")
    database_schema = os.getenv("DATABASE_SCHEMA")

    if database_host and database_username and database_name:
        # Handle the problem of special character escaping in the database URL
        database_username_enc = urllib.parse.quote_plus(database_username)
        database_password_enc = (
            urllib.parse.quote_plus(database_password) if database_password else ""
        )
        database_name_enc = urllib.parse.quote_plus(database_name)

        # Construct DATABASE_URL from the provided variables
        if database_password:
            database_url = f"postgresql://{database_username_enc}:{database_password_enc}@{database_host}/{database_name_enc}"
        else:
            database_url = f"postgresql://{database_username_enc}@{database_host}/{database_name_enc}"

        if database_schema:
            database_url += f"?schema={database_schema}"

        return database_url

    return None

