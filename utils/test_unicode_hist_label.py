
def test_unicode_hist_label():
    fig, ax = plt.subplots()
    a = (b'\xe5\xbe\x88\xe6\xbc\x82\xe4\xba\xae, ' +
         b'r\xc3\xb6m\xc3\xa4n ch\xc3\xa4r\xc3\xa1ct\xc3\xa8rs')
    b = b'\xd7\xa9\xd7\x9c\xd7\x95\xd7\x9d'
    labels = [a.decode('utf-8'),
              'hi aardvark',
              b.decode('utf-8'),
              ]

    ax.hist([range(15)] * 3, label=labels)
    ax.legend()

