
def build_signature(positional: Sequence[str], optional: Sequence[str]) -> str:
    """Build function signature from lists of positional and optional argument names."""
    args: MutableSequence[str] = []
    args.extend(positional)
    for arg in optional:
        if arg.startswith("*"):
            args.append(arg)
        else:
            args.append(f"{arg}=...")
    sig = f"({', '.join(args)})"
    # Ad-hoc fixes.
    sig = sig.replace("(self)", "")
    return sig

