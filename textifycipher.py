import argparse
import math
from typing import Tuple, List

import svgutils
import svgutils.transform as sg
from svgutils.transform import FigureElement

import custsvgutils
import os

from custsvgutils import CircleElement

HEIGHT_UNITS = 171.496  # The height of the thing in whatever units it exports
                        # as (so pixels, I think)
WIDTH_UNITS = 171.496

HEIGHT_CM = 6.05           # The intended height in cm.
WIDTH_CM = 6.05

BIG_DISK_DIAMETER = 6.999
BIG_DISK_CENTER_X_CM = 0.557 + BIG_DISK_DIAMETER / 2
BIG_DISK_CENTER_Y_CM = 0.463 + BIG_DISK_DIAMETER / 2

RING_OUTER_DIAMETER = 5.65
SMALL_DISK_DIAMETER = 4.7

assert -0.01 < HEIGHT_UNITS / HEIGHT_CM - WIDTH_UNITS / WIDTH_CM < 0.01


def cm_to_px(cm: float) -> float:
    return HEIGHT_UNITS / HEIGHT_CM * cm


def draw_circle_thing(diameter: float, center: Tuple[float, float]) -> List[FigureElement]:
    """
    makes swirly circle thing
    :param diameter: the diameter of design in cm
    :param center: center of design in cm
    """
    x, y = cm_to_px(center[0]), cm_to_px(center[1])
    r_px = cm_to_px(diameter) / 2

    circles = []
    num_circles = 12
    circle_mult = 1
    for i in range(num_circles):
        rads = 2*math.pi/num_circles * i
        little_radius = (r_px/2)*circle_mult
        center_offset = r_px - little_radius
        cx = x + math.sin(rads) * center_offset
        cy = y + math.cos(rads) * center_offset
        circles.append(CircleElement(cx, cy, little_radius, stroke_width=1, fill="none"))
    return circles


def make_cipher(name: str, src_file: str, out_root="./", red_cuts: bool = False, pos: Tuple[float, float]=(0,0)):
    font_size = 18
    font_family="monospace"
    font_weight = "bold"
    letter_spaceing=5
    name = name.strip()
    # print(name)
    # print(f"len {len(name)}")
    if len(name) == 7:
        font_size=15
        letter_spaceing=3
    elif len(name) == 8:
        font_size=13
        letter_spaceing=2
    elif len(name) == 9:
        font_size=13
        letter_spaceing=2
    elif len(name) == 10:
        font_size=12
        letter_spaceing=2
    elif len(name) > 10:
        raise ValueError(f"name len unsupported {name}")

    #two_line_name = "\n".join(name.split())
    name_text = custsvgutils.BorderedTextElement(
        #x=cm_to_px(8.095+5.001/2),
        #y=cm_to_px(1.503+5.001/2),
        x=cm_to_px(pos[0] + HEIGHT_CM/2)-5,
        y=cm_to_px(pos[1] + WIDTH_CM/2),
        text=name,
        size=font_size,
        font=font_family,
        weight=font_weight,
        anchor="middle",
        color="none",
        stroke_color="yellow",
        stroke_width="1",
        #text_length=cm_to_px(min(len(name)*.4, SMALL_DISK_DIAMETER*.7)),
        letter_spaceing=letter_spaceing
    )

    return name_text

    #circles = draw_circle_thing(
    #    diameter=SMALL_DISK_DIAMETER,
    #    center=(BIG_DISK_CENTER_X_CM, BIG_DISK_CENTER_Y_CM)
    #)
    #fig.append([root, name_text] + circles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='makin some ciphers.')
    parser.add_argument('-s', '--src', type=str, default=None)
    parser.add_argument('-o', '--outroot', type=str, default="outs/")
    parser.add_argument('-n', '--names', type=str, default="names.txt")
    parser.add_argument('-p', '--positions', type=str, default=None)
    #parser.add_argument('-r', '--red', action='store_true',
    #                    help="Whether or not to show cut lines as red rather than hairlines")
    args = parser.parse_args()
    args.red = True
    if args.src is None:
        #args.src = "tscipher_red.svg" if args.red else "tscipher.svg"
        args.src = "tscipher_small.svg"
    names = []
    positions = None
    with open(args.names) as f:
        for name in f:
            names.append(name)
    if args.positions is not None:
        positions = []
        with open(args.positions) as f:
            for position in f:
                positions.append([float(x) for x in position.split()])
    # print("positions", positions)
    names_figs = []
    for i, name in enumerate(names):
        pos = positions[i % len(positions)]
        names_figs += [make_cipher(name, args.src, args.outroot, args.red, pos)]
        print(i)
        if i == len(positions) or i == len(names) - 1:
            fig = svgutils.transform.fromfile(args.src)
            root = fig.getroot()
            fig.append([root] + names_figs)
            clean_name = name.strip().replace(" ", "")
            fig.save(os.path.join(args.outroot, f"{clean_name}_{args.src}"))



