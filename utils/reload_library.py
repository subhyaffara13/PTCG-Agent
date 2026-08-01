
def reload_library():
    """Reload the style library."""
    library.clear()
    library.update(_update_user_library(_base_library.copy()))
    available[:] = sorted(name for name in library if not name.startswith('_'))

