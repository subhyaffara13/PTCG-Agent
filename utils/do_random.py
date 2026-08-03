import random

def do_random(context: "Context", seq: "t.Sequence[V]") -> "t.Union[V, Undefined]":
    """Return a random item from the sequence."""
    try:
        return random.choice(seq)
    except IndexError:
        return context.environment.undefined("No random item, sequence was empty.")

