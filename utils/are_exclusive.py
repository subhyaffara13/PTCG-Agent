
def are_exclusive(stmt1, stmt2, exceptions: list[str] | None = None) -> bool:
    """return true if the two given statements are mutually exclusive

    `exceptions` may be a list of exception names. If specified, discard If
    branches and check one of the statement is in an exception handler catching
    one of the given exceptions.

    algorithm :
     1) index stmt1's parents
     2) climb among stmt2's parents until we find a common parent
     3) if the common parent is a If or Try statement, look if nodes are
        in exclusive branches
    """
    # index stmt1's parents
    stmt1_parents = {}
    children = {}
    previous = stmt1
    for node in stmt1.node_ancestors():
        stmt1_parents[node] = 1
        children[node] = previous
        previous = node
    # climb among stmt2's parents until we find a common parent
    previous = stmt2
    for node in stmt2.node_ancestors():
        if node in stmt1_parents:
            # if the common parent is a If or Try statement, look if
            # nodes are in exclusive branches
            if isinstance(node, If) and exceptions is None:
                c2attr, c2node = node.locate_child(previous)
                c1attr, c1node = node.locate_child(children[node])
                if "test" in (c1attr, c2attr):
                    # If any node is `If.test`, then it must be inclusive with
                    # the other node (`If.body` and `If.orelse`)
                    return False
                if c1attr != c2attr:
                    # different `If` branches (`If.body` and `If.orelse`)
                    return True
            elif isinstance(node, Try):
                c2attr, c2node = node.locate_child(previous)
                c1attr, c1node = node.locate_child(children[node])
                if c1node is not c2node:
                    first_in_body_caught_by_handlers = (
                        c2attr == "handlers"
                        and c1attr == "body"
                        and previous.catch(exceptions)
                    )
                    second_in_body_caught_by_handlers = (
                        c2attr == "body"
                        and c1attr == "handlers"
                        and children[node].catch(exceptions)
                    )
                    first_in_else_other_in_handlers = (
                        c2attr == "handlers" and c1attr == "orelse"
                    )
                    second_in_else_other_in_handlers = (
                        c2attr == "orelse" and c1attr == "handlers"
                    )
                    if any(
                        (
                            first_in_body_caught_by_handlers,
                            second_in_body_caught_by_handlers,
                            first_in_else_other_in_handlers,
                            second_in_else_other_in_handlers,
                        )
                    ):
                        return True
                elif c2attr == "handlers" and c1attr == "handlers":
                    return previous is not children[node]
            return False
        previous = node
    return False

