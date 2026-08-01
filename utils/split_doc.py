
def split_doc(string):
    '''Split the documentation into help and description.

    A two-value list is returned, of the form ``[help, desc]``. If no
    description is provided, the help is duplicated.'''
    parts = [part.strip() for part in string.split('\n\n', 1)]
    if len(parts) == 1:
        return parts * 2
    return parts

