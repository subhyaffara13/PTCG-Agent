
def _resolve_tokenizer(tokenizer, load_tokenizer, use_fast, model_name, config, task, hub_kwargs, model_kwargs):
    """Resolve and optionally load the tokenizer required by the pipeline class."""

    def load(tokenizer):
        tokenizer = _infer_pipeline_component(
            tokenizer,
            model_name,
            config,
            "Impossible to guess which tokenizer to use. "
            "Please provide a PreTrainedTokenizer class or a path/identifier to a pretrained tokenizer.",
        )

        if not isinstance(tokenizer, (str, tuple)):
            return tokenizer

        tokenizer_identifier, tokenizer_kwargs, tokenizer_use_fast = _get_tokenizer_loading_kwargs(
            tokenizer, use_fast, model_kwargs
        )
        return AutoTokenizer.from_pretrained(
            tokenizer_identifier,
            use_fast=tokenizer_use_fast,
            _from_pipeline=task,
            **hub_kwargs,
            **tokenizer_kwargs,
        )

    return _load_pipeline_component(load_tokenizer, tokenizer, load)

