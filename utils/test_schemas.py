
def test_schemas(obj1, obj2):
    try:
        jsonschema.validate(instance=obj1, schema=obj2)
    except jsonschema.exceptions.ValidationError:
        pass
    except jsonschema.exceptions.SchemaError:
        pass

