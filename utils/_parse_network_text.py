
def _parse_network_text(lines):
    """Reconstructs a graph from a network text representation.

    This is mainly used for testing.  Network text is for display, not
    serialization, as such this cannot parse all network text representations
    because node labels can be ambiguous with the glyphs and indentation used
    to represent edge structure. Additionally, there is no way to determine if
    disconnected graphs were originally directed or undirected.

    Parameters
    ----------
    lines : list or iterator of strings
        Input data in network text format

    Returns
    -------
    G: NetworkX graph
        The graph corresponding to the lines in network text format.
    """
    from itertools import chain
    from typing import Any, NamedTuple

    class ParseStackFrame(NamedTuple):
        node: Any
        indent: int
        has_vertical_child: int | None

    initial_line_iter = iter(lines)

    is_ascii = None
    is_directed = None

    ##############
    # Initial Pass
    ##############

    # Do an initial pass over the lines to determine what type of graph it is.
    # Remember what these lines were, so we can reiterate over them in the
    # parsing pass.
    initial_lines = []
    try:
        first_line = next(initial_line_iter)
    except StopIteration:
        ...
    else:
        initial_lines.append(first_line)
        # The first character indicates if it is an ASCII or UTF graph
        first_char = first_line[0]
        if first_char in {
            UtfBaseGlyphs.empty,
            UtfBaseGlyphs.newtree_mid[0],
            UtfBaseGlyphs.newtree_last[0],
        }:
            is_ascii = False
        elif first_char in {
            AsciiBaseGlyphs.empty,
            AsciiBaseGlyphs.newtree_mid[0],
            AsciiBaseGlyphs.newtree_last[0],
        }:
            is_ascii = True
        else:
            raise AssertionError(f"Unexpected first character: {first_char}")

    if is_ascii:
        directed_glyphs = AsciiDirectedGlyphs.as_dict()
        undirected_glyphs = AsciiUndirectedGlyphs.as_dict()
    else:
        directed_glyphs = UtfDirectedGlyphs.as_dict()
        undirected_glyphs = UtfUndirectedGlyphs.as_dict()

    # For both directed / undirected glyphs, determine which glyphs never
    # appear as substrings in the other undirected / directed glyphs.  Glyphs
    # with this property unambiguously indicates if a graph is directed /
    # undirected.
    directed_items = set(directed_glyphs.values())
    undirected_items = set(undirected_glyphs.values())
    unambiguous_directed_items = []
    for item in directed_items:
        other_items = undirected_items
        other_supersets = [other for other in other_items if item in other]
        if not other_supersets:
            unambiguous_directed_items.append(item)
    unambiguous_undirected_items = []
    for item in undirected_items:
        other_items = directed_items
        other_supersets = [other for other in other_items if item in other]
        if not other_supersets:
            unambiguous_undirected_items.append(item)

    for line in initial_line_iter:
        initial_lines.append(line)
        if any(item in line for item in unambiguous_undirected_items):
            is_directed = False
            break
        elif any(item in line for item in unambiguous_directed_items):
            is_directed = True
            break

    if is_directed is None:
        # Not enough information to determine, choose undirected by default
        is_directed = False

    glyphs = directed_glyphs if is_directed else undirected_glyphs

    # the backedge symbol by itself can be ambiguous, but with spaces around it
    # becomes unambiguous.
    backedge_symbol = " " + glyphs["backedge"] + " "

    # Reconstruct an iterator over all of the lines.
    parsing_line_iter = chain(initial_lines, initial_line_iter)

    ##############
    # Parsing Pass
    ##############

    edges = []
    nodes = []
    is_empty = None

    noparent = object()  # sentinel value

    # keep a stack of previous nodes that could be parents of subsequent nodes
    stack = [ParseStackFrame(noparent, -1, None)]

    for line in parsing_line_iter:
        if line == glyphs["empty"]:
            # If the line is the empty glyph, we are done.
            # There shouldn't be anything else after this.
            is_empty = True
            continue

        if backedge_symbol in line:
            # This line has one or more backedges, separate those out
            node_part, backedge_part = line.split(backedge_symbol)
            backedge_nodes = [u.strip() for u in backedge_part.split(", ")]
            # Now the node can be parsed
            node_part = node_part.rstrip()
            prefix, node = node_part.rsplit(" ", 1)
            node = node.strip()
            # Add the backedges to the edge list
            edges.extend([(u, node) for u in backedge_nodes])
        else:
            # No backedge, the tail of this line is the node
            prefix, node = line.rsplit(" ", 1)
            node = node.strip()

        prev = stack.pop()

        if node in glyphs["vertical_edge"]:
            # Previous node is still the previous node, but we know it will
            # have exactly one child, which will need to have its nesting level
            # adjusted.
            modified_prev = ParseStackFrame(
                prev.node,
                prev.indent,
                True,
            )
            stack.append(modified_prev)
            continue

        # The length of the string before the node characters give us a hint
        # about our nesting level. The only case where this doesn't work is
        # when there are vertical chains, which is handled explicitly.
        indent = len(prefix)
        curr = ParseStackFrame(node, indent, None)

        if prev.has_vertical_child:
            # In this case we know prev must be the parent of our current line,
            # so we don't have to search the stack. (which is good because the
            # indentation check wouldn't work in this case).
            ...
        else:
            # If the previous node nesting-level is greater than the current
            # nodes nesting-level than the previous node was the end of a path,
            # and is not our parent. We can safely pop nodes off the stack
            # until we find one with a comparable nesting-level, which is our
            # parent.
            while curr.indent <= prev.indent:
                prev = stack.pop()

        if node == "...":
            # The current previous node is no longer a valid parent,
            # keep it popped from the stack.
            stack.append(prev)
        else:
            # The previous and current nodes may still be parents, so add them
            # back onto the stack.
            stack.append(prev)
            stack.append(curr)

            # Add the node and the edge to its parent to the node / edge lists.
            nodes.append(curr.node)
            if prev.node is not noparent:
                edges.append((prev.node, curr.node))

    if is_empty:
        # Sanity check
        assert len(nodes) == 0

    # Reconstruct the graph
    cls = nx.DiGraph if is_directed else nx.Graph
    new = cls()
    new.add_nodes_from(nodes)
    new.add_edges_from(edges)
    return new

