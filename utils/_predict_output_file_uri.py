from typing import Optional

def _predict_output_file_uri(
    output_prefix: str, input_uri: str, job_id: Optional[str]
) -> Optional[str]:
    """
    Compute the deterministic per-job result file URI Bedrock writes to.

    Bedrock lays results out as::

        <output_prefix>/<job-id>/<basename(input_uri)>.out

    We compute it client-side so OpenAI-style ``client.files.content(output_file_id)``
    works without an extra S3 ``ListObjectsV2`` round-trip. Returns ``None`` if we
    don't have enough info; callers should fall back to the bare prefix.
    """
    if not output_prefix or not input_uri or not job_id:
        return None
    if not output_prefix.endswith("/"):
        output_prefix = output_prefix + "/"
    input_basename = input_uri.rsplit("/", 1)[-1]
    if not input_basename:
        return None
    return f"{output_prefix}{job_id}/{input_basename}.out"

