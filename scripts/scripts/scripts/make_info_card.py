from pathlib import Path


OUTPUT = Path("info-card.svg")


LINES = [
    ("OS", "Google Cloud / Windows"),
    ("HOST", "Bhubaneswar, Odisha, India"),
    ("ROLE", "Business Analyst • AI Strategy"),
    ("FOCUS", "Data Analytics • GenAI • AI Agents"),
    ("AI", "Gemini • ADK • Vertex AI • RAG"),
    ("DATA", "SQL • BigQuery • Power BI • Excel"),
    ("CLOUD", "Cloud Run • Firestore • Firebase"),
    ("PRODUCT", "AI Products • SaaS • Automation"),
    ("GITHUB", "badalsahu200ns-png"),
    ("LINKEDIN", "in/badalsahu200ns"),
]


def main():

    width = 980
    height = 440

    rows = []

    for index, (key, value) in enumerate(LINES):
        y = 100 + index * 31

        rows.append(
            f'''
            <g class="row" style="animation-delay:{index * 0.08}s">

                <text
                    x="48"
                    y="{y}"
                    class="key"
                >{key}</text>

                <text
                    x="205"
                    y="{y}"
                    class="value"
                >{value}</text>

            </g>
            '''
        )

    svg = f'''
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{width}"
    height="{height}"
    viewBox="0 0 {width} {height}"
>

<defs>

    <linearGradient id="gold">
        <stop offset="0%" stop-color="#FFF2A8"/>
        <stop offset="50%" stop-color="#D4AF37"/>
        <stop offset="100%" stop-color="#9B771D"/>
    </linearGradient>

    <style>

        .terminal {{
            font-family:
                "Courier New",
                monospace;
        }}

        .title {{
            fill: #D4AF37;
            font-size: 22px;
            font-weight: bold;
        }}

        .key {{
            fill: url(#gold);
            font-size: 14px;
            font-weight: bold;
        }}

        .value {{
            fill: #D0D0D0;
            font-size: 14px;
        }}

        .row {{
            opacity: 0;
            animation:
                reveal
                .6s
                ease-out
                forwards;
        }}

        @keyframes reveal {{
            from {{
                opacity: 0;
                transform: translateY(8px);
            }}

            to {{
                opacity: 1;
                transform: translateY(0);
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

<circle cx="30" cy="28" r="7" fill="#ff5f56"/>
<circle cx="55" cy="28" r="7" fill="#ffbd2e"/>
<circle cx="80" cy="28" r="7" fill="#27c93f"/>

<text
    x="115"
    y="35"
    class="title terminal"
>
    The Analytics Stack
</text>

<line
    x1="35"
    y1="58"
    x2="945"
    y2="58"
    stroke="#2A2A2A"
/>

<text
    x="48"
    y="82"
    fill="#666"
    font-family="monospace"
    font-size="11"
>
    badal@analytics:~$ profile --system
</text>

{"".join(rows)}

</svg>
'''

    OUTPUT.write_text(svg, encoding="utf-8")

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
