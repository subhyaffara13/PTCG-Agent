
def load_mnist(directory="/tmp/mnist"):
    """Download and parse the raw MNIST dataset."""
    # CVDF mirror of http://yann.lecun.com/exdb/mnist/
    base_url = "https://storage.googleapis.com/cvdf-datasets/mnist/"

    def parse_labels(filename):
        with gzip.open(filename, "rb") as fh:
            _ = struct.unpack(">II", fh.read(8))
            return np.array(array.array("B", fh.read()), dtype=np.uint8)

    def parse_images(filename):
        with gzip.open(filename, "rb") as fh:
            _, num_data, rows, cols = struct.unpack(">IIII", fh.read(16))
            return np.array(array.array("B", fh.read()), dtype=np.int8).reshape(
                (num_data, rows, cols)
            )

    for filename in [
        "train-images-idx3-ubyte.gz",
        "train-labels-idx1-ubyte.gz",
        "t10k-images-idx3-ubyte.gz",
        "t10k-labels-idx1-ubyte.gz",
    ]:
        _download(base_url + filename, filename, directory)

    train_images = parse_images(path.join(directory, "train-images-idx3-ubyte.gz"))
    train_labels = parse_labels(path.join(directory, "train-labels-idx1-ubyte.gz"))
    test_images = parse_images(path.join(directory, "t10k-images-idx3-ubyte.gz"))
    test_labels = parse_labels(path.join(directory, "t10k-labels-idx1-ubyte.gz"))

    return (train_images, train_labels), (test_images, test_labels)

