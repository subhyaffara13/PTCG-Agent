
def _define_reflectable(orig_method_name: str) -> None:
    method_name = f"__r{orig_method_name.strip('_')}__"

    def impl(self: "Proxy", rhs: Any) -> "Proxy":
        target = getattr(operator, orig_method_name)
        return self.tracer.create_proxy("call_function", target, (rhs, self), {})

    impl.__name__ = method_name
    impl.__qualname__ = method_name
    setattr(Proxy, method_name, impl)

