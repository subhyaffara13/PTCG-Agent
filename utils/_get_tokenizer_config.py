
def _get_tokenizer_config(hf_model_name: str) -> Dict[str, Any]:
    """
    Fetch tokenizer_config.json from HuggingFace (sync)

    Args:
        hf_model_name: HuggingFace model name (e.g., 'openai/gpt-oss-120b')

    Returns:
        Dict with 'status' and optionally 'tokenizer' keys
    """
    try:
        url = f"https://huggingface.co/{hf_model_name}/raw/main/tokenizer_config.json"
        client = _get_httpx_client()
        response = client.get(url=url)
    except Exception as e:
        raise e
    if response.status_code == 200:
        tokenizer_config = json.loads(response.content)
        return {"status": "success", "tokenizer": tokenizer_config}
    else:
        return {"status": "failure"}

