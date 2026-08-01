
def _extend_builtins(class_transforms):
    builtin_ast = AstroidManager().builtins_module
    for class_name, transform in class_transforms.items():
        transform(builtin_ast[class_name])

