
def _get_mutation_counters(t: torch.Tensor) -> MutationCounters:
    return MutationCounters(
        _get_mutation_counter(t),
        _get_storage_changed_counter(t),
        _get_inductor_storage_resized_counter(t),
    )

