
def prepare_model_for_inference(args, model, config, tokenizer, prompt_length, prompt):
    clear_cache()
    inputs, outputs = get_initial_inputs_and_outputs(
        config, tokenizer, prompt_length, prompt, args.target_device, args.use_fp16, args.use_buffer_share, args.engine
    )
    _, outputs = run_inference(args, model, args.warmup_runs, inputs, outputs)
    return inputs, outputs

