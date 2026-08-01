
def generate_feeds(sess, symbolic_dims: dict | None = None):
    feeds = {}
    symbolic_dims = symbolic_dims or {}
    for input_meta in sess.get_inputs():
        # replace any symbolic dimensions
        shape = []
        for dim in input_meta.shape:
            if not dim:
                # unknown dim
                shape.append(1)
            elif isinstance(dim, str):
                # symbolic dim. see if we have a value otherwise use 1
                if dim in symbolic_dims:
                    shape.append(int(symbolic_dims[dim]))
                else:
                    shape.append(1)
            else:
                shape.append(dim)

        if input_meta.type in float_dict:
            feeds[input_meta.name] = np.random.rand(*shape).astype(float_dict[input_meta.type])
        elif input_meta.type in integer_dict:
            feeds[input_meta.name] = np.random.uniform(high=1000, size=tuple(shape)).astype(
                integer_dict[input_meta.type]
            )
        elif input_meta.type == "tensor(bool)":
            feeds[input_meta.name] = np.random.randint(2, size=tuple(shape)).astype("bool")
        else:
            print(f"unsupported input type {input_meta.type} for input {input_meta.name}")
            sys.exit(-1)
    return feeds

