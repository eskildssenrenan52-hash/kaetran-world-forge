# Fatia as folhas de acessórios pintadas por IA (4x2) em atlas de 8 células para o personagem Kaetram.
# Uso: python3 scripts/build-look-sheets.py <pasta-com-png-brutos>
import sys
from PIL import Image
SRC = sys.argv[1] if len(sys.argv) > 1 else "/tmp/look"
# célula final (px, já em 2x da escala do jogo)
CELLS = {"hats": (36, 32), "horns": (40, 28), "capes": (32, 36), "wings": (64, 40), "eyes": (24, 12), "extras": (36, 24)}
for name, (cw, ch) in CELLS.items():
    im = Image.open(f"{SRC}/{name}.png").convert("RGBA")
    W, H = im.size; gw, gh = W // 4, H // 2
    px = im.load()
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if a and r > 170 and b > 170 and g < 110: px[x, y] = (0, 0, 0, 0)
            elif a < 128: px[x, y] = (0, 0, 0, 0)
            else: px[x, y] = (r, g, b, 255)
    out = Image.new("RGBA", (cw * 8, ch), (0, 0, 0, 0))
    for i in range(8):
        cell = im.crop(((i % 4) * gw, (i // 4) * gh, (i % 4 + 1) * gw, (i // 4 + 1) * gh))
        bb = cell.getbbox()
        if not bb: continue
        cell = cell.crop(bb)
        s = min(cw / cell.width, ch / cell.height)
        cell = cell.resize((max(1, round(cell.width * s)), max(1, round(cell.height * s))), Image.LANCZOS)
        a = cell.getchannel("A").point(lambda v: 255 if v > 110 else 0); cell.putalpha(a)
        out.alpha_composite(cell, (i * cw + (cw - cell.width) // 2, ch - cell.height))
    out.save(f"public/look/{name}.png")
    print(name, out.size)
