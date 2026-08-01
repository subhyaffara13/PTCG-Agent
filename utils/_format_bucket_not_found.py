
def _format_bucket_not_found(error: BucketNotFoundError) -> str:
    if error.bucket_id:
        msg = f"Bucket '{error.bucket_id}' not found."
        cmd = f"hf buckets create {error.bucket_id}"
    else:
        msg = "Bucket not found."
        cmd = "hf buckets create <bucket_id>"
    msg += "\nIf the bucket is private, make sure you are authenticated and your token has the required permissions."
    msg += f"\nIf the bucket does not exist, create it with: {cmd}"
    return msg

