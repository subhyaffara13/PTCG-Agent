
def _dump_snapshot(filename="dump_snapshot.pickle", augment_with_fx_traces=False):
    """
    Save a pickled version of the `torch.memory._snapshot()` dictionary to a file.

    This file can be opened by the interactive snapshot viewer at pytorch.org/memory_viz

    Snapshot file sizes scale with `max_entries` and stack trace depth per entry,
    with several KB per entry. These can easily be in the GB range for longer running
    workflows with large `max_entries`.

    Args:
        filename (str, optional): Name of the file to create. Defaults to "dump_snapshot.pickle".
        augment_with_fx_traces (bool, optional): If True, augment the snapshot with FX debug information
                                                  before dumping. This maps generated FX code stack traces
                                                  back to original model source code. Defaults to False.
    """
    s = _snapshot(augment_with_fx_traces=augment_with_fx_traces)

    with open(filename, "wb") as f:
        pickle.dump(s, f)


def _dump_snapshot(
    filename: str = "dump_snapshot.pickle", augment_with_fx_traces: bool = False
) -> None:
    """
    Save a pickled version of the `torch.memory._snapshot()` dictionary to a file.

    This file can be opened by the interactive snapshot viewer at pytorch.org/memory_viz

    Snapshot file sizes scale with `max_entries` and stack trace depth per entry,
    with several KB per entry. These can easily be in the GB range for longer running
    workflows with large `max_entries`.

    Arguments:
        filename (str, optional): Name of the file to create. Defaults to "dump_snapshot.pickle".
        augment_with_fx_traces (bool, optional): If True, augment the snapshot with FX debug information
            before dumping. This maps generated FX code stack traces back to original model
            source code. Defaults to ``False``.
    """
    s = _snapshot(augment_with_fx_traces=augment_with_fx_traces)

    with open(filename, "wb") as f:
        pickle.dump(s, f)

