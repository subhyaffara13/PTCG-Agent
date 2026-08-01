
def _get_ticklocation_from_orientation(orientation):
    return _api.getitem_checked(
        {None: "right", "vertical": "right", "horizontal": "bottom"},
        orientation=orientation)

