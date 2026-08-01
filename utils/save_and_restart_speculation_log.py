
def save_and_restart_speculation_log(
    tx: InstructionTranslatorBase,
) -> Generator[None, None, None]:
    # When reconstructing a generator after a graph break, we advance it until
    # it is fully exhausted. This process adds new entries to the speculation
    # log that were not previously observed. Without temporarily clearing the
    # speculation log, this could lead to a divergence error.

    entries = tx.speculation_log.entries
    index = tx.speculation_log.index
    try:
        tx.speculation_log.entries = []
        tx.speculation_log.index = 0
        yield
    finally:
        tx.speculation_log.entries = entries
        tx.speculation_log.index = index

