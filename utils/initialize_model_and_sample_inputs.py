
def initialize_model_and_sample_inputs(hf_model: str, cache_dir: str | None, tokenizer=None):
    """
    get the pretrained torch model from hugginface,
    and sample model-inputs
    """

    disable_huggingface_init()

    model = transformers.AutoModelForCausalLM.from_pretrained(  # type: ignore
        hf_model, torch_dtype=torch.float16, cache_dir=cache_dir, trust_remote_code=True
    )
    if tokenizer is None:
        tokenizer = hf_model
    tokenizer = transformers.AutoTokenizer.from_pretrained(tokenizer)  # type: ignore

    sample_inputs = tuple(tokenizer("Hello, my dog is cute", return_tensors="pt").values())
    return model, sample_inputs

