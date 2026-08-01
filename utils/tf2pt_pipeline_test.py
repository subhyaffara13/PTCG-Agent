
def tf2pt_pipeline_test():
    # For test on linux only
    import logging  # noqa: PLC0415

    import torch  # noqa: PLC0415

    logger = logging.getLogger("")
    for model_name in TFMODELS:
        config, model = tf2pt_pipeline(model_name)
        assert config.model_type is TFMODELS[model_name][0]

        input = torch.randint(low=0, high=config.vocab_size - 1, size=(4, 128), dtype=torch.long)
        try:
            model(input)
        except RuntimeError as e:
            logger.exception(e)

