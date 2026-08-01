
def test_patheffects_stroked_text():
    text_chunks = [
        'A B C D E F G H I J K L',
        'M N O P Q R S T U V W',
        'X Y Z a b c d e f g h i j',
        'k l m n o p q r s t u v',
        'w x y z 0123456789',
        r"!@#$%^&*()-=_+[]\;'",
        ',./{}|:"<>?'
    ]
    font_size = 50

    ax = plt.figure(figsize=(8, 6)).add_axes((0, 0, 1, 1))
    for i, chunk in enumerate(text_chunks):
        text = ax.text(x=0.01, y=(0.9 - i * 0.13), s=chunk,
                       fontdict={'ha': 'left', 'va': 'center',
                                 'size': font_size, 'color': 'white'})

        text.set_path_effects([path_effects.Stroke(linewidth=font_size / 10,
                                                   foreground='black'),
                               path_effects.Normal()])

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

