
def get_path(hatchpattern, density=6):
    """
    Given a hatch specifier, *hatchpattern*, generates Path to render
    the hatch in a unit square.  *density* is the number of lines per
    unit square.
    """
    density = int(density)

    patterns = [hatch_type(hatchpattern, density)
                for hatch_type in _hatch_types]
    num_vertices = sum([pattern.num_vertices for pattern in patterns])

    if num_vertices == 0:
        return Path(np.empty((0, 2)))

    vertices = np.empty((num_vertices, 2))
    codes = np.empty(num_vertices, Path.code_type)

    cursor = 0
    for pattern in patterns:
        if pattern.num_vertices != 0:
            vertices_chunk = vertices[cursor:cursor + pattern.num_vertices]
            codes_chunk = codes[cursor:cursor + pattern.num_vertices]
            pattern.set_vertices_and_codes(vertices_chunk, codes_chunk)
            cursor += pattern.num_vertices

    return Path(vertices, codes)


def get_path(
    basename: str, extension: str, specified_dir: str = ""
) -> tuple[str, str, str]:
    if specified_dir:
        if os.path.isabs(specified_dir):
            subdir = specified_dir
        else:
            subdir = os.path.join(cache_dir(), specified_dir)
    else:
        subdir = os.path.join(cache_dir(), basename[1:3])
    path = os.path.join(subdir, f"{basename}.{extension}")
    return basename, subdir, path


def get_path(
    o: object, seen: dict[int, object], parents: dict[int, tuple[int, object]]
) -> list[tuple[object, object]]:
    path = []
    while id(o) in parents:
        pid, attr = parents[id(o)]
        o = seen[pid]
        path.append((attr, o))
    path.reverse()
    return path

