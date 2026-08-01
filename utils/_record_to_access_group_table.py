
def _record_to_access_group_table(record) -> LiteLLM_AccessGroupTable:
    """Convert a Prisma record to a LiteLLM_AccessGroupTable pydantic object for caching."""
    return LiteLLM_AccessGroupTable(**record.dict())

