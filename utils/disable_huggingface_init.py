
def disable_huggingface_init():
    """do not init model twice as it slow initialization"""

    torch.nn.init.kaiming_uniform_ = lambda x, *args, **kwargs: x
    torch.nn.init.uniform_ = lambda x, *args, **kwargs: x
    torch.nn.init.normal_ = lambda x, *args, **kwargs: x
    torch.nn.init.constant_ = lambda x, *args, **kwargs: x
    torch.nn.init.xavier_uniform_ = lambda x, *args, **kwargs: x
    torch.nn.init.xavier_normal_ = lambda x, *args, **kwargs: x
    torch.nn.init.kaiming_normal_ = lambda x, *args, **kwargs: x
    torch.nn.init.orthogonal_ = lambda x, *args, **kwargs: x

