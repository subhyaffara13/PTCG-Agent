
def _get_priority_settings() -> "PriorityReservationSettings":
    """
    Get the priority reservation settings, guaranteed to be non-None.

    The settings are lazy-loaded in litellm.__init__ and always return an instance.
    This helper provides proper type narrowing for mypy.
    """
    settings = litellm.priority_reservation_settings
    if settings is None:
        # This should never happen due to lazy loading, but satisfy mypy
        from litellm.types.utils import PriorityReservationSettings

        return PriorityReservationSettings()
    return settings

