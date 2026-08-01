
def process_automatic_dynamic(
    tx: InstructionTranslator,
    name: str,
    entry: FrameStateSizeEntry,
    *,
    is_unspecialized_nn_module: bool = False,
) -> FrameStateSizeEntry:
    if (st := tx.distributed_state) is None:
        return update_automatic_dynamic(
            tx,
            name,
            entry,
            is_unspecialized_nn_module=is_unspecialized_nn_module,
        )
    elif st.all_states is None:
        # Preflight, always pretend as if it's static.  The point here
        # is we want to get through the preflight quickly, and static
        # will run faster.  The preexisting frame state will get
        # applied anyway after we do compiler collectives.
        # TODO: I'm not sure if we should just bong the entire pgo
        # state here, it kind of depends if we're going to have other
        # things that talk in compiler collective.  Also, the PGO
        # state, if we've already inferred something is automatic
        # dynamic, will have lost the actual input sizes, which might
        # be useful for debugging purposes (e.g., observing 0/1
        # specialization).  Bonging the entire PGO state here would
        # let us delete this logic here; the compiler collective
        # would just directly update_automatic_dynamic
        st.local_state.automatic_dynamic[name] = entry
        return entry
    else:
        # Apply the updates.  NB: all_states includes the local state
        # too.
        res = None
        for sub_state in st.all_states:
            if name in sub_state.automatic_dynamic:
                res = update_automatic_dynamic(
                    tx,
                    name,
                    sub_state.automatic_dynamic[name],
                    is_unspecialized_nn_module=is_unspecialized_nn_module,
                )
        assert res is not None
        return res

