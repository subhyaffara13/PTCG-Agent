
def get_tokenizer(pipeline_info: PipelineInfo, framework_model_dir, subfolder="tokenizer"):
    tokenizer_dir = os.path.join(framework_model_dir, pipeline_info.name(), subfolder)

    if not os.path.exists(tokenizer_dir):
        model = CLIPTokenizer.from_pretrained(
            pipeline_info.name(),
            subfolder=subfolder,
            use_safetensors=pipeline_info.is_xl(),
        )
        model.save_pretrained(tokenizer_dir)
    else:
        print(f"[I] Load tokenizer pytorch model from: {tokenizer_dir}")
        model = CLIPTokenizer.from_pretrained(tokenizer_dir)
    return model

