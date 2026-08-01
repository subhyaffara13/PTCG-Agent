
def alert_not_deterministic(caller: str):
    if torch.are_deterministic_algorithms_enabled():
        if torch.is_deterministic_algorithms_warn_only_enabled():
            warnings.warn(
                f"{caller} does not have a deterministic implementation, but you set "
                f"'torch.use_deterministic_algorithms(True, warn_only=True)'. "
                f"You can file an issue at https://github.com/pytorch/pytorch/issues "
                f"to help us prioritize adding deterministic support for this operation.",
                stacklevel=2,
            )
        else:
            torch._check(
                False,
                lambda: (
                    f"{caller} does not have a deterministic implementation, but you set "
                    f"'torch.use_deterministic_algorithms(True)'. You can turn off "
                    f"determinism just for this operation, or you can use the "
                    f"'warn_only=True' option, if that's acceptable for your application. "
                    f"You can also file an issue at https://github.com/pytorch/pytorch/issues "
                    f"to help us prioritize adding deterministic support for this operation."
                ),
            )

