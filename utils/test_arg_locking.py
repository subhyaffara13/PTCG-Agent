
def test_arg_locking(kernel, outcome):
    # should complete without triggering races but may error

    done = 0
    arrs = [np.array([1, 2, 3]) for _ in range(1000)]

    def read_arrs(b):
        nonlocal done
        b.wait()
        try:
            kernel(arrs)
        finally:
            done += 1

    def contract_and_expand_list(b):
        b.wait()
        while done < 4:
            if len(arrs) > 10:
                arrs.pop(0)
            elif len(arrs) <= 10:
                arrs.extend([np.array([1, 2, 3]) for _ in range(1000)])

    def replace_list_items(b):
        b.wait()
        rng = np.random.RandomState()
        rng.seed(0x4d3d3d3)
        while done < 4:
            data = rng.randint(0, 1000, size=4)
            arrs[data[0]] = data[1:]

    for mutation_func in (replace_list_items, contract_and_expand_list):
        b = threading.Barrier(5)
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as tpe:
                tasks = [tpe.submit(read_arrs, b) for _ in range(4)]
                tasks.append(tpe.submit(mutation_func, b))
                for t in tasks:
                    t.result()
        except RuntimeError as e:
            if outcome == "success":
                raise
            assert "Inconsistent object during array creation?" in str(e)
            msg = "replace_list_items should not raise errors"
            assert mutation_func is contract_and_expand_list, msg
        finally:
            if len(tasks) < 5:
                b.abort()

