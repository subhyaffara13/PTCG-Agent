import sys

def test_movie_writer_registry():
    assert len(animation.writers._registered) > 0
    mpl.rcParams['animation.ffmpeg_path'] = "not_available_ever_xxxx"
    assert not animation.writers.is_available("ffmpeg")
    # something guaranteed to be available in path and exits immediately
    bin = "true" if sys.platform != 'win32' else "where"
    mpl.rcParams['animation.ffmpeg_path'] = bin
    assert animation.writers.is_available("ffmpeg")

