
def rope_config_validation(config: RotaryEmbeddingConfigMixin, ignore_keys: set | None = None):
    """
    This is a deprecated function.
    It has been kept for backward compatibility with custom code models.
    """
    warnings.warn(
        "`rope_config_validation` is deprecated and has been removed. "
        "Its functionality has been moved to RotaryEmbeddingConfigMixin.validate_rope method. "
        "PreTrainedConfig inherits this class, so please call self.validate_rope() instead. "
        "Also, make sure to use the new rope_parameters syntax. "
        "You can call self.standardize_rope_params() in the meantime.",
        FutureWarning,
    )
    config.standardize_rope_params()
    config.validate_rope()

