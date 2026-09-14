import random

WIDTH = 900
HEIGHT = 220
FONT_SIZE = 16
COL_WIDTH = 18
NUM_COLS = WIDTH // COL_WIDTH
CHARS = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ$#%+-<>/\\"

def esc(ch):
    return {"<": "&lt;", ">": "&gt;", "&": "&amp;"}.get(ch, ch)

def rand_chars(n):
    return [esc(random.choice(CHARS)) for _ in range(n)]

def make_column(x, i):
    col_len = random.randint(6, 14)
    dur = round(random.uniform(2.2, 4.2), 2)
    delay = round(random.uniform(0, 4), 2)
    chars = rand_chars(col_len)
    tspans = []
    for j, ch in enumerate(chars):
        # brightest char at the head (last one), fading upward
        opacity = round(0.15 + 0.85 * (j / max(col_len - 1, 1)), 2)
        fill = "#ccffcc" if j == col_len - 1 else "#00ff41"
        tspans.append(
            f'<tspan x="{x}" dy="{FONT_SIZE if j else 0}" fill="{fill}" opacity="{opacity}">{ch}</tspan>'
        )
    text_block = "".join(tspans)
    start_y = -col_len * FONT_SIZE
    end_y = HEIGHT + FONT_SIZE
    return f'''
  <text font-family="monospace" font-size="{FONT_SIZE}" x="{x}" y="{start_y}">
    {text_block}
    <animateTransform attributeName="transform" type="translate"
      values="0,0;0,{end_y - start_y}" dur="{dur}s" begin="{delay}s"
      repeatCount="indefinite"/>
  </text>'''

def build_svg(title_text):
    random.seed(42)
    columns = "".join(make_column(i * COL_WIDTH + 4, i) for i in range(NUM_COLS))
    svg = f'''<svg viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="frame"><rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="10"/></clipPath>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d0208" stop-opacity="1"/>
      <stop offset="15%" stop-color="#0d0208" stop-opacity="0"/>
      <stop offset="85%" stop-color="#0d0208" stop-opacity="0"/>
      <stop offset="100%" stop-color="#0d0208" stop-opacity="1"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#frame)">
    <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#0d0208"/>
    {columns}
    <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="url(#fade)"/>
    <text x="50%" y="52%" text-anchor="middle" font-family="monospace"
      font-size="42" font-weight="bold" fill="#00ff41" opacity="0.95">{title_text}</text>
    <text x="50%" y="66%" text-anchor="middle" font-family="monospace"
      font-size="16" fill="#39ff14" opacity="0.85">Student of AI and robotics</text>
  </g>
</svg>'''
    return svg

if __name__ == "__main__":
    svg = build_svg("Dod0")
    with open("/home/claude/matrix/matrix-banner.svg", "w") as f:
        f.write(svg)
    print("written", len(svg), "bytes")
