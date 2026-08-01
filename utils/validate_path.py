
def validate_path(path: str, has_scheme: bool, has_authority: bool) -> None:
    """
    Path validation rules that depend on if the URL contains
    a scheme or authority component.

    See https://datatracker.ietf.org/doc/html/rfc3986.html#section-3.3
    """
    if has_authority:
        # If a URI contains an authority component, then the path component
        # must either be empty or begin with a slash ("/") character."
        if path and not path.startswith("/"):
            raise InvalidURL("For absolute URLs, path must be empty or begin with '/'")

    if not has_scheme and not has_authority:
        # If a URI does not contain an authority component, then the path cannot begin
        # with two slash characters ("//").
        if path.startswith("//"):
            raise InvalidURL("Relative URLs cannot have a path starting with '//'")

        # In addition, a URI reference (Section 4.1) may be a relative-path reference,
        # in which case the first path segment cannot contain a colon (":") character.
        if path.startswith(":"):
            raise InvalidURL("Relative URLs cannot have a path starting with ':'")


def validate_path(G, s, t, soln_len, path):
    assert path[0] == s
    assert path[-1] == t
    assert soln_len == sum(
        G[u][v].get("weight", 1) for u, v in zip(path[:-1], path[1:])
    )


def validate_path(G, s, t, soln_len, path, weight="weight"):
    assert path[0] == s
    assert path[-1] == t

    if callable(weight):
        weight_f = weight
    else:
        if G.is_multigraph():

            def weight_f(u, v, d):
                return min(e.get(weight, 1) for e in d.values())

        else:

            def weight_f(u, v, d):
                return d.get(weight, 1)

    computed = sum(weight_f(u, v, G[u][v]) for u, v in pairwise(path))
    assert soln_len == computed

