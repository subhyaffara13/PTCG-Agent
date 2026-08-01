
def sample_inputs_unique_consecutive(*args, **kwargs):
    for sample_input in sample_inputs_unique(*args, **kwargs):
        if not sample_input.kwargs["sorted"]:
            sample_input.kwargs.pop("sorted")
            yield sample_input

