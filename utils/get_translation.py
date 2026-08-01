
def get_translation() -> gettext_module.NullTranslations:
    return _TRANSLATIONS.get(getattr(_CURRENT, "locale", None), _TRANSLATIONS[None])

