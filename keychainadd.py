import svgutils
import svgutils.transform as sg

HEIGHT_UNITS = 99.213   # The height of the thing in whatever units it exports
                        # as (so pixels, I think)
WIDTH_UNITS = 187.795

HEIGHT_CM = 3.5         # The intended height in cm.
WIDTH_CM = 6.625

assert -0.01 < HEIGHT_UNITS / HEIGHT_CM - WIDTH_UNITS / WIDTH_CM < 0.01


def cm_to_px(cm: float) -> float:
    return HEIGHT_UNITS / HEIGHT_CM * cm


if __name__ == "__main__":
    fig = svgutils.transform.fromfile('keychain_red.svg')
    root = fig.getroot()
    for e in root:
        print(e.tostr())
    name = "Foobar Bazington"
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
    fig.save("new_keychain.svg")
