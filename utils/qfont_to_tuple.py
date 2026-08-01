
def qfont_to_tuple(font):
    return (str(font.family()), int(font.pointSize()),
            font.italic(), font.bold())

