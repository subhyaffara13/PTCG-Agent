
def call_highest_priority(method_name: str
    ) -> Callable[[Callable[[T1, T2], T3]], Callable[[T1, T2], T3]]:
    """A decorator for binary special methods to handle _op_priority.

    Explanation
    ===========

    Binary special methods in Expr and its subclasses use a special attribute
    '_op_priority' to determine whose special method will be called to
    handle the operation. In general, the object having the highest value of
    '_op_priority' will handle the operation. Expr and subclasses that define
    custom binary special methods (__mul__, etc.) should decorate those
    methods with this decorator to add the priority logic.

    The ``method_name`` argument is the name of the method of the other class
    that will be called.  Use this decorator in the following manner::

        # Call other.__rmul__ if other._op_priority > self._op_priority
        @call_highest_priority('__rmul__')
        def __mul__(self, other):
            ...

        # Call other.__mul__ if other._op_priority > self._op_priority
        @call_highest_priority('__mul__')
        def __rmul__(self, other):
        ...
    """
    def priority_decorator(func: Callable[[T1, T2], T3]) -> Callable[[T1, T2], T3]:
        @wraps(func)
        def binary_op_wrapper(self: T1, other: T2) -> T3:
            if hasattr(other, '_op_priority'):
                if other._op_priority > self._op_priority:  # type: ignore
                    f: Union[Callable[[T1], T3], None] = getattr(other, method_name, None)
                    if f is not None:
                        return f(self)
            return func(self, other)
        return binary_op_wrapper
    return priority_decorator

