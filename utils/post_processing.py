
def post_processing(outputs_path, outputs_path_other):
    # Compare outputs with e.g. fp16 and fp32
    record = {}
    if_close = {}

    import glob  # noqa: PLC0415

    for filename in glob.glob(os.path.join(outputs_path, "*.tensorproto")):
        filename_other = os.path.join(outputs_path_other, Path(filename).name)
        if not os.path.exists(filename_other):
            continue
        with open(filename, "rb") as f:
            tensor = TensorProto()
            tensor.ParseFromString(f.read())
            array = numpy_helper.to_array(tensor)
            with open(filename_other, "rb") as f:  # noqa: PLW2901
                tensor_other = TensorProto()
                tensor_other.ParseFromString(f.read())
                array_other = numpy_helper.to_array(tensor_other)
                if array_other.size == 0:
                    continue
                diff = numpy.average(numpy.abs(array_other - array) / (numpy.abs(array_other) + 1e-6))
                if math.isnan(diff):
                    continue
                record[Path(filename).name.split(".")[0]] = diff
                if_close[Path(filename).name.split(".")[0]] = numpy.allclose(array, array_other, rtol=1e-04, atol=1e-04)

    results = ["Node\tDiff\tClose"]
    for k, v in sorted(record.items(), key=lambda x: x[1], reverse=True):
        results.append(f"{k}\t{v}\t{if_close[k]}")
    for line in results:
        print(line)

