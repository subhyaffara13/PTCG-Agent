
def get_node_name_to_buf_meta(
    node_name_to_buf_name: dict[str, str],
) -> dict[str, BufMeta]:
    buf_name_to_n_node = {}
    for node_name, buf_name in node_name_to_buf_name.items():
        if buf_name not in buf_name_to_n_node:
            buf_name_to_n_node[buf_name] = OrderedSet([node_name])
        else:
            # pyrefly: ignore [missing-attribute]
            buf_name_to_n_node[buf_name].add(node_name)

    node_name_to_buf_meta = {}
    for node_name, buf_name in node_name_to_buf_name.items():
        n_node = len(buf_name_to_n_node[buf_name])
        node_name_to_buf_meta[node_name] = BufMeta(buf_name, n_node)
    return node_name_to_buf_meta

