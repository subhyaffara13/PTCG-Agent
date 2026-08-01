
def filter_output_hidden_states(forward_function):
    """
    Wrapper for backbone forwards. Backbones always compute `hidden_states` to build their feature maps, so
    this forces `output_hidden_states=True` on the wrapped forward and then removes `hidden_states` from the
    returned object unless the caller explicitly requested them.

    NOTE: We assume a `can_return_tuple` decorator to be applied before so that we always expect a dict like
          object to remove the hidden states.
    """

    @functools.wraps(forward_function)
    def wrapper(self, *args, **kwargs):
        output_hidden_states = kwargs.get("output_hidden_states", getattr(self.config, "output_hidden_states", False))
        kwargs["output_hidden_states"] = True
        output = forward_function(self, *args, **kwargs)
        if not output_hidden_states:
            filtered_output_data = {k: v for k, v in output.items() if k != "hidden_states"}
            output = type(output)(**filtered_output_data)
        return output

    return wrapper

