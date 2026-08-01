
def test_no_length_frames(anim):
    anim.save('unused.null', writer=NullMovieWriter())

