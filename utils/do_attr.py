
def do_attr(
    environment: "Environment", obj: t.Any, name: str
) -> t.Union[Undefined, t.Any]:
    """Get an attribute of an object. ``foo|attr("bar")`` works like
    ``foo.bar``, but returns undefined instead of falling back to ``foo["bar"]``
    if the attribute doesn't exist.

    See :ref:`Notes on subscriptions <notes-on-subscriptions>` for more details.
    """
    # Environment.getattr will fall back to obj[name] if obj.name doesn't exist.
    # But we want to call env.getattr to get behavior such as sandboxing.
    # Determine if the attr exists first, so we know the fallback won't trigger.
    try:
        # This avoids executing properties/descriptors, but misses __getattr__
        # and __getattribute__ dynamic attrs.
        getattr_static(obj, name)
    except AttributeError:
        # This finds dynamic attrs, and we know it's not a descriptor at this point.
        if not hasattr(obj, name):
            return environment.undefined(obj=obj, name=name)

    return environment.getattr(obj, name)

