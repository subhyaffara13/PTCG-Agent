
def dynamo_dir() -> str | None:
    import torch._dynamo

    return _module_dir(torch._dynamo)

