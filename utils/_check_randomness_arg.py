
def _check_randomness_arg(randomness: str) -> None:
    if randomness not in ["error", "different", "same"]:
        raise RuntimeError(
            f"Only allowed values for randomness are 'error', 'different', or 'same'. Got {randomness}"
        )

