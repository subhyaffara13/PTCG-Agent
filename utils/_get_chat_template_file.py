
def _get_chat_template_file(hf_model_name: str) -> Dict[str, Any]:
    """
    Fetch chat template from separate .jinja file (sync)

    Args:
        hf_model_name: HuggingFace model name (e.g., 'openai/gpt-oss-120b')

    Returns:
        Dict with 'status' and optionally 'chat_template' keys
    """
    template_filenames = ["chat_template.jinja", "chat_template.jinja2"]
    client = _get_httpx_client()

    for filename in template_filenames:
        try:
            url = f"https://huggingface.co/{hf_model_name}/raw/main/{filename}"
            response = client.get(url=url)
            if response.status_code == 200:
                return {
                    "status": "success",
                    "chat_template": response.content.decode("utf-8"),
                }
        except Exception:
            continue

    return {"status": "failure"}

