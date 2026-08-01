
def run_turbo_demo(args):
    """Run demo of generating images with test prompts with ORT CUDA provider."""
    args.engine = "ORT_CUDA"
    base, refiner = load_pipelines(args, 1)

    from datasets import load_dataset  # noqa: PLC0415

    dataset = load_dataset("Gustavosta/Stable-Diffusion-Prompts")
    num_rows = dataset["test"].num_rows
    batch_size = args.batch_size
    num_batch = int(num_rows / batch_size)
    args.batch_size = 1
    for i in range(num_batch):
        args.prompt = [dataset["test"][i]["Prompt"] for i in range(i * batch_size, (i + 1) * batch_size)]
        base.set_scheduler(args.scheduler)
        if refiner:
            refiner.set_scheduler(args.refiner_scheduler)
        prompt, negative_prompt = repeat_prompt(args)
        run_pipelines(args, base, refiner, prompt, negative_prompt, is_warm_up=False)

    base.teardown()
    if refiner:
        refiner.teardown()

