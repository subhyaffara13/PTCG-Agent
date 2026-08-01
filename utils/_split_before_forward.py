
def _split_before_forward(self, *args, **kwargs):
    pipe_split()
    return self._orig_forward(*args, **kwargs)

