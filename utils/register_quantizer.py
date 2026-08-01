
def register_quantizer(name: str):
    """Register a custom quantizer."""

    def register_quantizer_fn(cls):
        if name in AUTO_QUANTIZER_MAPPING:
            raise ValueError(f"Quantizer '{name}' already registered")

        if not issubclass(cls, HfQuantizer):
            raise TypeError("Quantizer must extend HfQuantizer")

        AUTO_QUANTIZER_MAPPING[name] = cls
        return cls

    return register_quantizer_fn

