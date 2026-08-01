
def visualize_data() -> str:
    """Retrieve the data to be used by the visualizer.

    Returns:
        str: The data to be used by the visualizer.
    """
    return lib.VisualizeData(Battle.battle_ptr).decode()

