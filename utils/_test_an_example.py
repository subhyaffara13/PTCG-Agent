
def _test_an_example(our_hint, example_name):
    all_examples = _get_all_examples()
    for example in all_examples:
        if example['example_name'] == example_name:
            _test_particular_example(our_hint, example)

