"""
Code adapted from svgutils

Copyright (C) 2011 by Bartosz Telenczuk. Available under MIT license
"""
from lxml import etree

from svgutils.transform import FigureElement, SVG


class BorderedTextElement(FigureElement):
    """Text element.

    Corresponds to SVG ``<text>`` tag."""
    def __init__(self, x, y, text, size=8, font="Verdana",
                 weight="normal", letterspacing=0, anchor='start',
                 color='black', stroke_color="black", stroke_width="1px"):
        txt = etree.Element(
            SVG+"text",
            {
                "x": str(x), "y": str(y),
                "font-size": str(size),
                "font-family": font,
                "font-weight": weight,
                "letter-spacing": str(letterspacing),
                "text-anchor": str(anchor),
                "fill": str(color),
                "stroke": str(stroke_color),
                "stroke-width": str(stroke_width),
                "paint-order": "stroke",
                "stroke-linecap": "butt",
                "stroke-linejoin": "miter",
                "stroke-opacity": "1"
            }
        )
        txt.text = text
        FigureElement.__init__(self, txt)


class CircleElement(FigureElement):
    def __init__(self, x, y, r, fill='black', stroke_color="black", stroke_width="1px"):
        txt = etree.Element(
            SVG+"circle",
            {
                "cx": str(x), "cy": str(y), "r": str(r),
                "fill": str(fill),
                "stroke": str(stroke_color),
                "stroke-width": str(stroke_width),
                "paint-order": "stroke",
            }
        )
        FigureElement.__init__(self, txt)
