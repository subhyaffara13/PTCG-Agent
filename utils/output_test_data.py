import os

def output_test_data(directory: str, inputs: dict[str, np.ndarray]):
    """Output input tensors of test data to a directory

    Args:
        directory (str): path of a directory
        inputs (Dict[str, np.ndarray]): map from input name to value
    """
    if not os.path.exists(directory):
        try:
            os.mkdir(directory)
        except OSError:
            print(f"Creation of the directory {directory} failed")
        else:
            print(f"Successfully created the directory {directory} ")
    else:
        print(f"Warning: directory {directory} existed. Files will be overwritten.")

    for index, (name, data) in enumerate(inputs.items()):
        tensor = numpy_helper.from_array(data, name)
        with open(os.path.join(directory, f"input_{index}.pb"), "wb") as file:
            file.write(tensor.SerializeToString())

