
def _center_is_true(structure, origin):
    structure = np.asarray(structure)
    coor = tuple([oo + ss // 2 for ss, oo in zip(structure.shape,
                                                 origin)])
    return bool(structure[coor])

