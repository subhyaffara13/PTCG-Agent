import re

def parse_gml_lines(lines, label, destringizer):
    """Parse GML `lines` into a graph."""

    def tokenize():
        patterns = [
            r"[A-Za-z][0-9A-Za-z_]*\b",  # keys
            # reals
            r"[+-]?(?:[0-9]*\.[0-9]+|[0-9]+\.[0-9]*|INF)(?:[Ee][+-]?[0-9]+)?",
            r"[+-]?[0-9]+",  # ints
            r'".*?"',  # strings
            r"\[",  # dict start
            r"\]",  # dict end
            r"#.*$|\s+",  # comments and whitespaces
        ]
        tokens = re.compile("|".join(f"({pattern})" for pattern in patterns))
        lineno = 0
        multilines = []  # entries spread across multiple lines
        for line in lines:
            pos = 0

            # deal with entries spread across multiple lines
            #
            # should we actually have to deal with escaped "s then do it here
            if multilines:
                multilines.append(line.strip())
                if line[-1] == '"':  # closing multiline entry
                    # multiline entries will be joined by space. cannot
                    # reintroduce newlines as this will break the tokenizer
                    line = " ".join(multilines)
                    multilines = []
                else:  # continued multiline entry
                    lineno += 1
                    continue
            else:
                if line.count('"') == 1:  # opening multiline entry
                    if line.strip()[0] != '"' and line.strip()[-1] != '"':
                        # since we expect something like key "value", the " should not be found at ends
                        # otherwise tokenizer will pick up the formatting mistake.
                        multilines = [line.rstrip()]
                        lineno += 1
                        continue

            length = len(line)

            while pos < length:
                match = tokens.match(line, pos)
                if match is None:
                    m = f"cannot tokenize {line[pos:]} at ({lineno + 1}, {pos + 1})"
                    raise NetworkXError(m)
                for i in range(len(patterns)):
                    group = match.group(i + 1)
                    if group is not None:
                        if i == 0:  # keys
                            value = group.rstrip()
                        elif i == 1:  # reals
                            value = float(group)
                        elif i == 2:  # ints
                            value = int(group)
                        else:
                            value = group
                        if i != 6:  # comments and whitespaces
                            yield Token(Pattern(i), value, lineno + 1, pos + 1)
                        pos += len(group)
                        break
            lineno += 1
        yield Token(None, None, lineno + 1, 1)  # EOF

    def unexpected(curr_token, expected):
        category, value, lineno, pos = curr_token
        value = repr(value) if value is not None else "EOF"
        raise NetworkXError(f"expected {expected}, found {value} at ({lineno}, {pos})")

    def consume(curr_token, category, expected):
        if curr_token.category == category:
            return next(tokens)
        unexpected(curr_token, expected)

    def parse_kv(curr_token):
        dct = defaultdict(list)
        while curr_token.category == Pattern.KEYS:
            key = curr_token.value
            curr_token = next(tokens)
            category = curr_token.category
            if category == Pattern.REALS or category == Pattern.INTS:
                value = curr_token.value
                curr_token = next(tokens)
            elif category == Pattern.STRINGS:
                value = unescape(curr_token.value[1:-1])
                if destringizer:
                    try:
                        value = destringizer(value)
                    except ValueError:
                        pass
                # Special handling for empty lists and tuples
                if value == "()":
                    value = ()
                if value == "[]":
                    value = []
                curr_token = next(tokens)
            elif category == Pattern.DICT_START:
                curr_token, value = parse_dict(curr_token)
            else:
                # Allow for string convertible id and label values
                if key in ("id", "label", "source", "target"):
                    try:
                        # String convert the token value
                        value = unescape(str(curr_token.value))
                        if destringizer:
                            try:
                                value = destringizer(value)
                            except ValueError:
                                pass
                        curr_token = next(tokens)
                    except Exception:
                        msg = (
                            "an int, float, string, '[' or string"
                            + " convertible ASCII value for node id or label"
                        )
                        unexpected(curr_token, msg)
                # Special handling for nan and infinity.  Since the gml language
                # defines unquoted strings as keys, the numeric and string branches
                # are skipped and we end up in this special branch, so we need to
                # convert the current token value to a float for NAN and plain INF.
                # +/-INF are handled in the pattern for 'reals' in tokenize().  This
                # allows labels and values to be nan or infinity, but not keys.
                elif curr_token.value in {"NAN", "INF"}:
                    value = float(curr_token.value)
                    curr_token = next(tokens)
                else:  # Otherwise error out
                    unexpected(curr_token, "an int, float, string or '['")
            dct[key].append(value)

        def clean_dict_value(value):
            if not isinstance(value, list):
                return value
            if len(value) == 1:
                return value[0]
            if value[0] == LIST_START_VALUE:
                return value[1:]
            return value

        dct = {key: clean_dict_value(value) for key, value in dct.items()}
        return curr_token, dct

    def parse_dict(curr_token):
        # dict start
        curr_token = consume(curr_token, Pattern.DICT_START, "'['")
        # dict contents
        curr_token, dct = parse_kv(curr_token)
        # dict end
        curr_token = consume(curr_token, Pattern.DICT_END, "']'")
        return curr_token, dct

    def parse_graph():
        curr_token, dct = parse_kv(next(tokens))
        if curr_token.category is not None:  # EOF
            unexpected(curr_token, "EOF")
        if "graph" not in dct:
            raise NetworkXError("input contains no graph")
        graph = dct["graph"]
        if isinstance(graph, list):
            raise NetworkXError("input contains more than one graph")
        return graph

    tokens = tokenize()
    graph = parse_graph()

    directed = graph.pop("directed", False)
    multigraph = graph.pop("multigraph", False)
    if not multigraph:
        G = nx.DiGraph() if directed else nx.Graph()
    else:
        G = nx.MultiDiGraph() if directed else nx.MultiGraph()
    graph_attr = {k: v for k, v in graph.items() if k not in ("node", "edge")}
    G.graph.update(graph_attr)

    def pop_attr(dct, category, attr, i):
        try:
            return dct.pop(attr)
        except KeyError as err:
            raise NetworkXError(f"{category} #{i} has no {attr!r} attribute") from err

    nodes = graph.get("node", [])
    mapping = {}
    node_labels = set()
    for i, node in enumerate(nodes if isinstance(nodes, list) else [nodes]):
        id = pop_attr(node, "node", "id", i)
        if id in G:
            raise NetworkXError(f"node id {id!r} is duplicated")
        if label is not None and label != "id":
            node_label = pop_attr(node, "node", label, i)
            if node_label in node_labels:
                raise NetworkXError(f"node label {node_label!r} is duplicated")
            node_labels.add(node_label)
            mapping[id] = node_label
        G.add_node(id, **node)

    edges = graph.get("edge", [])
    for i, edge in enumerate(edges if isinstance(edges, list) else [edges]):
        source = pop_attr(edge, "edge", "source", i)
        target = pop_attr(edge, "edge", "target", i)
        if source not in G:
            raise NetworkXError(f"edge #{i} has undefined source {source!r}")
        if target not in G:
            raise NetworkXError(f"edge #{i} has undefined target {target!r}")
        if not multigraph:
            if not G.has_edge(source, target):
                G.add_edge(source, target, **edge)
            else:
                arrow = "->" if directed else "--"
                msg = f"edge #{i} ({source!r}{arrow}{target!r}) is duplicated"
                raise nx.NetworkXError(msg)
        else:
            key = edge.pop("key", None)
            if key is not None and G.has_edge(source, target, key):
                arrow = "->" if directed else "--"
                msg = f"edge #{i} ({source!r}{arrow}{target!r}, {key!r})"
                msg2 = 'Hint: If multigraph add "multigraph 1" to file header.'
                raise nx.NetworkXError(msg + " is duplicated\n" + msg2)
            G.add_edge(source, target, key, **edge)

    if label is not None and label != "id":
        G = nx.relabel_nodes(G, mapping)
    return G

