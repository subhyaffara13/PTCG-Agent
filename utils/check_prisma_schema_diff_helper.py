
def check_prisma_schema_diff_helper(db_url: str) -> Tuple[bool, List[str]]:
    """Checks for differences between current database and Prisma schema.
    Returns:
        A tuple containing:
        - A boolean indicating if differences were found (True) or not (False).
        - A string with the diff output or error message.
    Raises:
        subprocess.CalledProcessError: If the Prisma command fails.
        Exception: For any other errors during execution.
    """
    verbose_logger.debug("Checking for Prisma schema diff...")
    try:
        result = subprocess.run(
            [
                "prisma",
                "migrate",
                "diff",
                "--from-url",
                db_url,
                "--to-schema-datamodel",
                "./schema.prisma",
                "--script",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        # return True, "Migration diff generated successfully."
        sql_commands = extract_sql_commands(result.stdout)

        if sql_commands:
            print("Changes to DB Schema detected")  # noqa: T201
            print("Required SQL commands:")  # noqa: T201
            for command in sql_commands:
                print(command)  # noqa: T201
            return True, sql_commands
        else:
            return False, []
    except subprocess.CalledProcessError as e:
        error_message = f"Failed to generate migration diff. Error: {e.stderr}"
        print(error_message)  # noqa: T201
        return False, []

