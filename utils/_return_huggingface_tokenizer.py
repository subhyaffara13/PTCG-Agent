
def _return_huggingface_tokenizer(model: str) -> Optional[SelectTokenizerResponse]:
    if model in litellm.cohere_models and "command-r" in model:
        # cohere
        cohere_tokenizer = Tokenizer.from_pretrained(
            "Xenova/c4ai-command-r-v01-tokenizer"
        )
        return {"type": "huggingface_tokenizer", "tokenizer": cohere_tokenizer}
    # anthropic
    elif model in litellm.anthropic_models and "claude-3" not in model:
        claude_tokenizer = Tokenizer.from_str(claude_json_str)
        return {"type": "huggingface_tokenizer", "tokenizer": claude_tokenizer}
    # llama2
    elif "llama-2" in model.lower() or "replicate" in model.lower():
        tokenizer = Tokenizer.from_pretrained("hf-internal-testing/llama-tokenizer")
        return {"type": "huggingface_tokenizer", "tokenizer": tokenizer}
    # llama3
    elif "llama-3" in model.lower():
        tokenizer = Tokenizer.from_pretrained("Xenova/llama-3-tokenizer")
        return {"type": "huggingface_tokenizer", "tokenizer": tokenizer}
    else:
        return None

