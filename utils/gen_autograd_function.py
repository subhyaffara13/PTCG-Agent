
def gen_autograd_function(name, forward, backward):
    generated_cls = type(
        name,
        (torch.autograd.Function,),
        {
            "forward": staticmethod(forward),
            "backward": staticmethod(backward),
        },
    )
    return generated_cls

