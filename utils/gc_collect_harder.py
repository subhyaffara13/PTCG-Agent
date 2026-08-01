
def gc_collect_harder(iterations: int) -> None:
    for _ in range(iterations):
        gc.collect()

