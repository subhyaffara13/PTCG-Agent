
def get_conversion_pr_reference(api: HfApi, model_id: str, **kwargs):
    private = api.model_info(model_id).private

    logger.info("Attempting to create safetensors variant")
    pr_title = "Adding `safetensors` variant of this model"
    token = kwargs.get("token")

    # This looks into the current repo's open PRs to see if a PR for safetensors was already open. If so, it
    # returns it. It checks that the PR was opened by the bot and not by another user so as to prevent
    # security breaches.
    pr = previous_pr(api, model_id, pr_title, token=token)

    if pr is None or (not private and pr.author != "SFconvertbot"):
        spawn_conversion(token, private, model_id)
        pr = previous_pr(api, model_id, pr_title, token=token)
    else:
        logger.info("Safetensors PR exists")
    if pr is None:
        raise OSError(
            "Could not create safetensors conversion PR. The repo does not appear to have a file named pytorch_model.bin or model.safetensors."
            "If you are loading with variant, use `use_safetensors=False` to load the original model."
        )

    sha = f"refs/pr/{pr.num}"

    return sha

