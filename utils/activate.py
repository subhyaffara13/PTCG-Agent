import os

def activate(
    locale: str | None, path: str | os.PathLike[str] | None = None
) -> gettext_module.NullTranslations:
    """Activate internationalisation.

    Set `locale` as current locale. Search for locale in directory `path`.

    Args:
        locale (str | None): Language name, e.g. `en_GB`. If `None`, defaults to no
            translation. Similar to calling ``deactivate()``.
        path (str | pathlib.Path): Path to search for locales.

    Returns:
        dict: Translations.

    Raises:
        FileNotFoundError: If humanize cannot find the locale folder.
    """
    if locale is None or locale.startswith("en"):
        _CURRENT.locale = None
        return _TRANSLATIONS[None]

    if path is None:
        path = _get_default_locale_path()

    if path is None:
        msg = (
            "Humanize cannot determinate the default location of the 'locale' folder. "
            "You need to pass the path explicitly."
        )
        raise FileNotFoundError(msg)
    if locale not in _TRANSLATIONS:
        translation = gettext_module.translation("humanize", path, [locale])
        _TRANSLATIONS[locale] = translation
    _CURRENT.locale = locale
    return _TRANSLATIONS[locale]

