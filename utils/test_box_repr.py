
def test_box_repr():
    s = repr(_mathtext.Parser().parse(
        r"$\frac{1}{2}$",
        _mathtext.DejaVuSansFonts(fm.FontProperties(), LoadFlags.NO_HINTING),
        fontsize=12, dpi=100))
    assert s == textwrap.dedent("""\
        Hlist<w=9.51 h=14.24 d=6.06 s=0.00>[
          Hlist<w=0.00 h=0.00 d=0.00 s=0.00>[],
          Hlist<w=9.51 h=14.24 d=6.06 s=0.00>[
            Hlist<w=9.51 h=14.24 d=6.06 s=0.00>[
              Hbox,
              Vlist<w=7.43 h=20.30 d=0.00 s=6.06>[
                HCentered<w=7.43 h=8.51 d=0.00 s=0.00>[
                  Glue,
                  Hlist<w=7.43 h=8.51 d=0.00 s=0.00>[
                    `1`,
                    k2.36,
                  ],
                  Glue,
                ],
                Vbox,
                Hrule,
                Vbox,
                HCentered<w=7.43 h=8.66 d=0.00 s=0.00>[
                  Glue,
                  Hlist<w=7.43 h=8.66 d=0.00 s=0.00>[
                    `2`,
                    k2.02,
                  ],
                  Glue,
                ],
              ],
              Hbox,
            ],
          ],
          Hlist<w=0.00 h=0.00 d=0.00 s=0.00>[],
        ]""")

