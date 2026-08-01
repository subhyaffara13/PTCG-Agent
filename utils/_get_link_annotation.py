
def _get_link_annotation(gc, x, y, width, height, angle=0):
    """
    Create a link annotation object for embedding URLs.
    """
    quadpoints, rect = _get_coordinates_of_block(x, y, width, height, angle)
    link_annotation = {
        'Type': Name('Annot'),
        'Subtype': Name('Link'),
        'Rect': rect,
        'Border': [0, 0, 0],
        'A': {
            'S': Name('URI'),
            'URI': gc.get_url(),
        },
    }
    if angle % 90:
        # Add QuadPoints
        link_annotation['QuadPoints'] = quadpoints
    return link_annotation

