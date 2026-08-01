
def _parse_node_line(line):
    line_items = line.split(" ")
    node_id, addr, flags, master_id, ping, pong, epoch, connected = line.split(" ")[:8]
    ip = addr.split("@")[0]
    hostname = addr.split("@")[1].split(",")[1] if "@" in addr and "," in addr else ""
    node_dict = {
        "node_id": node_id,
        "hostname": hostname,
        "flags": flags,
        "master_id": master_id,
        "last_ping_sent": ping,
        "last_pong_rcvd": pong,
        "epoch": epoch,
        "slots": [],
        "migrations": [],
        "connected": True if connected == "connected" else False,
    }
    if len(line_items) >= 9:
        slots, migrations = _parse_slots(line_items[8:])
        node_dict["slots"], node_dict["migrations"] = slots, migrations
    return ip, node_dict

