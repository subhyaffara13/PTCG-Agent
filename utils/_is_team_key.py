
def _is_team_key(data: Union[GenerateKeyRequest, LiteLLM_VerificationToken]):
    return data.team_id is not None

