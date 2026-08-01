
def _get_effective_ui_settings_class() -> Type[UISettings]:
    """Return UISettings with any extension-registered fields merged in.

    Memoized — pydantic ``create_model`` runs metaclass + schema work
    each call, so we cache until a new registration invalidates it.
    """
    global _EFFECTIVE_UI_SETTINGS_CLASS
    if _EFFECTIVE_UI_SETTINGS_CLASS is not None:
        return _EFFECTIVE_UI_SETTINGS_CLASS
    if not _EXTRA_UI_SETTINGS_FIELDS:
        return UISettings
    _EFFECTIVE_UI_SETTINGS_CLASS = create_model(  # type: ignore[call-overload]
        "EffectiveUISettings",
        __base__=UISettings,
        __doc__=UISettings.__doc__,
        **_EXTRA_UI_SETTINGS_FIELDS,
    )
    return _EFFECTIVE_UI_SETTINGS_CLASS

