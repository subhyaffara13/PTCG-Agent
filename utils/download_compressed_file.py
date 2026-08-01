
def download_compressed_file(tf_ckpt_url, ckpt_dir):
    r = requests.get(tf_ckpt_url)
    compressed_file_name = tf_ckpt_url.split("/")[-1]
    compressed_file_dir = os.path.join(ckpt_dir, compressed_file_name)
    with open(compressed_file_dir, "wb") as f:
        f.write(r.content)
    return compressed_file_dir

