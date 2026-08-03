import sys

def test_movie_writer_invalid_path(anim):
    if sys.platform == "win32":
        match_str = r"\[WinError 3] .*\\\\foo\\\\bar\\\\aardvark'"
    elif sys.platform == "emscripten":
        match_str = r"\[Errno 44] .*'/foo"
    else:
        match_str = r"\[Errno 2] .*'/foo"
    with pytest.raises(FileNotFoundError, match=match_str):
        anim.save("/foo/bar/aardvark/thiscannotreallyexist.mp4",
                  writer=animation.FFMpegFileWriter())

