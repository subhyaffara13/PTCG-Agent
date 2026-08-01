
def _observer_forward_pre_hook(self, input):
    r"""Forward pre hook that calls observer on the output"""
    return self.activation_post_process(input[0])

