
def install_method(method_name):
    def _not_implemented(self, *args, **kwargs):
        raise NotImplementedError(
            f"Object '{self._name}' was mocked out during packaging but it is being used in {method_name}"
        )

    setattr(MockedObject, method_name, _not_implemented)

