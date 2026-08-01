
def _asof_by_function(direction: str):
    name = f"asof_join_{direction}_on_X_by_Y"
    return getattr(libjoin, name, None)

