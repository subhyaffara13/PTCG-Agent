
def get_warning(
    api: str, new_api: str | None = None, replace_newlines: bool = False
) -> str:
    if new_api is None:
        new_api = f"torch.func.{api}"
    warning = (
        f"We've integrated functorch into PyTorch. As the final step of the \n"
        f"integration, `functorch.{api}` is deprecated as of PyTorch \n"
        f"2.0 and will be deleted in a future version of PyTorch >= 2.3. \n"
        f"Please use `{new_api}` instead; see the PyTorch 2.0 release notes \n"
        f"and/or the `torch.func` migration guide for more details \n"
        f"https://pytorch.org/docs/main/func.migrating.html"
    )
    if replace_newlines:
        warning = warning.replace("\n", "")
    return warning

