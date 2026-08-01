
def _is_valid_gcs_bucket_name(bucket: str) -> bool:
    """
    Validate bucket name against core GCS naming constraints.
    """
    bucket_length = len(bucket)
    max_bucket_length = 222 if "." in bucket else 63
    if bucket_length < 3 or bucket_length > max_bucket_length:
        return False
    if "." in bucket and any(
        len(label) == 0 or len(label) > 63 for label in bucket.split(".")
    ):
        return False
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*[a-z0-9]", bucket):
        return False
    if ".." in bucket:
        return False
    if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", bucket):
        return False
    return True

