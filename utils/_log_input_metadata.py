
def _log_input_metadata(runtime_metadata: ViewAndMutationMeta) -> None:
    aot_graphs_log.debug(
        "Expected input metadata (count=%s):", len(runtime_metadata.subclass_inp_meta)
    )
    for i, meta in enumerate(runtime_metadata.subclass_inp_meta):
        aot_graphs_log.debug("  [%s] %s", i, meta)

