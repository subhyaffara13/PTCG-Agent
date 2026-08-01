
def _ffmpeg_stream(ffmpeg_command, buflen: int):
    """
    Internal function to create the generator of data through ffmpeg
    """
    bufsize = 2**24  # 16Mo
    try:
        with subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, bufsize=bufsize) as ffmpeg_process:
            while True:
                raw = ffmpeg_process.stdout.read(buflen)
                if raw == b"":
                    break
                yield raw
    except FileNotFoundError as error:
        raise ValueError("ffmpeg was not found but is required to stream audio files from filename") from error

