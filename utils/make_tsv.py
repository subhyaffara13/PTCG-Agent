
def make_tsv(metadata, save_path, metadata_header=None) -> None:
    if not metadata_header:
        metadata = [str(x) for x in metadata]
    else:
        if len(metadata_header) != len(
            metadata[0]
        ):
            raise AssertionError("len of header must be equal to the number of columns in metadata")
        metadata = ["\t".join(str(e) for e in l) for l in [metadata_header] + metadata]

    metadata_bytes = tf.compat.as_bytes("\n".join(metadata) + "\n")
    with tf.io.gfile.GFile(_gfile_join(save_path, "metadata.tsv"), "wb") as f:
        f.write(metadata_bytes)

