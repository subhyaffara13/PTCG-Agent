
def get_long_model_name(model: TypeModelOrEnum) -> str:
    return f'{model.__module__}__{model.__qualname__}'.replace('.', '__')

