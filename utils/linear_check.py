
def linear_check(tensor_type, module_instance):
    """
    Checks that an input tensor type satisfies the conditions for linear operation
    and returns the output type based on in and out features given by module_instance
    """
    if len(tensor_type.__args__) >= 2:
        if is_consistent(module_instance.in_features, tensor_type.__args__[-1]):
            new_type_args = list(tensor_type.__args__)
            new_type_args[-1] = module_instance.out_features
            return TensorType(tuple(new_type_args))
        else:
            raise TypeError(
                f"Inconsistent {module_instance.in_features} and {tensor_type.__args__[-1]} in {module_instance}"
            )
    else:
        raise TypeError(f"Type {tensor_type} must have rank 2 or more.")

