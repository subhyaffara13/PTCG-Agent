
def _get_orientation_from_location(location):
    return _api.getitem_checked(
        {None: None, "left": "vertical", "right": "vertical",
         "top": "horizontal", "bottom": "horizontal"}, location=location)

