
def _format_items_dict(items: Mapping[str, int]) -> str:
    """Render a {book, hat, basketball} dict as ``Book=A, Hat=B, Basketball=C``."""
    return ", ".join(f"{_ITEM_LABELS[k]}={int(items.get(k, 0))}" for k in _ITEM_KEYS)


def _format_items_dict(items: Mapping[str, int], labels: Mapping[str, str]) -> str:
    """Render a {book, hat, basketball} dict as ``L1=A, L2=B, L3=C``."""
    return ", ".join(f"{labels[k]}={int(items.get(k, 0))}" for k in _ITEM_KEYS)

