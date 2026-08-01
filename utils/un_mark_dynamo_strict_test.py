
def unMarkDynamoStrictTest(cls=None):
    def decorator(cls):
        cls.dynamo_strict = False
        return cls

    if cls is None:
        return decorator
    else:
        return decorator(cls)

