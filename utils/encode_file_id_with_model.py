
def encode_file_id_with_model(
    file_id: str, model: str, id_type: Literal["file", "batch"] = "file"
) -> str:
    """
    Encode a file/batch ID with model routing information.

    Format: <prefix><base64(litellm:<original_id>;model,<model_name>)>
    The result preserves the original prefix (file-, batch_, etc.) for OpenAI compliance.

    Args:
        file_id: Original file/batch ID from the provider (e.g., "file-abc123", "batch_xyz")
        model: Model name from model_list (e.g., "gpt-4o-litellm")
        id_type: Type of ID being encoded. Used to determine the correct prefix when
                 the raw ID lacks a recognizable prefix (e.g., Vertex AI numeric IDs).
                 Defaults to "file" for backward compatibility.

    Returns:
        Encoded ID starting with appropriate prefix and containing routing information

    Examples:
        encode_file_id_with_model("file-abc123", "gpt-4o-litellm")
        -> "file-bGl0ZWxsbTpmaWxlLWFiYzEyMzttb2RlbCxncHQtNG8taWZvb2Q"

        encode_file_id_with_model("batch_abc123", "gpt-4o-test")
        -> "batch_bGl0ZWxsbTpiYXRjaF9hYmMxMjM7bW9kZWwsZ3B0LTRvLXRlc3Q"

        encode_file_id_with_model("3814889423749775360", "gemini-2.5-pro", id_type="batch")
        -> "batch_bGl0ZWxsbTozODE0ODg5NDIzNzQ5Nzc1MzYwO21vZGVsLGdlbWluaS0yLjUtcHJv"
    """
    encoded_str = f"litellm:{file_id};model,{model}"
    encoded_bytes = base64.urlsafe_b64encode(encoded_str.encode())
    encoded_b64 = encoded_bytes.decode().rstrip("=")

    # Detect the prefix from the original ID (file-, batch_, etc.)
    # For provider-specific IDs without a recognizable prefix (e.g., Vertex AI
    # numeric batch IDs), fall back to id_type to determine the correct prefix.
    if file_id.startswith("batch_"):
        prefix = "batch_"
    elif file_id.startswith("file-"):
        prefix = "file-"
    else:
        prefix = "batch_" if id_type == "batch" else "file-"

    return f"{prefix}{encoded_b64}"

