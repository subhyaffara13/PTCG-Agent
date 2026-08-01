
def _observer_forward_hook(self, input, output):
    r"""Forward hook that calls observer on the output"""
    return self.activation_post_process(output)

