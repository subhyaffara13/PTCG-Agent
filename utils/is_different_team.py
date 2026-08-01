
def is_different_team(
    data: UpdateKeyRequest, existing_key_row: LiteLLM_VerificationToken
) -> bool:
    if data.team_id is None:
        return False
    if existing_key_row.team_id is None:
        return True
    return data.team_id != existing_key_row.team_id

