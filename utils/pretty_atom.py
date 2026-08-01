
def pretty_atom(atom_name, default=None, printer=None):
    """return pretty representation of an atom"""
    if _use_unicode:
        if printer is not None and atom_name == 'ImaginaryUnit' and printer._settings['imaginary_unit'] == 'j':
            return U('DOUBLE-STRUCK ITALIC SMALL J')
        else:
            return atoms_table[atom_name]
    else:
        if default is not None:
            return default

        raise KeyError('only unicode')  # send it default printer

