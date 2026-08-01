
def _serialize_sample(sample_input):
    # NB: For OpInfos, SampleInput.summary() prints in a cleaner way.
    if getattr(sample_input, "summary", None) is not None:
        return sample_input.summary()
    return str(sample_input)

