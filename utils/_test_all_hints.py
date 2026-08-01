
def _test_all_hints(runxfail=False):
    all_hints = list(allhints)+["default"]
    all_examples = _get_all_examples()

    for our_hint in all_hints:
        if our_hint.endswith('_Integral') or 'series' in our_hint:
            continue
        _test_all_examples_for_one_hint(our_hint, all_examples, runxfail)

