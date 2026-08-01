
def get_negative_prompt_kwargs(negative_prompt, use_num_images_per_prompt, is_flux, batch_size) -> dict:
    # Flux does not support negative prompt
    kwargs = (
        (
            {"negative_prompt": negative_prompt}
            if use_num_images_per_prompt
            else {"negative_prompt": [negative_prompt] * batch_size}
        )
        if not is_flux
        else {}
    )

    # Fix the random seed so that we can inspect the output quality easily.
    if torch.cuda.is_available():
        kwargs["generator"] = torch.Generator(device="cuda").manual_seed(123)

    return kwargs

