
def _allow_property_for_view(prop_info: 'ObjectMetadataLibrary.SerializableProperty', value_: Any,
                             view_: Optional[Type[ViewType]]) -> bool:
    # First check Property is part of the View is given
    allow_for_view = False
    if view_:
        if prop_info.views and view_ in prop_info.views:
            allow_for_view = True
        elif not prop_info.views:
            allow_for_view = True
    else:
        if not prop_info.views:
            allow_for_view = True

    # Second check for inclusion of None values
    if value_ is None or (prop_info.is_array and len(value_) < 1):
        if not prop_info.include_none:
            allow_for_view = False
        elif prop_info.include_none and prop_info.include_none_views:
            allow_for_view = False
            for _v, _a in prop_info.include_none_views:
                if _v == view_:
                    allow_for_view = True

    return allow_for_view

