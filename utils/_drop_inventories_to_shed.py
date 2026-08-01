
def _drop_inventories_to_shed(private, capacity):
    """Drop every per-farmer inventory into the shed up to `capacity`; overflow is discarded.
    Seeds are tracked separately in private["seeds"] and don't pass through the shed."""
    shed = private["shed"]
    for inv in private["inventories"]:
        for item, n in list(inv.items()):
            if n <= 0:
                del inv[item]
                continue
            current = sum(v for k, v in shed.items())
            room = max(0, capacity - current)
            take = min(n, room)
            if take > 0:
                shed[item] = shed.get(item, 0) + take
            del inv[item]

