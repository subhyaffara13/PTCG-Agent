import os
from typing import Optional

def check_prisma_schema_diff(db_url: Optional[str] = None) -> None:
    """Main function to run the Prisma schema diff check."""
    if db_url is None:
        db_url = os.getenv("DATABASE_URL")
        if db_url is None:
            raise Exception("DATABASE_URL not set")
    has_diff, message = check_prisma_schema_diff_helper(db_url)
    if has_diff:
        verbose_logger.exception(
            "🚨🚨🚨 prisma schema out of sync with db. Consider running these sql_commands to sync the two - {}".format(
                message
            )
        )

