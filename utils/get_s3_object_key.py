
def get_s3_object_key(
    s3_path: str,
    prefix: str,
    start_time: datetime,
    s3_file_name: str,
) -> str:
    s3_object_key = (
        (s3_path.rstrip("/") + "/" if s3_path else "")
        + prefix
        + start_time.strftime("%Y-%m-%d")
        + "/"
        + s3_file_name
    )  # we need the s3 key to include the time, so we log cache hits too
    s3_object_key += ".json"
    return s3_object_key

