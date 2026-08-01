
def _is_django_cached_property(runtime: Any) -> bool:  # pragma: no cover
    # This is a special case for
    # https://docs.djangoproject.com/en/5.2/ref/utils/#django.utils.functional.cached_property
    # This is needed in `django-stubs` project:
    # https://github.com/typeddjango/django-stubs
    if type(runtime).__name__ != "cached_property":
        return False
    try:
        return bool(runtime.func)
    except Exception:
        return False

