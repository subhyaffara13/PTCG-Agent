
def count_label(label: str) -> None:
    prev = simple_call_counter.setdefault(label, 0)
    simple_call_counter[label] = prev + 1

