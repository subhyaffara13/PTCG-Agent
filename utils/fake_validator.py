
def fake_validator(*errors):
    errors = list(reversed(errors))

    class FakeValidator:
        def __init__(self, *args, **kwargs):
            pass

        def iter_errors(self, instance):
            if errors:
                return errors.pop()
            return []  # pragma: no cover

        @classmethod
        def check_schema(self, schema):
            pass

    return FakeValidator

