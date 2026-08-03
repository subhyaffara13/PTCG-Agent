from typing import Any

def register_extra_ui_setting(name: str, annotation: Any, field: FieldInfo) -> None:
    """Register an additional UI settings field contributed by an extension package.

    ``field`` must be a ``FieldInfo`` instance — construct it directly
    (e.g. ``FieldInfo(default=..., description=...)``) rather than via
    the ``pydantic.Field`` factory, whose stub reports the default's
    type instead of ``FieldInfo`` and trips mypy at the call site.
    """
    global _EFFECTIVE_UI_SETTINGS_CLASS
    _EXTRA_UI_SETTINGS_FIELDS[name] = (annotation, field)
    ALLOWED_UI_SETTINGS_FIELDS.add(name)
    _EFFECTIVE_UI_SETTINGS_CLASS = None

