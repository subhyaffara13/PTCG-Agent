
def resampling_validator(value: Union[int, "PILImageResampling"] | None = None):
    if value is None:
        pass
    elif isinstance(value, int) and value not in list(range(6)):
        raise ValueError(
            f"The resampling should be one of {list(range(6))} when provided as integer, but got resampling={value}"
        )
    elif is_vision_available() and not isinstance(value, (PILImageResampling, int)):
        raise ValueError(f"The resampling should an integer or `PIL.Image.Resampling`, but got resampling={value}")

