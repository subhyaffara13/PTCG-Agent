
def _prisma_skill_to_litellm(prisma_skill) -> LiteLLM_SkillsTable:
    """Convert a Prisma skill record to LiteLLM_SkillsTable.

    Handles Base64 decoding of file_content field — model_dump() converts
    Base64 fields to base64-encoded strings.
    """
    import base64

    data = prisma_skill.model_dump()

    if data.get("file_content") is not None:
        if isinstance(data["file_content"], str):
            data["file_content"] = base64.b64decode(data["file_content"])

    return LiteLLM_SkillsTable(**data)

