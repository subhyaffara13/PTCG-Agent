
def add_preprocessing_fn(
    fn: PreprocessingFunction,
):
    """Add a preprocessing function to be applied to choices before autotuning.

    Preprocessing functions are called sequentially in the order they were registered,
    with each function receiving the output of the previous one. They can filter,
    reorder, transform, or modify the list of choices in any way.

    Args:
        fn: A function that takes a list of ChoiceCaller objects and returns
            a modified list of ChoiceCaller objects.

    Example:
        def my_filter(choices):
            # Filter out choices with certain names
            return [c for c in choices if 'slow' not in c.name.lower()]

        add_preprocessing_fn(my_filter)
    """
    cache = get_algorithm_selector_cache()
    cache.add_preprocessing_fn(fn)

