
def _prompt_single_image(image_seq_len, fake_token_around_image, image_token, global_image_token):
    """Prompt with expanded image tokens for a single image."""
    return (
        f"{fake_token_around_image}"
        + f"{global_image_token}"
        + f"{image_token}" * image_seq_len
        + f"{fake_token_around_image}"
    )

