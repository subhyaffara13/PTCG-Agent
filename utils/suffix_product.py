
def suffix_product(a: IntTuple, init: IntTuple = 1) -> IntTuple:
    # TODO: With all these length asserts, may want to create a zip_strict wrapper.
    if is_tuple(a):
        if is_tuple(init):  # tuple tuple
            if len(a) != len(init):
                raise AssertionError
            return tuple(suffix_product(x, i) for x, i in zip(a, init))
        else:  # tuple "int"
            # Process from right to left for lexicographic ordering
            # r = [prefix_product(a[len(a)-1],init)] +
            # [prefix_product(a[i],init := init * product(a[i+1])) for i in range(len(a)-1,0)].reverse()
            r = []

            # Calculate products from right to left, appending to list
            for i in range(len(a) - 1, -1, -1):
                r.append(suffix_product(a[i], init))
                init = init * product(a[i])

            # Reverse to get correct lexicographic order
            r.reverse()
            return tuple(r)
    else:
        if is_tuple(init):  # "int" tuple
            raise AssertionError("Invalid combination: int with tuple init")
        else:  # "int" "int"
            return init

