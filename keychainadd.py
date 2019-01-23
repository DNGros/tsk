import argparse

import svgutils
import svgutils.transform as sg
import custsvgutils
import os

HEIGHT_UNITS = 99.213   # The height of the thing in whatever units it exports
                        # as (so pixels, I think)
WIDTH_UNITS = 187.795

HEIGHT_CM = 3.5         # The intended height in cm.
WIDTH_CM = 6.625

assert -0.01 < HEIGHT_UNITS / HEIGHT_CM - WIDTH_UNITS / WIDTH_CM < 0.01


def cm_to_px(cm: float) -> float:
    return HEIGHT_UNITS / HEIGHT_CM * cm


def make_a_chain(name: str, src_file: str, out_root="./"):
    fig = svgutils.transform.fromfile(src_file)
    root = fig.getroot()
    text_margin = 0.08
    font_size = 13
    font_family="monospace"
    font_weight = "bold"

    name_text = sg.TextElement(
        x=cm_to_px(0.5 + text_margin),  # coord is bottom left corner of text
        y=cm_to_px(0.5 + .5 - text_margin),
        text=name,
        size=font_size,
        font=font_family,
        weight=font_weight
    )
    year_text = sg.TextElement(
        x=WIDTH_UNITS - cm_to_px(0.5 + text_margin*2),
        y=HEIGHT_UNITS - cm_to_px(0.5 + text_margin),
        text="2023",
        size=font_size,
        anchor="end",  # "right justify"
        font=font_family,
        weight=font_weight
    )

    fig.append([root, name_text, year_text])
    clean_name = name.strip().replace(" ", "")
    fig.save(os.path.join(out_root, f"{clean_name}_{src_file}"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='makin some chains.')
    parser.add_argument('-s', '--src', type=str, default="keychain.svg")
    parser.add_argument('-o', '--outroot', type=str, default="outs/")
    parser.add_argument('-n', '--names', type=str, default="names.txt")
    args = parser.parse_args()
    with open(args.names) as f:
        for name in f:
            make_a_chain(name, args.src, args.outroot)


