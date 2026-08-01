
def _make_class_factory(mixin_class, fmt, attr_name=None):
    """
    Return a function that creates picklable classes inheriting from a mixin.

    After ::

        factory = _make_class_factory(FooMixin, fmt, attr_name)
        FooAxes = factory(Axes)

    ``Foo`` is a class that inherits from ``FooMixin`` and ``Axes`` and **is
    picklable** (picklability is what differentiates this from a plain call to
    `type`).  Its ``__name__`` is set to ``fmt.format(Axes.__name__)`` and the
    base class is stored in the ``attr_name`` attribute, if not None.

    Moreover, the return value of ``factory`` is memoized: calls with the same
    ``Axes`` class always return the same subclass.
    """

    @functools.cache
    def class_factory(axes_class):
        # if we have already wrapped this class, declare victory!
        if issubclass(axes_class, mixin_class):
            return axes_class

        # The parameter is named "axes_class" for backcompat but is really just
        # a base class; no axes semantics are used.
        base_class = axes_class

        class subcls(mixin_class, base_class):
            # Better approximation than __module__ = "matplotlib.cbook".
            __module__ = mixin_class.__module__

            def __reduce__(self):
                return (_picklable_class_constructor,
                        (mixin_class, fmt, attr_name, base_class),
                        self.__getstate__())

        subcls.__name__ = subcls.__qualname__ = fmt.format(base_class.__name__)
        if attr_name is not None:
            setattr(subcls, attr_name, base_class)
        return subcls

    class_factory.__module__ = mixin_class.__module__
    return class_factory

