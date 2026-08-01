
def generate_guarded(
    mod: str, target: str, ignore_errors: bool = True, verbose: bool = False
) -> Iterator[None]:
    """Ignore or report errors during stub generation.

    Optionally report success.
    """
    if verbose:
        print(f"Processing {mod}")
    try:
        yield
    except Exception as e:
        if not ignore_errors:
            raise e
        else:
            # --ignore-errors was passed
            print("Stub generation failed for", mod, file=sys.stderr)
    else:
        if verbose:
            print(f"Created {target}")

