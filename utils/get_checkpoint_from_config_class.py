
def get_checkpoint_from_config_class(config_class):
    checkpoint = None

    # source code of `config_class`
    # config_source = inspect.getsource(config_class)
    config_source = config_class.__doc__
    if not config_source:
        return None

    checkpoints = _re_checkpoint.findall(config_source)
    # Each `checkpoint` is a tuple of a checkpoint name and a checkpoint link.
    # For example, `('google-bert/bert-base-uncased', 'https://huggingface.co/google-bert/bert-base-uncased')`
    for ckpt_name, ckpt_link in checkpoints:
        # allow the link to end with `/`
        ckpt_link = ckpt_link.removesuffix("/")

        # verify the checkpoint name corresponds to the checkpoint link
        ckpt_link_from_name = f"https://huggingface.co/{ckpt_name}"
        if ckpt_link == ckpt_link_from_name:
            checkpoint = ckpt_name
            break

    return checkpoint

