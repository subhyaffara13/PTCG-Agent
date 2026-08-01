
def get_block_addrs(pool_id: tuple[int, int], live_only: bool = True) -> list[int]:
    blocks = []

    for segment in get_cudagraph_segments(pool_id):
        addr = segment["address"]
        for block in segment["blocks"]:
            if block["state"] == "active_allocated" or not live_only:
                blocks.append(addr)

            addr += block["size"]

    return blocks

