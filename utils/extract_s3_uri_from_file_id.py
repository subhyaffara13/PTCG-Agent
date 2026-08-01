
def extract_s3_uri_from_file_id(file_id: str) -> str:
    """
    Resolve a Bedrock file id to its S3 URI.

    Accepts either a base64-encoded LiteLLM unified file id (whose decoded
    form carries `llm_output_file_id,s3://...`) or a direct `s3://` URI.
    """
    try:
        padded = file_id + "=" * (-len(file_id) % 4)
        decoded = base64.urlsafe_b64decode(padded).decode()

        if decoded.startswith(SpecialEnums.LITELM_MANAGED_FILE_ID_PREFIX.value):
            if "llm_output_file_id," in decoded:
                return decoded.split("llm_output_file_id,")[1].split(";")[0]
    except Exception:
        pass

    if file_id.startswith("s3://"):
        return file_id

    raise ValueError("file_id must be a managed LiteLLM S3 file id")

