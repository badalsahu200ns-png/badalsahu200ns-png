from pathlib import Path
from PIL import Image


INPUT = Path("source-prepped.png")
OUTPUT = Path("hxni-ascii.svg")

RAMP = " .`:-=+*cs#%@"

WIDTH = 76
CHAR_ASPECT = 0.50


def pixel_to_char(value):
    index = int((value / 255) * (len(RAMP) - 1))
    return RAMP[index]


def main():
    image = Image.open(INPUT).convert("L")

    ratio = image.height / image.width
    height = max(1, int(WIDTH * ratio * CHAR_ASPECT))

    image = image.resize((WIDTH, height))

    lines = []

    for y in range(image.height):
        row = []

        for x in range(image.width):
            row.append(pixel_to_char(image.getpixel((x, y))))

        lines.append("".join(row))

    svg_width = 900
    line_height = 11
    top = 50

    svg_height = top + len(lines) * line_height + 35

    text_elements = []

    for i, line in enumerate(lines):
        delay = i * 0.025

        escaped = (
            line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        text_elements.append(
            f'''
            <text
                x="35"
                y="{top + i * line_height}"
                class="ascii"
                style="animation-delay:{delay:.3f}s"
            >{escaped}</text>
            '''
        )

    svg = f'''<svg
        xmlns="http://www.w3.org/2000/svg"
        width="{svg_width}"
        height="{svg_height}"
        viewBox="0 0 {svg_width} {svg_height}"
    >

    <defs>

        <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#FFF2A8"/>
            <stop offset="45%" stop-color="#D4AF37"/>
            <stop offset="100%" stop-color="#8C6B18"/>
        </linearGradient>

        <clipPath id="wipe">
            <rect
                x="0"
                y="0"
                width="{svg_width}"
                height="{svg_height}"
            >
                <animate
                    attributeName="width"
                    from="0"
                    to="{svg_width}"
                    dur="2.8s"
                    fill="freeze"
                />
            </rect>
        </clipPath>

        <filter id="glow">
            <feGaussianBlur
                stdDeviation="2"
                result="blur"
            />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>

        <style>
            .ascii {{
                font-family:
                    "Courier New",
                    Courier,
                    monospace;

                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
                fill: url(#gold);

                opacity: 0;

                animation:
                    fin
                    0.45s
                    ease-out
                    forwards;
            }}

            @keyframes fin {{
                from {{
                    opacity: 0;
                    transform: translateX(-8px);
                }}

                to {{
                    opacity: 1;
                    transform: translateX(0);
                }}
            }}
        </style>

    </defs>

    <rect
        width="100%"
        height="100%"
        rx="24"
        fill="#0d0d0d"
        stroke="#D4AF37"
        stroke-width="1"
    />

    <circle cx="28" cy="25" r="6" fill="#ff5f56"/>
    <circle cx="50" cy="25" r="6" fill="#ffbd2e"/>
    <circle cx="72" cy="25" r="6" fill="#27c93f"/>

    <text
        x="105"
        y="29"
        fill="#777"
        font-family="monospace"
        font-size="12"
    >
        badal@ai-analytics:~
    </text>

    <g clip-path="url(#wipe)" filter="url(#glow)">
        {"".join(text_elements)}
    </g>

    </svg>
    '''

    OUTPUT.write_text(svg, encoding="utf-8")

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
