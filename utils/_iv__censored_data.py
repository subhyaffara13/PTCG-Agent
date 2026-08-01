
def _iv_CensoredData(
    sample: "npt.ArrayLike | CensoredData", param_name: str = "sample"
) -> CensoredData:
    """Attempt to convert `sample` to `CensoredData`."""
    if not isinstance(sample, CensoredData):
        try:  # takes care of input standardization/validation
            sample = CensoredData(uncensored=sample)
        except ValueError as e:
            message = str(e).replace('uncensored', param_name)
            raise type(e)(message) from e
    return sample

