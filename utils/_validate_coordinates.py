
def _validate_coordinates(coordinates=None, speeds=None, check_duplicates=True,
                          is_dynamicsymbols=True, u_auxiliary=None):
    """Validate the generalized coordinates and generalized speeds.

    Parameters
    ==========
    coordinates : iterable, optional
        Generalized coordinates to be validated.
    speeds : iterable, optional
        Generalized speeds to be validated.
    check_duplicates : bool, optional
        Checks if there are duplicates in the generalized coordinates and
        generalized speeds. If so it will raise a ValueError. The default is
        True.
    is_dynamicsymbols : iterable, optional
        Checks if all the generalized coordinates and generalized speeds are
        dynamicsymbols. If any is not a dynamicsymbol, a ValueError will be
        raised. The default is True.
    u_auxiliary : iterable, optional
        Auxiliary generalized speeds to be validated.

    """
    t_set = {dynamicsymbols._t}
    # Convert input to iterables
    if coordinates is None:
        coordinates = []
    elif not iterable(coordinates):
        coordinates = [coordinates]
    if speeds is None:
        speeds = []
    elif not iterable(speeds):
        speeds = [speeds]
    if u_auxiliary is None:
        u_auxiliary = []
    elif not iterable(u_auxiliary):
        u_auxiliary = [u_auxiliary]

    msgs = []
    if check_duplicates:  # Check for duplicates
        seen = set()
        coord_duplicates = {x for x in coordinates if x in seen or seen.add(x)}
        seen = set()
        speed_duplicates = {x for x in speeds if x in seen or seen.add(x)}
        seen = set()
        aux_duplicates = {x for x in u_auxiliary if x in seen or seen.add(x)}
        overlap_coords = set(coordinates).intersection(speeds)
        overlap_aux = set(coordinates).union(speeds).intersection(u_auxiliary)
        if coord_duplicates:
            msgs.append(f'The generalized coordinates {coord_duplicates} are '
                        f'duplicated, all generalized coordinates should be '
                        f'unique.')
        if speed_duplicates:
            msgs.append(f'The generalized speeds {speed_duplicates} are '
                        f'duplicated, all generalized speeds should be unique.')
        if aux_duplicates:
            msgs.append(f'The auxiliary speeds {aux_duplicates} are duplicated,'
                        f' all auxiliary speeds should be unique.')
        if overlap_coords:
            msgs.append(f'{overlap_coords} are defined as both generalized '
                        f'coordinates and generalized speeds.')
        if overlap_aux:
            msgs.append(f'The auxiliary speeds {overlap_aux} are also defined '
                        f'as generalized coordinates or generalized speeds.')
    if is_dynamicsymbols:  # Check whether all coordinates are dynamicsymbols
        for coordinate in coordinates:
            if not (isinstance(coordinate, (AppliedUndef, Derivative)) and
                    coordinate.free_symbols == t_set):
                msgs.append(f'Generalized coordinate "{coordinate}" is not a '
                            f'dynamicsymbol.')
        for speed in speeds:
            if not (isinstance(speed, (AppliedUndef, Derivative)) and
                    speed.free_symbols == t_set):
                msgs.append(
                    f'Generalized speed "{speed}" is not a dynamicsymbol.')
        for aux in u_auxiliary:
            if not (isinstance(aux, (AppliedUndef, Derivative)) and
                    aux.free_symbols == t_set):
                msgs.append(
                    f'Auxiliary speed "{aux}" is not a dynamicsymbol.')
    if msgs:
        raise ValueError('\n'.join(msgs))

