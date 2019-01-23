import argparse

import svgutils
import svgutils.transform as sg
import custsvgutils
import os
HEIGHT_UNITS = 226.772  # The height of the thing in whatever units it exports
                        # as (so pixels, I think)
WIDTH_UNITS = 394.016

HEIGHT_CM = 8           # The intended height in cm.
WIDTH_CM = 13.9

assert -0.01 < HEIGHT_UNITS / HEIGHT_CM - WIDTH_UNITS / WIDTH_CM < 0.01


def cm_to_px(cm: float) -> float:
    return HEIGHT_UNITS / HEIGHT_CM * cm


def make_cipher(name: str, src_file: str, out_root="./"):
    fig = svgutils.transform.fromfile(src_file)
    root = fig.getroot()
    font_size = 12
    font_family="sarif"
    font_weight = "bold"

    #two_line_name = "\n".join(name.split())
    name_text = custsvgutils.BorderedTextElement(
        x=cm_to_px(8.095+5.001/2),
        y=cm_to_px(1.503+5.001/2),
        text=name,
        size=font_size,
        font=font_family,
        weight=font_weight,
        anchor="middle",
        color="none",
        stroke_color="red",
        stroke_width="1"
    )

    fig.append([root, name_text])
    clean_name = name.strip().replace(" ", "")
    fig.save(os.path.join(out_root, f"{clean_name}_{src_file}"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='makin some ciphers.')
    parser.add_argument('-s', '--src', type=str, default="tscipher.svg")
    parser.add_argument('-o', '--outroot', type=str, default="outs/")
    parser.add_argument('-n', '--names', type=str, default="names.txt")
    args = parser.parse_args()
    with open(args.names) as f:
        for name in f:
            make_cipher(name, args.src, args.outroot)


