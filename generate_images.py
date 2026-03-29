import math
import os
from random import Random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = r"D:\Tresorit\z_Keepass\GSP\AI\Claude\ws02_Claudes_Daily_Diary"
OUT  = os.path.join(BASE, "articles", "2026", "03")
W, H = 1200, 630
TH   = 96
rng  = Random(42)   # deterministic


# ── Helper functions ────────────────────────────────────────────────────────

def fnt(size, bold=False, mono=False):
    candidates = []
    if mono:
        candidates = ["consolab.ttf", "consola.ttf", "cour.ttf", "DejaVuSansMono.ttf"]
    elif bold:
        candidates = ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"]
    else:
        candidates = ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except (IOError, OSError):
            pass
    return ImageFont.load_default()


def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def comp(base, over):
    return Image.alpha_composite(base.convert("RGBA"), over.convert("RGBA")).convert("RGB")


def make_thumb(img):
    """Center-crop to square, resize to TH×TH with LANCZOS."""
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top  = (h - side) // 2
    cropped = img.crop((left, top, left + side, top + side))
    return cropped.resize((TH, TH), Image.LANCZOS)


def add_badge(img, date, keyword, artist):
    """Add date/keyword/artist badge overlay."""
    draw = ImageDraw.Draw(img, "RGBA")

    # Dark semi-transparent rectangle covering x=0..700, y=H-150..H
    draw.rectangle([(0, H - 150), (700, H)], fill=(0, 0, 0, 160))

    # Coral rounded-rectangle badge
    coral = (232, 115, 74)
    bx0, by0, bx1, by1 = 40, H - 138, 255, H - 96
    draw.rounded_rectangle([(bx0, by0), (bx1, by1)], radius=9, fill=coral)

    # White mono text on badge (date)
    f_date = fnt(26, mono=True)
    draw.text((bx0 + 10, by0 + 6), date, fill=(255, 255, 255), font=f_date)

    # White bold keyword
    f_kw = fnt(46, bold=True)
    draw.text((40, H - 86), keyword, fill=(255, 255, 255), font=f_kw)

    # Cream italic-look small text
    f_artist = fnt(18)
    draw.text((40, H - 34), f"in the style of {artist}", fill=(253, 240, 235, 180), font=f_artist)

    return img


# ── Eight motif functions ────────────────────────────────────────────────────

def img_kandinsky():
    """Wassily Kandinsky 'Composition VIII' style."""
    base = Image.new("RGB", (W, H), (18, 34, 72))

    # 1. Diagonal grid lines
    grid_layer = layer()
    gd = ImageDraw.Draw(grid_layer)
    step = 60
    line_color = (255, 255, 255, 25)
    # Top-left to bottom-right diagonals
    for offset in range(-H, W + H, step):
        gd.line([(offset, 0), (offset + H, H)], fill=line_color, width=1)
    # Orthogonal (top-right to bottom-left)
    for offset in range(0, W + H + step, step):
        gd.line([(offset, 0), (offset - H, H)], fill=line_color, width=1)
    base = comp(base, grid_layer)

    # 2. Large yellow circle
    c_layer = layer()
    cd = ImageDraw.Draw(c_layer)
    cd.ellipse([(640, -60), (1100, 400)], fill=(255, 215, 0, 230), outline=(0, 0, 0, 255), width=6)
    base = comp(base, c_layer)

    # 3. Red triangle (pointing up)
    t_layer = layer()
    td = ImageDraw.Draw(t_layer)
    td.polygon([(200, 520), (460, 520), (330, 180)], fill=(220, 30, 50, 220), outline=(0, 0, 0, 255))
    base = comp(base, t_layer)

    # 4. Blue pie-slice
    p_layer = layer()
    pd = ImageDraw.Draw(p_layer)
    pd.pieslice([(820, 280), (1180, 580)], start=190, end=350, fill=(30, 90, 220, 200), outline=(0, 0, 0, 255), width=5)
    base = comp(base, p_layer)

    # 5. Large black arc
    a_layer = layer()
    ad = ImageDraw.Draw(a_layer)
    ad.arc([(50, 50), (550, 550)], start=260, end=70, fill=(0, 0, 0, 255), width=8)
    base = comp(base, a_layer)

    # 6. Orange circle
    oc_layer = layer()
    ocd = ImageDraw.Draw(oc_layer)
    ocd.ellipse([(100, 80), (260, 240)], fill=(255, 120, 20, 220), outline=(0, 0, 0, 255), width=5)
    base = comp(base, oc_layer)

    # 7. Purple circle
    pc_layer = layer()
    pcd = ImageDraw.Draw(pc_layer)
    pcd.ellipse([(380, 30), (520, 170)], fill=(150, 50, 200, 200), outline=(0, 0, 0, 255), width=4)
    base = comp(base, pc_layer)

    # 8. Green diamond
    gm_layer = layer()
    gmd = ImageDraw.Draw(gm_layer)
    gmd.polygon([(550, 350), (640, 250), (730, 350), (640, 450)], fill=(40, 180, 90, 200), outline=(0, 0, 0, 255), width=4)
    base = comp(base, gm_layer)

    # 9. 10 small scatter circles
    scatter = layer()
    sd = ImageDraw.Draw(scatter)
    positions = [
        (150, 320), (320, 400), (490, 140), (700, 60), (850, 500),
        (950, 200), (1050, 80), (1100, 450), (60, 480), (420, 300),
    ]
    colors = [
        (255, 215, 0, 220), (220, 30, 50, 220), (255, 255, 255, 200),
        (0, 240, 255, 200), (255, 120, 20, 220), (150, 50, 200, 200),
        (50, 220, 50, 220), (255, 215, 0, 200), (0, 240, 255, 200), (220, 30, 50, 220),
    ]
    radii = [18, 14, 11, 20, 9, 16, 13, 15, 12, 17]
    for (px, py), col, r in zip(positions, colors, radii):
        sd.ellipse([(px - r, py - r), (px + r, py + r)], fill=col, outline=(0, 0, 0, 255), width=2)
    base = comp(base, scatter)

    # 10. 3 bold lines
    lines_layer = layer()
    ld = ImageDraw.Draw(lines_layer)
    ld.line([(0, 400), (400, 100)], fill=(0, 0, 0, 255), width=4)
    ld.line([(500, 600), (900, 200)], fill=(0, 0, 0, 255), width=3)
    ld.line([(800, 600), (1100, 300)], fill=(255, 255, 255, 255), width=2)
    base = comp(base, lines_layer)

    return base


def img_mondrian():
    """Piet Mondrian 'Broadway Boogie Woogie' style."""
    base = Image.new("RGB", (W, H), (245, 240, 225))
    draw = ImageDraw.Draw(base)

    YELLOW = (255, 215, 0)
    RED    = (220, 40, 40)
    BLUE   = (30, 80, 200)
    BLACK  = (20, 20, 20)

    grid_x = [0, 120, 230, 340, 460, 560, 680, 790, 910, 1010, 1120, W]
    grid_y = [0, 80, 160, 250, 340, 420, 510, 600, H]
    band_w = 16

    # 1. Yellow bands
    for gx in grid_x[1:-1]:
        draw.rectangle([(gx - band_w // 2, 0), (gx + band_w // 2, H)], fill=YELLOW)
    for gy in grid_y[1:-1]:
        draw.rectangle([(0, gy - band_w // 2), (W, gy + band_w // 2)], fill=YELLOW)

    # 2. Intersection blocks
    cycle_colors = [RED, BLUE, YELLOW, (245, 240, 225), RED, BLUE, RED, (245, 240, 225), BLUE, RED, BLUE, (245, 240, 225)]
    idx = 0
    for i, gx in enumerate(grid_x[1:-1]):
        for j, gy in enumerate(grid_y[1:-1]):
            col = cycle_colors[idx % len(cycle_colors)]
            idx += 1
            cx = gx - band_w // 2
            cy = gy - band_w // 2
            draw.rectangle([(cx - 5, cy - 5), (cx + 15, cy + 15)], fill=col)

    # 3. Filled grid cells (big coloured rectangles)
    inset = band_w // 2 + 2
    colored_cells = [
        (0, 0, RED),   (2, 1, BLUE),  (5, 0, RED),
        (1, 3, BLUE),  (4, 2, RED),   (7, 1, BLUE),
        (3, 5, RED),   (6, 3, BLUE),  (9, 4, RED),
        (8, 6, BLUE),  (10, 2, RED),
    ]
    for ci, cj, col in colored_cells:
        if ci < len(grid_x) - 1 and cj < len(grid_y) - 1:
            x0 = grid_x[ci] + inset
            y0 = grid_y[cj] + inset
            x1 = grid_x[ci + 1] - inset
            y1 = grid_y[cj + 1] - inset
            if x1 > x0 and y1 > y0:
                draw.rectangle([(x0, y0), (x1, y1)], fill=col)

    # 4. Grid lines on top
    for gx in grid_x:
        draw.line([(gx, 0), (gx, H)], fill=BLACK, width=2)
    for gy in grid_y:
        draw.line([(0, gy), (W, gy)], fill=BLACK, width=2)

    return base


def img_futurism():
    """Giacomo Balla / Italian Futurism speed style."""
    base = Image.new("RGBA", (W, H), (5, 5, 20, 255))

    VP = (1100, 315)

    colors_list = [
        (0, 240, 255),   # cyan
        (255, 0, 200),   # magenta
        (255, 220, 0),   # yellow
        (0, 255, 80),    # lime
        (255, 80, 0),    # orange
        (160, 0, 255),   # violet
        (255, 255, 255), # white
        (0, 160, 255),   # sky
        (255, 40, 80),   # hotpink
        (120, 255, 0),   # yelgreen
    ]

    # 1. 18 radiating planes from VP
    fan_half = math.radians(130)
    base_angle = math.pi  # pointing left
    planes_layer = layer()
    pd = ImageDraw.Draw(planes_layer)
    for i in range(18):
        t1 = base_angle - fan_half + (2 * fan_half * i / 18)
        t2 = base_angle - fan_half + (2 * fan_half * (i + 1) / 18)
        dist = 1300
        fp1 = (VP[0] + dist * math.cos(t1), VP[1] + dist * math.sin(t1))
        fp2 = (VP[0] + dist * math.cos(t2), VP[1] + dist * math.sin(t2))
        col = colors_list[i % len(colors_list)]
        alpha = 120 + (i * 4) % 61
        draw_col = col + (alpha,)
        pd.polygon([VP, fp1, fp2], fill=draw_col)
    base = Image.alpha_composite(base, planes_layer)

    # 2. Horizontal motion lines
    ml_layer = layer()
    mld = ImageDraw.Draw(ml_layer)
    center_y = H // 2
    for k in range(15):
        ly = 30 + k * 42
        dist_from_center = abs(ly - center_y)
        intensity = max(60, 220 - dist_from_center)
        col = (min(255, intensity + 50), min(255, intensity + 20), 80, intensity)
        mld.line([(0, ly), (900, ly)], fill=col, width=1)
    base = Image.alpha_composite(base, ml_layer)

    # 3. Glow burst at VP
    glow_layer = layer()
    gd = ImageDraw.Draw(glow_layer)
    glow_radii = [(200, 40), (150, 60), (100, 80), (60, 110), (30, 150)]
    for r, a in glow_radii:
        gd.ellipse([(VP[0] - r, VP[1] - r), (VP[0] + r, VP[1] + r)], fill=(255, 255, 255, a))
    base = Image.alpha_composite(base, glow_layer)

    return base.convert("RGB")


def img_klimt():
    """Gustav Klimt 'The Kiss / Tree of Life' gold mosaic style."""
    base = Image.new("RGB", (W, H), (10, 10, 30))
    draw = ImageDraw.Draw(base)

    GOLD  = (212, 175, 55)
    GOLD2 = (255, 215, 80)
    TEAL  = (30, 150, 140)
    RUST  = (150, 50, 30)
    CREAM = (240, 220, 170)

    # 1. Background texture (20x20 patches)
    patch = 20
    for py in range(0, H, patch):
        for px in range(0, W, patch):
            r_val = rng.random()
            if r_val < 0.25:
                r = rng.randint(5, 20)
                g = rng.randint(5, 25)
                b = rng.randint(30, 60)
            elif r_val < 0.40:
                r = rng.randint(20, 40)
                g = rng.randint(100, 140)
                b = rng.randint(110, 150)
            else:
                r = rng.randint(5, 15)
                g = rng.randint(5, 15)
                b = rng.randint(20, 40)
            draw.rectangle([(px, py), (px + patch, py + patch)], fill=(r, g, b))

    # 2. Golden spiral
    spiral_layer = layer()
    sd = ImageDraw.Draw(spiral_layer)
    cx, cy = 600, 400
    for deg in range(0, 721, 3):
        angle = math.radians(deg)
        r = deg * 0.4
        rx = cx + r * math.cos(angle)
        ry = cy + r * 0.5 * math.sin(angle)
        sd.ellipse([(rx - 2, ry - 2), (rx + 2, ry + 2)], fill=GOLD + (200,))
    base = comp(base, spiral_layer)

    # 3. 6 branch spirals
    branch_layer = layer()
    bd = ImageDraw.Draw(branch_layer)
    for branch in range(6):
        ba = math.radians(branch * 60)
        bx = cx + 150 * math.cos(ba)
        by = cy + 150 * math.sin(ba)
        for deg in range(0, 361, 3):
            angle = math.radians(deg)
            r = deg * 0.2
            rx = bx + r * math.cos(angle)
            ry = by + r * math.sin(angle)
            bd.ellipse([(rx - 1, ry - 1), (rx + 1, ry + 1)], fill=GOLD + (180,))
    base = comp(base, branch_layer)

    # 4. 200 mosaic elements
    mosaic_layer = layer()
    md = ImageDraw.Draw(mosaic_layer)
    for _ in range(200):
        mx = rng.randint(0, W)
        my = rng.randint(0, H)
        sz = rng.randint(6, 18)
        shape_type = rng.choice(["rect", "ellipse", "tri", "eye"])
        col_r = rng.random()
        if col_r < 0.50:
            col = GOLD
        elif col_r < 0.70:
            col = TEAL
        elif col_r < 0.85:
            col = RUST
        else:
            col = CREAM
        alpha = rng.randint(160, 220)
        col_a = col + (alpha,)
        if shape_type == "rect":
            md.rectangle([(mx, my), (mx + sz, my + sz)], fill=col_a)
        elif shape_type == "ellipse":
            md.ellipse([(mx - sz // 2, my - sz // 2), (mx + sz // 2, my + sz // 2)], fill=col_a)
        elif shape_type == "tri":
            md.polygon([(mx, my + sz), (mx + sz, my + sz), (mx + sz // 2, my)], fill=col_a)
        else:  # eye
            md.ellipse([(mx - sz, my - sz // 2), (mx + sz, my + sz // 2)], fill=col_a)
            inner = sz // 3
            md.ellipse([(mx - inner, my - inner), (mx + inner, my + inner)], fill=(10, 10, 30, alpha))
    base = comp(base, mosaic_layer)

    # 5. 3 large gold circle outlines
    circle_layer = layer()
    cd = ImageDraw.Draw(circle_layer)
    circles = [(800, 150, 120), (400, 480, 90), (1050, 400, 100)]
    for gcx, gcy, gr in circles:
        cd.ellipse([(gcx - gr, gcy - gr), (gcx + gr, gcy + gr)],
                   fill=GOLD + (80,), outline=GOLD2 + (150,), width=3)
    base = comp(base, circle_layer)

    return base


def img_klee():
    """Paul Klee 'Fire in the Evening' / Magic Squares style."""
    base = Image.new("RGB", (W, H), (20, 20, 30))
    draw = ImageDraw.Draw(base)

    cell_w, cell_h = 72, 52
    cols = math.ceil(W / cell_w) + 1
    rows = math.ceil(H / cell_h) + 1

    warm_palette  = [(180,40,20),(200,80,30),(220,120,40),(240,160,60),(200,60,80),(180,100,40),(220,80,50),(200,140,60)]
    mid_palette   = [(150,80,150),(180,100,160),(120,80,120),(200,120,180),(140,120,60),(160,140,80),(120,160,100),(100,140,80)]
    cool_palette  = [(40,80,160),(60,100,180),(80,120,200),(40,60,140),(60,140,180),(80,160,200),(40,100,160),(60,80,140)]

    for row in range(rows):
        y0 = row * cell_h
        y_center = y0 + cell_h // 2
        # Determine zone
        if y_center > H * 2 // 3:
            palette = warm_palette
        elif y_center > H // 3:
            palette = mid_palette
        else:
            palette = cool_palette

        for col in range(cols):
            x0 = col * cell_w
            idx = (row * 3 + col * 2) % len(palette)
            base_col = palette[idx]
            r = max(0, min(255, base_col[0] + rng.randint(-15, 15)))
            g = max(0, min(255, base_col[1] + rng.randint(-15, 15)))
            b = max(0, min(255, base_col[2] + rng.randint(-15, 15)))
            draw.rectangle([(x0, y0), (x0 + cell_w, y0 + cell_h)], fill=(r, g, b))

    # Grid lines
    for col in range(cols + 1):
        x = col * cell_w
        draw.line([(x, 0), (x, H)], fill=(10, 10, 15), width=2)
    for row in range(rows + 1):
        y = row * cell_h
        draw.line([(0, y), (W, y)], fill=(10, 10, 15), width=2)

    # Node highlights
    nodes = [(3,2),(6,4),(9,2),(12,5),(5,6),(10,7),(8,3),(4,5),(11,1)]
    node_centers = []
    for (nc, nr) in nodes:
        nx = nc * cell_w + cell_w // 2
        ny = nr * cell_h + cell_h // 2
        node_centers.append((nx, ny))
        r_n = 16
        draw.ellipse([(nx - r_n, ny - r_n), (nx + r_n, ny + r_n)],
                     fill=(255, 255, 255), outline=(180, 180, 180), width=2)

    # Node connections
    conn_layer = layer()
    cld = ImageDraw.Draw(conn_layer)
    for i in range(len(node_centers) - 1):
        nx1, ny1 = node_centers[i]
        nx2, ny2 = node_centers[i + 1]
        cld.line([(nx1, ny1), (nx2, ny2)], fill=(255, 255, 255, 120), width=2)
    base = comp(base, conn_layer)

    return base


def img_delaunay():
    """Robert Delaunay 'Simultaneous Discs' / Orphism style."""
    base = Image.new("RGB", (W, H), (15, 15, 25))

    spectral = [
        (255, 255, 255),  # white (innermost)
        (200, 30, 180),   # magenta
        (100, 30, 220),   # violet
        (30, 120, 255),   # blue
        (50, 200, 60),    # green
        (255, 220, 0),    # yellow
        (255, 100, 0),    # orange
        (220, 30, 50),    # red (outermost)
    ]

    main_discs = [(300, 200, 220), (800, 380, 280), (130, 500, 180)]

    for dcx, dcy, max_r in main_discs:
        disc_layer = layer()
        dd = ImageDraw.Draw(disc_layer)
        ring_w = max_r // 8
        for ring_idx in range(7, -1, -1):
            r = max_r - ring_idx * ring_w
            col = spectral[ring_idx]
            dd.ellipse([(dcx - r, dcy - r), (dcx + r, dcy + r)], fill=col + (210,))
        base = comp(base, disc_layer)

    # Accent discs
    accent_discs = [(950, 120, 120), (550, 100, 90), (1100, 500, 150)]
    accent_spectral = [
        (255, 255, 255),
        (255, 220, 0),
        (30, 120, 255),
        (220, 30, 50),
    ]
    for dcx, dcy, max_r in accent_discs:
        acc_layer = layer()
        ad = ImageDraw.Draw(acc_layer)
        ring_w = max_r // 4
        for ring_idx in range(3, -1, -1):
            r = max_r - ring_idx * ring_w
            col = accent_spectral[ring_idx]
            ad.ellipse([(dcx - r, dcy - r), (dcx + r, dcy + r)], fill=col + (180,))
        base = comp(base, acc_layer)

    return base


def img_miro():
    """Joan Miro abstract biomorphic style."""
    base = Image.new("RGB", (W, H), (20, 20, 60))

    # 1. Background blobs
    blob_layer = layer()
    bd = ImageDraw.Draw(blob_layer)
    bd.ellipse([(0, 100), (800, H)], fill=(30, 30, 80, 100))
    bd.ellipse([(200, 0), (W, 500)], fill=(25, 25, 70, 80))
    base = comp(base, blob_layer)

    # 2. Biomorphic shapes
    shapes = [
        ([(200,100),(320,80),(380,150),(350,280),(250,310),(160,240),(140,160)], (220,50,50,220)),
        ([(550,200),(680,160),(760,240),(740,380),(620,420),(520,350),(480,270)], (255,215,0,220)),
        ([(850,80),(980,100),(1040,200),(990,330),(880,360),(800,280),(790,170)], (40,120,220,220)),
        ([(100,400),(220,380),(280,460),(230,560),(130,570),(80,490)], (50,180,80,220)),
        ([(700,430),(820,400),(880,480),(840,570),(730,590),(660,510)], (255,100,30,220)),
    ]
    for pts, col in shapes:
        sh_layer = layer()
        shd = ImageDraw.Draw(sh_layer)
        shd.polygon(pts, fill=col)
        base = comp(base, sh_layer)
        # Black outline as closed polyline
        outline_layer = layer()
        od = ImageDraw.Draw(outline_layer)
        od.line(pts + [pts[0]], fill=(0, 0, 0, 220), width=5)
        base = comp(base, outline_layer)

    # 3. Stars
    def make_star(cx, cy, r_o, r_i, n):
        pts = []
        for k in range(n * 2):
            angle = math.radians(-90 + k * 180 / n)
            r = r_o if k % 2 == 0 else r_i
            pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        return pts

    stars = [
        (1060, 200, 60, 25, 5, (255,255,255,220)),
        (440,  100, 45, 18, 6, (255,215,0,220)),
        (900,  500, 50, 22, 4, (220,30,50,220)),
        (1150, 420, 35, 14, 5, (255,255,255,220)),
        (320,  510, 40, 16, 6, (40,120,220,220)),
    ]
    for scx, scy, ro, ri, n, col in stars:
        star_pts = make_star(scx, scy, ro, ri, n)
        sl = layer()
        sld = ImageDraw.Draw(sl)
        sld.polygon(star_pts, fill=col)
        base = comp(base, sl)

    # 4. Connecting lines between shape centroids
    def centroid(pts):
        return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))

    centroids = [centroid(pts) for pts, _ in shapes]
    lines_layer = layer()
    ld = ImageDraw.Draw(lines_layer)
    for i in range(len(centroids) - 1):
        ld.line([centroids[i], centroids[i+1]], fill=(255, 255, 255, 150), width=2)
    base = comp(base, lines_layer)

    # 5. Scatter dots
    dots = [
        (470, 480, 18, (255,255,255,220)),
        (750, 150, 14, (220,30,50,220)),
        (1000,350, 20, (255,215,0,220)),
        (150, 300, 12, (255,255,255,220)),
        (1100, 80, 16, (40,120,220,220)),
        (640, 540, 14, (255,255,255,220)),
    ]
    dot_layer = layer()
    dd = ImageDraw.Draw(dot_layer)
    for dx, dy, dr, col in dots:
        dd.ellipse([(dx-dr, dy-dr), (dx+dr, dy+dr)], fill=col, outline=(0,0,0,220), width=2)
    base = comp(base, dot_layer)

    return base


def img_malevich():
    """Kazimir Malevich 'Suprematism' pure geometry."""
    base = Image.new("RGBA", (W, H), (240, 235, 220, 255))

    def rotated_rect_pts(x0, y0, x1, y1, angle_deg):
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        hw = (x1 - x0) / 2
        hh = (y1 - y0) / 2
        angle = math.radians(angle_deg)
        corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        rotated = []
        for rx, ry in corners:
            nx = cx + rx * math.cos(angle) - ry * math.sin(angle)
            ny = cy + rx * math.sin(angle) + ry * math.cos(angle)
            rotated.append((nx, ny))
        return rotated

    shapes = [
        # (type, params, fill)
        ("poly", rotated_rect_pts(480, 180, 920, 460, -12), (20, 15, 10, 255)),
        ("ellipse", (370, 110, 600, 340), (210, 30, 30, 255)),
        ("poly", rotated_rect_pts(180, 345, 870, 425, 8),   (25, 45, 155, 255)),
        ("poly", rotated_rect_pts(745, 70, 875, 195, 22),   (235, 205, 0, 255)),
        ("poly", rotated_rect_pts(80, 132, 1120, 162, -3),  (20, 15, 10, 255)),
        ("poly", rotated_rect_pts(945, 295, 1065, 420, 17), (210, 30, 30, 255)),
        ("poly", rotated_rect_pts(140, 425, 410, 565, -6),  (25, 135, 125, 255)),
    ]

    for stype, sparams, col in shapes:
        sl = layer()
        sld = ImageDraw.Draw(sl)
        if stype == "poly":
            sld.polygon(sparams, fill=col)
        else:
            sld.ellipse(sparams, fill=col)
        base = Image.alpha_composite(base, sl)

    return base.convert("RGB")


def img_seurat_20260321():
    """Georges Seurat pointillist style — messaging/channels network theme."""
    base = Image.new("RGB", (W, H), (12, 18, 45))   # deep navy

    draw = ImageDraw.Draw(base)

    # 1. Background dot field — faint, low-saturation scatter
    for _ in range(3000):
        x = rng.randint(0, W)
        y = rng.randint(0, H)
        r = rng.randint(1, 3)
        val = rng.randint(30, 80)
        draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=(val, val+10, val+30))

    # 2. Three glowing node circles representing network hubs
    nodes = [(280, 200), (620, 340), (960, 180)]
    halo_colours = [
        [(255,80,40), (255,140,60), (255,200,120), (255,240,200)],
        [(40,120,255), (80,180,255), (140,220,255), (210,240,255)],
        [(60,200,80), (100,230,100), (160,250,140), (220,255,200)],
    ]
    for (nx, ny), hcols in zip(nodes, halo_colours):
        for radius, col in zip([120, 80, 45, 20], hcols):
            nl = layer()
            nd = ImageDraw.Draw(nl)
            # Fill halo with tiny dots
            for _ in range(600):
                angle = rng.uniform(0, 2 * math.pi)
                dist = rng.uniform(0, radius)
                dx = int(nx + dist * math.cos(angle))
                dy = int(ny + dist * math.sin(angle))
                dr = rng.randint(1, 4)
                alpha = int(180 * (1 - dist / radius))
                nd.ellipse([(dx-dr, dy-dr), (dx+dr, dy+dr)],
                           fill=(col[0], col[1], col[2], alpha))
            base = comp(base, nl)

    # 3. Connection arcs between nodes — dense dot trails
    arc_pairs = [(nodes[0], nodes[1]), (nodes[1], nodes[2]), (nodes[0], nodes[2])]
    arc_colours = [(255, 160, 60), (100, 180, 255), (140, 255, 140)]
    for (ax, ay), (bx, by) in arc_pairs:
        al = layer()
        ad = ImageDraw.Draw(al)
        for t_i in range(200):
            t = t_i / 199
            mx = ax + (bx - ax) * t
            my = ay + (by - ay) * t - 60 * math.sin(math.pi * t)   # arc bow
            dr = rng.randint(2, 5)
            col = arc_colours[arc_pairs.index(((ax, ay), (bx, by)))]
            alpha = int(200 * math.sin(math.pi * t))
            ad.ellipse([(mx-dr, my-dr), (mx+dr, my+dr)],
                       fill=(col[0], col[1], col[2], alpha))
        base = comp(base, al)

    # 4. Foreground spectral scatter — bright dots across full canvas
    spectral = [
        (255, 50, 50), (255, 140, 0), (255, 230, 0),
        (50, 220, 80), (50, 150, 255), (180, 80, 255),
    ]
    fl = layer()
    fd = ImageDraw.Draw(fl)
    for _ in range(1200):
        x = rng.randint(0, W)
        y = rng.randint(0, H)
        r = rng.randint(1, 4)
        col = rng.choice(spectral)
        fd.ellipse([(x-r, y-r), (x+r, y+r)],
                   fill=(col[0], col[1], col[2], rng.randint(60, 180)))
    base = comp(base, fl)

    return base


def img_leger_20260322():
    """Fernand Leger mechanical/industrial style — architecture & policy theme."""
    base = Image.new("RGB", (W, H), (28, 28, 32))   # near-black charcoal

    # 1. Bold flat background bands
    bl = layer()
    bd = ImageDraw.Draw(bl)
    bd.rectangle([(0, 0), (W, 210)], fill=(50, 50, 58, 255))
    bd.rectangle([(0, 420), (W, H)], fill=(42, 42, 50, 255))
    base = comp(base, bl)

    # 2. Large mechanical circles — Leger's signature tubular forms
    circles = [
        (160, 315, 200, (210, 30, 30, 220)),    # big red
        (560, 180, 160, (235, 200, 0, 200)),     # yellow
        (920, 380, 180, (30, 90, 200, 220)),     # blue
        (760, 120, 90,  (210, 30, 30, 180)),     # small red
        (340, 490, 110, (235, 200, 0, 160)),     # small yellow
        (1080, 200, 120,(30, 90, 200, 180)),     # small blue
    ]
    for cx, cy, r, col in circles:
        cl = layer()
        cd = ImageDraw.Draw(cl)
        # Thick outline ring — Leger's bold black contour
        cd.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=col, outline=(0,0,0,255), width=8)
        # Inner highlight
        cd.ellipse([(cx-r//3, cy-r//2), (cx+r//5, cy-r//4)],
                   fill=(255, 255, 255, 80))
        base = comp(base, cl)

    # 3. Mechanical cylinders / pipe shapes (rectangles with rounded caps)
    pipes = [
        (380, 100, 480, 560, (28, 28, 32, 255), 12),   # dark vertical bar
        (700, 260, 1150, 320, (210, 30, 30, 200), 8),   # red horizontal bar
        (50,  380, 600,  430, (30, 90, 200, 200), 8),   # blue horizontal bar
        (820, 50,  870,  580, (235, 200, 0, 180), 8),   # yellow vertical
    ]
    for x0, y0, x1, y1, col, w in pipes:
        pl = layer()
        pd = ImageDraw.Draw(pl)
        pd.rectangle([(x0, y0), (x1, y1)], fill=col, outline=(0,0,0,255), width=w)
        base = comp(base, pl)

    # 4. Grid of small machine-bolt dots — Leger's industrial texture
    dl = layer()
    dd = ImageDraw.Draw(dl)
    for gx in range(60, W, 120):
        for gy in range(60, H, 120):
            r = 10
            dd.ellipse([(gx-r, gy-r), (gx+r, gy+r)],
                       fill=(200, 195, 185, 140), outline=(0,0,0,200), width=3)
    base = comp(base, dl)

    return base


def img_franz_marc_20260310():
    """Franz Marc — jewel-toned, stylised organic forms — APAC expansion / new territory."""
    # Rich cobalt background
    base = Image.new("RGB", (W, H), (18, 42, 105))

    # 1. Large stylised animal/landscape shape — Franz Marc's signature
    # Rolling hills / organic forms in emerald and gold
    fl = layer()
    fd = ImageDraw.Draw(fl)
    # Sweeping cobalt-to-emerald hill form across lower half
    fd.polygon([(0, 420), (300, 280), (600, 350), (900, 240), (1200, 320), (1200, 630), (0, 630)],
               fill=(22, 140, 90, 230))
    base = comp(base, fl)

    # 2. Second organic hill in teal — depth layer
    sl = layer()
    sd = ImageDraw.Draw(sl)
    sd.polygon([(0, 500), (200, 380), (500, 440), (800, 360), (1100, 430), (1200, 400),
                (1200, 630), (0, 630)], fill=(18, 110, 130, 200))
    base = comp(base, sl)

    # 3. Large stylised sun/moon disc — warm amber
    ol = layer()
    od = ImageDraw.Draw(ol)
    od.ellipse([(820, 30), (1100, 310)], fill=(220, 160, 20, 200))
    # Inner highlight
    od.ellipse([(870, 70), (1050, 250)], fill=(240, 200, 60, 120))
    base = comp(base, ol)

    # 4. Abstract animal forms — Marc's horses/deer as geometric colour masses
    al = layer()
    ad = ImageDraw.Draw(al)
    # Blue stylised horse body (left)
    ad.ellipse([(60, 180), (320, 400)], fill=(40, 80, 200, 180))
    ad.polygon([(60, 300), (0, 200), (100, 160)], fill=(40, 80, 200, 160))  # head
    # Red-orange form (right foreground)
    ad.ellipse([(280, 300), (520, 500)], fill=(200, 70, 30, 190))
    base = comp(base, al)

    # 5. Jewel-tone scatter — Marc's characteristic gem-like colour accents
    jl = layer()
    jd = ImageDraw.Draw(jl)
    jewels = [(160, 60, (180, 30, 120, 180)),   # magenta
              (500, 120, (220, 180, 20, 180)),   # gold
              (700, 200, (30, 160, 200, 170)),   # cyan
              (1050, 380, (140, 30, 180, 170)),  # purple
              (350, 480, (220, 100, 20, 160)),   # amber
              (900, 500, (30, 140, 80, 160))]    # green
    for jx, jy, jcol in jewels:
        jr = rng.randint(28, 52)
        jd.ellipse([(jx-jr, jy-jr), (jx+jr, jy+jr)], fill=jcol)
    base = comp(base, jl)

    return base


def img_calder_20260311():
    """Alexander Calder — primary shapes on thin lines, mobile balance — mixed/flexible day."""
    # White background
    base = Image.new("RGB", (W, H), (250, 250, 250))

    # 1. Thin black structural lines — Calder's mobile wires
    wl = layer()
    wd = ImageDraw.Draw(wl)
    # Main horizontal spine
    wd.line([(100, 180), (1100, 180)], fill=(15, 15, 15, 255), width=3)
    # Drooping sub-arms
    wd.line([(250, 180), (250, 320)], fill=(15, 15, 15, 255), width=2)
    wd.line([(550, 180), (480, 400)], fill=(15, 15, 15, 255), width=2)
    wd.line([(550, 180), (640, 380)], fill=(15, 15, 15, 255), width=2)
    wd.line([(850, 180), (800, 340)], fill=(15, 15, 15, 255), width=2)
    wd.line([(850, 180), (950, 420)], fill=(15, 15, 15, 255), width=2)
    wd.line([(1050, 180), (1050, 300)], fill=(15, 15, 15, 255), width=2)
    # Lower sub-arms
    wd.line([(480, 400), (380, 520)], fill=(15, 15, 15, 255), width=2)
    wd.line([(480, 400), (560, 500)], fill=(15, 15, 15, 255), width=2)
    wd.line([(950, 420), (880, 540)], fill=(15, 15, 15, 255), width=2)
    wd.line([(950, 420), (1040, 540)], fill=(15, 15, 15, 255), width=2)
    # Vertical anchor line from top
    wd.line([(600, 0), (600, 180)], fill=(15, 15, 15, 255), width=3)
    base = comp(base, wl)

    # 2. Calder's flat primary colour shapes hanging from the wires
    shapes = [
        # (x, y, size, shape, colour)
        (250, 355, 50, 'circle', (220, 30, 30, 255)),     # red circle
        (800, 355, 55, 'circle', (30, 80, 200, 255)),     # blue circle
        (1050, 320, 40, 'rect',  (220, 185, 0, 255)),     # yellow rect
        (380, 545, 48, 'circle', (220, 30, 30, 255)),     # red circle lower
        (560, 520, 44, 'rect',   (30, 80, 200, 255)),     # blue rect
        (880, 560, 46, 'circle', (220, 185, 0, 255)),     # yellow circle
        (1040, 560, 42, 'rect',  (220, 30, 30, 255)),     # red rect
        (640, 400, 38, 'circle', (15, 140, 70, 255)),     # green circle
    ]
    for sx, sy, sz, stype, scol in shapes:
        pl = layer()
        pd = ImageDraw.Draw(pl)
        if stype == 'circle':
            pd.ellipse([(sx-sz, sy-sz), (sx+sz, sy+sz)], fill=scol)
        else:
            pd.rectangle([(sx-sz, sy-sz//2), (sx+sz, sy+sz//2)], fill=scol)
        base = comp(base, pl)

    # 3. Small black pivot dots at wire junctions
    dl = layer()
    dd = ImageDraw.Draw(dl)
    pivots = [(250, 180), (550, 180), (850, 180), (1050, 180),
              (480, 400), (640, 380), (800, 340), (950, 420), (600, 180)]
    for px, py in pivots:
        dd.ellipse([(px-6, py-6), (px+6, py+6)], fill=(15, 15, 15, 255))
    base = comp(base, dl)

    return base


def img_rothko_20260312():
    """Mark Rothko colour field — luminous bands — certification/launch day reflective quality."""
    # Deep charcoal background
    base = Image.new("RGB", (W, H), (28, 22, 18))

    def soft_band(img, y0, y1, colour, feather=60):
        """Draw a soft-edged Rothko colour band."""
        bl = layer()
        bd = ImageDraw.Draw(bl)
        r, g, b = colour
        # Core solid band
        bd.rectangle([(80, y0 + feather), (W - 80, y1 - feather)], fill=(r, g, b, 220))
        # Feathered edges — top
        for i in range(feather):
            alpha = int(180 * (i / feather))
            bd.rectangle([(80 + i, y0 + i), (W - 80 - i, y0 + i + 1)], fill=(r, g, b, alpha))
        # Feathered edges — bottom
        for i in range(feather):
            alpha = int(180 * ((feather - i) / feather))
            bd.rectangle([(80 + i, y1 - i - 1), (W - 80 - i, y1 - i)], fill=(r, g, b, alpha))
        return comp(img, bl)

    # Three luminous Rothko bands
    # Top — deep burgundy-crimson
    base = soft_band(base, 40, 240, (140, 28, 42), feather=55)
    # Middle — warm amber-gold (widest, most luminous)
    base = soft_band(base, 220, 430, (195, 120, 30), feather=65)
    # Bottom — muted terracotta-rust
    base = soft_band(base, 400, 590, (160, 65, 40), feather=55)

    # Luminous inner glow on middle band
    gl = layer()
    gd = ImageDraw.Draw(gl)
    for i in range(40):
        alpha = int(60 * (1 - i / 40))
        gd.rectangle([(200 + i, 260 + i), (W - 200 - i, 390 - i)], fill=(240, 200, 80, alpha))
    base = comp(base, gl)

    return base


def img_rothko_20260327():
    """Mark Rothko colour field — deep mystery of a leaked model, legal weight, financial horizon."""
    # Very deep near-black background — sense of depth and revelation
    base = Image.new("RGB", (W, H), (18, 14, 22))

    def soft_band(img, y0, y1, colour, feather=70):
        bl = layer()
        bd = ImageDraw.Draw(bl)
        r, g, b = colour
        bd.rectangle([(60, y0 + feather), (W - 60, y1 - feather)], fill=(r, g, b, 210))
        for i in range(feather):
            alpha = int(180 * (i / feather))
            bd.rectangle([(60 + i, y0 + i), (W - 60 - i, y0 + i + 1)], fill=(r, g, b, alpha))
        for i in range(feather):
            alpha = int(180 * ((feather - i) / feather))
            bd.rectangle([(60 + i, y1 - i - 1), (W - 60 - i, y1 - i)], fill=(r, g, b, alpha))
        return comp(img, bl)

    # Top band — deep violet-indigo: mystery of Mythos
    base = soft_band(base, 30, 230, (68, 28, 110), feather=65)
    # Middle band — warm gold: legal victory, the turning point
    base = soft_band(base, 210, 430, (185, 130, 25), feather=75)
    # Bottom band — cool steel-blue: the financial horizon of an IPO
    base = soft_band(base, 405, 600, (28, 72, 120), feather=60)

    # Inner luminous glow on the gold band — the moment of revelation
    gl = layer()
    gd = ImageDraw.Draw(gl)
    for i in range(50):
        alpha = int(70 * (1 - i / 50))
        gd.rectangle([(180 + i, 265 + i), (W - 180 - i, 375 - i)], fill=(255, 215, 80, alpha))
    base = comp(base, gl)

    # Subtle violet bloom at the top — the leak emerging from darkness
    bl2 = layer()
    bd2 = ImageDraw.Draw(bl2)
    for i in range(80):
        alpha = int(40 * (1 - i / 80))
        bd2.ellipse([(W//2 - 200 - i*2, 20 - i), (W//2 + 200 + i*2, 180 + i)],
                    fill=(140, 60, 200, alpha))
    base = comp(base, bl2)

    return base


def img_lissitzky_20260323():
    """El Lissitzky Constructivism — computer use / tooling theme."""
    # Cream/white background
    base = Image.new("RGB", (W, H), (245, 242, 232))

    # 1. Large bold diagonal red bar — Lissitzky's signature red wedge
    rl = layer()
    rd = ImageDraw.Draw(rl)
    rd.polygon([(0, 420), (580, 0), (680, 0), (100, 420)], fill=(210, 25, 25, 240))
    base = comp(base, rl)

    # 2. Heavy black horizontal bar — constructivist structure
    bl = layer()
    bd = ImageDraw.Draw(bl)
    bd.rectangle([(0, 280), (1200, 330)], fill=(15, 15, 15, 255))
    base = comp(base, bl)

    # 3. Bold black vertical bar — right side anchor
    vl = layer()
    vd = ImageDraw.Draw(vl)
    vd.rectangle([(880, 0), (940, 630)], fill=(15, 15, 15, 255))
    base = comp(base, vl)

    # 4. Red circle — Lissitzky's focal point element
    cl = layer()
    cd = ImageDraw.Draw(cl)
    cd.ellipse([(980, 60), (1160, 240)], fill=(210, 25, 25, 230))
    base = comp(base, cl)

    # 5. Thin diagonal black lines — constructivist grid tension
    ll = layer()
    ld = ImageDraw.Draw(ll)
    for i in range(6):
        x_off = i * 60
        ld.line([(700 + x_off, 0), (700 + x_off - 180, 280)], fill=(15, 15, 15, 200), width=4)
    base = comp(base, ll)

    # 6. Small black filled square — geometric punctuation
    sl = layer()
    sd = ImageDraw.Draw(sl)
    sd.rectangle([(60, 60), (200, 200)], fill=(15, 15, 15, 255))
    # White inner square — negative space
    sd.rectangle([(90, 90), (170, 170)], fill=(245, 242, 232, 255))
    base = comp(base, sl)

    # 7. Red thin diagonal accent lines — lower right
    al = layer()
    ad = ImageDraw.Draw(al)
    for i in range(5):
        y_off = i * 30
        ad.line([(950, 380 + y_off), (1190, 460 + y_off)], fill=(210, 25, 25, 180), width=3)
    base = comp(base, al)

    return base


def img_moholy_20260324():
    """László Moholy-Nagy Bauhaus — transparency, IPO, court theme."""
    # White background
    base = Image.new("RGB", (W, H), (252, 252, 252))

    # 1. Large transparent overlapping circles — Moholy-Nagy's core motif
    circles = [
        (300, 220, 220, (220, 40, 40, 90)),    # red
        (520, 300, 200, (30, 80, 200, 80)),    # blue
        (420, 180, 180, (240, 200, 0, 70)),    # yellow
        (680, 260, 160, (30, 80, 200, 70)),    # blue smaller
        (260, 380, 140, (220, 40, 40, 60)),    # red smaller
    ]
    for cx, cy, r, col in circles:
        cl = layer()
        cd = ImageDraw.Draw(cl)
        cd.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=col, outline=(0, 0, 0, 120), width=3)
        base = comp(base, cl)

    # 2. Overlapping semi-transparent rectangles — Bauhaus geometry
    rects = [
        (700, 80, 1100, 380, (30, 80, 200, 50)),   # large blue rect
        (820, 180, 1180, 500, (220, 40, 40, 45)),   # large red rect
        (750, 300, 1050, 580, (240, 200, 0, 55)),   # yellow rect
    ]
    for x0, y0, x1, y1, col in rects:
        rl = layer()
        rd = ImageDraw.Draw(rl)
        rd.rectangle([(x0, y0), (x1, y1)], fill=col, outline=(0, 0, 0, 100), width=2)
        base = comp(base, rl)

    # 3. Thin black structural lines — Bauhaus grid
    gl = layer()
    gd = ImageDraw.Draw(gl)
    # Horizontal
    for y in [160, 315, 470]:
        gd.line([(0, y), (1200, y)], fill=(20, 20, 20, 180), width=2)
    # Vertical
    for x in [420, 700, 950]:
        gd.line([(x, 0), (x, 630)], fill=(20, 20, 20, 180), width=2)
    base = comp(base, gl)

    # 4. Solid primary accent shapes — small anchors
    al = layer()
    ad = ImageDraw.Draw(al)
    # Black filled circle top-right
    ad.ellipse([(1050, 30), (1150, 130)], fill=(15, 15, 15, 255))
    # Red small square bottom-left
    ad.rectangle([(40, 490), (160, 590)], fill=(210, 25, 25, 255))
    # Yellow triangle lower centre
    ad.polygon([(560, 580), (640, 420), (720, 580)], fill=(220, 185, 0, 220))
    base = comp(base, al)

    # 5. Scatter of tiny primary dots — photogram texture
    dl = layer()
    dd = ImageDraw.Draw(dl)
    dot_cols = [(210, 25, 25, 160), (30, 80, 200, 160), (220, 185, 0, 160), (15, 15, 15, 140)]
    for _ in range(120):
        dx = rng.randint(0, W)
        dy = rng.randint(0, H)
        dr = rng.randint(3, 9)
        col = dot_cols[rng.randint(0, 3)]
        dd.ellipse([(dx-dr, dy-dr), (dx+dr, dy+dr)], fill=col)
    base = comp(base, dl)

    return base


def img_klimt_20260301():
    """Gustav Klimt — App Store No.1 viral surge + API best practices."""
    base = Image.new("RGB", (W, H), (12, 8, 20))

    # 1. Dense gold spiral field — Klimt's mosaic-gold background
    sl = layer()
    sd = ImageDraw.Draw(sl)
    for _ in range(320):
        sx = rng.randint(0, W)
        sy = rng.randint(0, H)
        sr = rng.randint(2, 7)
        alpha = rng.randint(80, 200)
        sd.ellipse([(sx-sr, sy-sr), (sx+sr, sy+sr)], fill=(218, 165, 32, alpha))
    base = comp(base, sl)

    # 2. Large Klimt-style portrait oval — central composition
    ol = layer()
    od = ImageDraw.Draw(ol)
    od.ellipse([(350, 60), (850, 420)], fill=(44, 28, 12, 210), outline=(218, 165, 32, 255), width=6)
    base = comp(base, ol)

    # 3. Mosaic fragments — gold/teal/rust geometric patches
    ml = layer()
    md = ImageDraw.Draw(ml)
    patches = [
        (120, 80,  220, 160, (218, 165, 32, 160)),
        (940, 100, 1060, 200, (30, 130, 120, 160)),
        (80,  440, 200, 540, (180, 80, 20, 150)),
        (1000, 380, 1150, 500, (218, 165, 32, 140)),
        (200, 540, 360, 620, (30, 130, 120, 140)),
        (860, 520, 1060, 610, (180, 80, 20, 130)),
    ]
    for px0, py0, px1, py1, col in patches:
        md.rectangle([(px0, py0), (px1, py1)], fill=col)
    base = comp(base, ml)

    # 4. Gold spiral arcs on the oval — Klimt's decorative layering
    al = layer()
    ad = ImageDraw.Draw(al)
    for i in range(8):
        angle_start = i * 45
        r_var = 60 + i * 15
        ad.arc([(600 - r_var, 200 - r_var), (600 + r_var, 200 + r_var)],
               start=angle_start, end=angle_start + 120,
               fill=(218, 165, 32, 160 - i * 12), width=4)
    base = comp(base, al)

    # 5. Teal/rust accent dots — mosaic tesserae
    dl = layer()
    dd = ImageDraw.Draw(dl)
    accent_colors = [(30, 130, 120, 200), (180, 80, 20, 200), (218, 165, 32, 220)]
    for _ in range(80):
        dx = rng.randint(0, W)
        dy = rng.randint(0, H)
        dr = rng.randint(4, 10)
        col = accent_colors[rng.randint(0, 2)]
        dd.ellipse([(dx-dr, dy-dr), (dx+dr, dy+dr)], fill=col)
    base = comp(base, dl)

    return base


def img_mondrian_20260302():
    """Piet Mondrian — outage / memory / migration grid."""
    base = Image.new("RGB", (W, H), (245, 241, 228))
    draw = ImageDraw.Draw(base)

    YELLOW = (255, 210, 0)
    RED    = (218, 38, 38)
    BLUE   = (28, 76, 196)
    BLACK  = (18, 18, 18)
    BW     = 14

    # Grid coordinates
    vx = [0, 180, 340, 520, 700, 870, 1050, W]
    hy = [0, 100, 220, 360, 480, H]

    # 1. Vertical black lines
    for x in vx[1:-1]:
        draw.rectangle([(x - BW//2, 0), (x + BW//2, H)], fill=BLACK)

    # 2. Horizontal black lines
    for y in hy[1:-1]:
        draw.rectangle([(0, y - BW//2), (W, y + BW//2)], fill=BLACK)

    # 3. Coloured rectangles in selected cells
    inset = BW // 2 + 2
    coloured = [
        (0, 0, RED),   (3, 2, BLUE),  (5, 0, RED),
        (1, 3, YELLOW),(4, 1, BLUE),  (2, 4, RED),
        (6, 2, YELLOW),(0, 4, BLUE),  (5, 3, YELLOW),
    ]
    for ci, ri, col in coloured:
        x0 = vx[ci] + inset
        y0 = hy[ri] + inset
        x1 = vx[ci + 1] - inset
        y1 = hy[ri + 1] - inset
        draw.rectangle([(x0, y0), (x1, y1)], fill=col)

    return base


def img_rothko_20260303():
    """Mark Rothko Colour Field — AI governance / deep context."""
    # Three hazy stacked colour bands
    base = Image.new("RGB", (W, H), (28, 18, 48))

    # 1. Top band — deep indigo/violet
    tl = layer()
    td = ImageDraw.Draw(tl)
    td.rectangle([(0, 0), (W, 240)], fill=(55, 30, 110, 230))
    base = comp(base, tl)

    # 2. Middle band — rich burnt sienna
    ml = layer()
    md = ImageDraw.Draw(ml)
    md.rectangle([(0, 210), (W, 440)], fill=(168, 62, 28, 220))
    base = comp(base, ml)

    # 3. Lower band — muted warm gold
    ll = layer()
    ld = ImageDraw.Draw(ll)
    ld.rectangle([(0, 410), (W, H)], fill=(192, 138, 38, 200))
    base = comp(base, ll)

    # 4. Luminous soft edge — blur simulation via thin translucent strips
    for i in range(20):
        el = layer()
        ed = ImageDraw.Draw(el)
        alpha = 30 - i
        ed.rectangle([(0, 230 + i * 2), (W, 232 + i * 2)], fill=(255, 140, 60, alpha))
        ed.rectangle([(0, 406 - i * 2), (W, 408 - i * 2)], fill=(255, 200, 60, alpha))
        base = comp(base, el)

    # 5. Warm centre glow
    gl = layer()
    gd = ImageDraw.Draw(gl)
    gd.ellipse([(200, 180), (1000, 460)], fill=(220, 100, 40, 40))
    base = comp(base, gl)

    return base


def img_malevich_20260304():
    """Kazimir Malevich — Pentagon supply chain designation — safety absolutes."""
    base = Image.new("RGB", (W, H), (238, 234, 218))

    # 1. Large tilted black square — Suprematist anchor
    bl = layer()
    bd = ImageDraw.Draw(bl)
    cx, cy, s = 580, 270, 220
    angle_pts = [
        (cx - s, cy - 30), (cx + 30, cy - s),
        (cx + s, cy + 30), (cx - 30, cy + s),
    ]
    bd.polygon(angle_pts, fill=(18, 18, 18, 255))
    base = comp(base, bl)

    # 2. Bold red rectangle — Malevich's primary accent
    rl = layer()
    rd = ImageDraw.Draw(rl)
    rd.rectangle([(820, 80), (1130, 210)], fill=(210, 28, 28, 240))
    base = comp(base, rl)

    # 3. Navy elongated shape — tilted
    nl = layer()
    nd = ImageDraw.Draw(nl)
    nd.polygon([(80, 480), (340, 420), (420, 580), (160, 620)], fill=(28, 40, 120, 230))
    base = comp(base, nl)

    # 4. Yellow thin bar — diagonal
    yl = layer()
    yd = ImageDraw.Draw(yl)
    yd.polygon([(700, 460), (1180, 400), (1185, 440), (705, 500)], fill=(235, 195, 0, 220))
    base = comp(base, yl)

    # 5. Small white circle — Suprematist floating element
    wl = layer()
    wd = ImageDraw.Draw(wl)
    wd.ellipse([(160, 80), (290, 210)], fill=(238, 234, 218, 240), outline=(18, 18, 18, 200), width=3)
    base = comp(base, wl)

    return base


def img_lissitzky_20260305():
    """El Lissitzky — Anthropic public statement / labour market research."""
    base = Image.new("RGB", (W, H), (244, 241, 230))

    # 1. Red diagonal wedge — Lissitzky 'Beat the Whites' motif
    rl = layer()
    rd = ImageDraw.Draw(rl)
    rd.polygon([(0, 540), (620, 0), (730, 0), (115, 540)], fill=(208, 22, 22, 240))
    base = comp(base, rl)

    # 2. Bold black vertical bar — right anchor
    vl = layer()
    vd = ImageDraw.Draw(vl)
    vd.rectangle([(860, 0), (920, H)], fill=(15, 15, 15, 255))
    base = comp(base, vl)

    # 3. Heavy black horizontal bar — structural rule
    hl = layer()
    hd = ImageDraw.Draw(hl)
    hd.rectangle([(0, 300), (W, 348)], fill=(15, 15, 15, 255))
    base = comp(base, hl)

    # 4. Red circle — upper right focal point
    cl = layer()
    cd = ImageDraw.Draw(cl)
    cd.ellipse([(960, 50), (1150, 240)], fill=(208, 22, 22, 220))
    base = comp(base, cl)

    # 5. Parallel thin black lines — upper right hatching
    ll = layer()
    ld = ImageDraw.Draw(ll)
    for i in range(7):
        ox = i * 50
        ld.line([(720 + ox, 0), (720 + ox - 160, 298)], fill=(15, 15, 15, 180), width=3)
    base = comp(base, ll)

    # 6. Black framed square — lower left logo element
    sql = layer()
    sqd = ImageDraw.Draw(sql)
    sqd.rectangle([(50, 50), (200, 200)], fill=(15, 15, 15, 255))
    sqd.rectangle([(78, 78), (172, 172)], fill=(244, 241, 230, 255))
    base = comp(base, sql)

    return base


def img_balla_20260306():
    """Giacomo Balla Futurism — 1M daily sign-ups, viral growth speed."""
    base = Image.new("RGB", (W, H), (10, 10, 18))

    # Vanishing point at center-left
    vp = (180, 315)

    # 1. Radiating coloured planes from VP — Balla's speed vectors
    colours = [
        (230, 60, 40, 200), (240, 180, 0, 190), (40, 120, 220, 190),
        (180, 40, 200, 160), (40, 200, 100, 160), (230, 60, 40, 140),
        (240, 180, 0, 140), (40, 120, 220, 140),
    ]
    angles = [i * (360 / len(colours)) for i in range(len(colours))]
    for i, (col, ang) in enumerate(zip(colours, angles)):
        rad = math.radians(ang)
        ex = int(vp[0] + 1400 * math.cos(rad))
        ey = int(vp[1] + 1400 * math.sin(rad))
        rad2 = math.radians(ang + 360 / len(colours))
        ex2 = int(vp[0] + 1400 * math.cos(rad2))
        ey2 = int(vp[1] + 1400 * math.sin(rad2))
        pl = layer()
        pd = ImageDraw.Draw(pl)
        pd.polygon([vp, (ex, ey), (ex2, ey2)], fill=col)
        base = comp(base, pl)

    # 2. Motion lines radiating outward
    ll = layer()
    ld = ImageDraw.Draw(ll)
    for i in range(24):
        ang = i * 15
        rad = math.radians(ang)
        lx = int(vp[0] + 900 * math.cos(rad))
        ly = int(vp[1] + 900 * math.sin(rad))
        ld.line([vp, (lx, ly)], fill=(255, 255, 255, 50), width=2)
    base = comp(base, ll)

    # 3. Bright white flash at VP
    fl = layer()
    fd = ImageDraw.Draw(fl)
    fd.ellipse([(vp[0]-50, vp[1]-50), (vp[0]+50, vp[1]+50)], fill=(255, 255, 255, 220))
    base = comp(base, fl)

    # 4. Speed arc streaks — concentric arcs from VP
    al = layer()
    ad = ImageDraw.Draw(al)
    for r in [120, 200, 310, 450]:
        ad.arc([(vp[0]-r, vp[1]-r), (vp[0]+r, vp[1]+r)],
               start=340, end=200, fill=(255, 255, 255, 100), width=3)
    base = comp(base, al)

    return base


def img_klee_20260307():
    """Paul Klee — multi-agent architecture / whoa moment."""
    base = Image.new("RGB", (W, H), (22, 18, 28))

    GRID_W = 10
    GRID_H = 7
    cw = W // GRID_W
    ch = H // GRID_H

    # 1. Warm-to-cool colour grid cells
    warm = [(200, 90, 20), (210, 130, 10), (180, 60, 40)]
    cool = [(20, 80, 170), (40, 130, 140), (60, 40, 120)]
    cell_colors = []
    for row in range(GRID_H):
        for col in range(GRID_W):
            t = col / (GRID_W - 1)
            r_blend = (1 - t)
            if row % 2 == 0:
                src = warm[row % len(warm)]
                dst = cool[col % len(cool)]
            else:
                src = cool[row % len(cool)]
                dst = warm[col % len(warm)]
            col_rgb = tuple(int(src[k] * (1-t) + dst[k] * t) for k in range(3))
            alpha = rng.randint(160, 220)
            cell_colors.append(col_rgb + (alpha,))

    for idx, col in enumerate(cell_colors):
        row = idx // GRID_W
        ci  = idx % GRID_W
        x0, y0 = ci * cw, row * ch
        cl = layer()
        cd = ImageDraw.Draw(cl)
        cd.rectangle([(x0 + 3, y0 + 3), (x0 + cw - 3, y0 + ch - 3)], fill=col)
        base = comp(base, cl)

    # 2. Dark grid lines
    gl = layer()
    gd = ImageDraw.Draw(gl)
    for c in range(GRID_W + 1):
        gd.line([(c * cw, 0), (c * cw, H)], fill=(18, 15, 25, 255), width=4)
    for r in range(GRID_H + 1):
        gd.line([(0, r * ch), (W, r * ch)], fill=(18, 15, 25, 255), width=4)
    base = comp(base, gl)

    # 3. White node circles at grid intersections
    nl = layer()
    nd = ImageDraw.Draw(nl)
    for ci in range(GRID_W + 1):
        for ri in range(GRID_H + 1):
            r = 7
            nd.ellipse([(ci*cw - r, ri*ch - r), (ci*cw + r, ri*ch + r)],
                       fill=(255, 255, 255, 200), outline=(18, 15, 25, 255), width=2)
    base = comp(base, nl)

    # 4. Connector lines between select nodes — "agent network"
    al = layer()
    ad = ImageDraw.Draw(al)
    connections = [(0,0,3,2),(1,1,4,0),(2,2,5,3),(3,0,6,2),(5,1,8,3),(6,0,9,1),(2,4,7,5),(4,3,7,4)]
    for c1, r1, c2, r2 in connections:
        ad.line([(c1*cw, r1*ch), (c2*cw, r2*ch)], fill=(255, 230, 80, 120), width=3)
    base = comp(base, al)

    return base


def img_delaunay_20260308():
    """Robert Delaunay — prompt caching / cross-platform signals / spectral rings."""
    base = Image.new("RGB", (W, H), (14, 12, 32))

    # 1. Large overlapping spectral ring discs
    discs = [
        (300, 260, 260),
        (700, 200, 220),
        (520, 400, 190),
        (950, 350, 240),
        (150, 450, 180),
    ]
    spectrum = [
        (220, 30, 30), (220, 120, 0), (200, 200, 0),
        (30, 180, 30), (0, 100, 210), (100, 0, 200),
    ]
    for cx, cy, max_r in discs:
        for i, col in enumerate(reversed(spectrum)):
            r = max_r - i * (max_r // len(spectrum))
            if r <= 0:
                continue
            rl = layer()
            rd = ImageDraw.Draw(rl)
            alpha = 180 - i * 18
            rd.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=col + (alpha,))
            base = comp(base, rl)

    # 2. White centre sparks at each disc centre
    wl = layer()
    wd = ImageDraw.Draw(wl)
    for cx, cy, _ in discs:
        wd.ellipse([(cx-10, cy-10), (cx+10, cy+10)], fill=(255, 255, 255, 220))
    base = comp(base, wl)

    # 3. Thin white radiating lines from largest disc
    ll = layer()
    ld = ImageDraw.Draw(ll)
    for i in range(16):
        ang = i * (360 / 16)
        rad = math.radians(ang)
        lx = int(300 + 320 * math.cos(rad))
        ly = int(260 + 320 * math.sin(rad))
        ld.line([(300, 260), (lx, ly)], fill=(255, 255, 255, 60), width=1)
    base = comp(base, ll)

    # 4. Small scattered spectrum dots — signal noise
    dl = layer()
    dd = ImageDraw.Draw(dl)
    for i in range(100):
        dx = rng.randint(0, W)
        dy = rng.randint(0, H)
        dr = rng.randint(3, 8)
        col = spectrum[rng.randint(0, len(spectrum)-1)]
        dd.ellipse([(dx-dr, dy-dr), (dx+dr, dy+dr)], fill=col + (140,))
    base = comp(base, dl)

    return base


def img_miro_20260309():
    """Joan Miró — Anthropic files lawsuit + M365 E7 bundle — bold biomorphic."""
    base = Image.new("RGB", (W, H), (22, 18, 72))

    # 1. Large biomorphic blob — red primary
    b1 = layer()
    b1d = ImageDraw.Draw(b1)
    b1d.ellipse([(80, 120), (420, 440)], fill=(218, 32, 32, 210))
    base = comp(base, b1)

    # 2. Yellow irregular blob — middle
    b2 = layer()
    b2d = ImageDraw.Draw(b2)
    b2d.polygon([(520, 60), (720, 40), (780, 180), (690, 320), (510, 280), (440, 140)],
                fill=(238, 200, 0, 200))
    base = comp(base, b2)

    # 3. Blue large rounded shape — right
    b3 = layer()
    b3d = ImageDraw.Draw(b3)
    b3d.ellipse([(820, 200), (1140, 520)], fill=(30, 80, 210, 190))
    base = comp(base, b3)

    # 4. Black bold outlines / contour lines
    ol = layer()
    od = ImageDraw.Draw(ol)
    od.ellipse([(80, 120), (420, 440)], outline=(10, 8, 18, 255), width=8)
    od.polygon([(520, 60), (720, 40), (780, 180), (690, 320), (510, 280), (440, 140)],
               outline=(10, 8, 18, 255), width=6)
    od.ellipse([(820, 200), (1140, 520)], outline=(10, 8, 18, 255), width=8)
    base = comp(base, ol)

    # 5. Miró stars — scattered asterisk stars
    stl = layer()
    std = ImageDraw.Draw(stl)
    stars = [(250, 80), (600, 520), (950, 100), (1100, 420), (400, 560), (730, 350)]
    for sx, sy in stars:
        for ang in range(0, 360, 60):
            rad = math.radians(ang)
            ex = int(sx + 28 * math.cos(rad))
            ey = int(sy + 28 * math.sin(rad))
            std.line([(sx, sy), (ex, ey)], fill=(255, 255, 255, 230), width=4)
        std.ellipse([(sx-7, sy-7), (sx+7, sy+7)], fill=(255, 255, 255, 255))
    base = comp(base, stl)

    # 6. Fine black line connecting blobs — Miró's characteristic thin connector
    ll = layer()
    ld = ImageDraw.Draw(ll)
    ld.line([(250, 280), (520, 180), (820, 360)], fill=(10, 8, 18, 200), width=5)
    base = comp(base, ll)

    return base


def img_franz_marc_20260325():
    """Franz Marc — rich jewel tones, stylised figures — 81k voices / human diversity theme."""
    # Deep cobalt background — Franz Marc's signature jewel-tone richness
    base = Image.new("RGB", (W, H), (18, 38, 108))

    # 1. Large emerald green organic form — lower left (earth / grounding)
    g1 = layer()
    g1d = ImageDraw.Draw(g1)
    g1d.ellipse([(-60, 280), (420, 680)], fill=(20, 160, 80, 200))
    base = comp(base, g1)

    # 2. Crimson curved shape — upper right (passion / energy)
    r1 = layer()
    r1d = ImageDraw.Draw(r1)
    r1d.ellipse([(780, -60), (1280, 380)], fill=(200, 30, 50, 190))
    base = comp(base, r1)

    # 3. Amber/gold diagonal wedge — centre sweep (light / aspiration)
    a1 = layer()
    a1d = ImageDraw.Draw(a1)
    a1d.polygon([(300, 580), (700, 80), (900, 120), (500, 630)], fill=(220, 170, 20, 170))
    base = comp(base, a1)

    # 4. Deep violet arc shape — upper left (mystery / concern)
    v1 = layer()
    v1d = ImageDraw.Draw(v1)
    v1d.pieslice([(-100, -100), (500, 400)], start=0, end=80, fill=(100, 20, 180, 160))
    base = comp(base, v1)

    # 5. Teal overlapping ellipse — mid-right (balance / connection)
    t1 = layer()
    t1d = ImageDraw.Draw(t1)
    t1d.ellipse([(680, 280), (1100, 620)], fill=(0, 160, 180, 150))
    base = comp(base, t1)

    # 6. Bold black contour outlines — Franz Marc's defining outline language
    ol = layer()
    od = ImageDraw.Draw(ol)
    od.ellipse([(-60, 280), (420, 680)], outline=(8, 8, 20, 255), width=7)
    od.ellipse([(780, -60), (1280, 380)], outline=(8, 8, 20, 255), width=7)
    od.ellipse([(680, 280), (1100, 620)], outline=(8, 8, 20, 255), width=5)
    od.pieslice([(-100, -100), (500, 400)], start=0, end=80, outline=(8, 8, 20, 255), width=5)
    base = comp(base, ol)

    # 7. Scattered small jewel circles — representing 159 countries / 81k voices
    dots = layer()
    dd = ImageDraw.Draw(dots)
    jewel_cols = [
        (220, 60, 60, 210), (30, 200, 100, 200), (240, 190, 10, 210),
        (60, 80, 220, 200), (200, 80, 180, 200), (0, 200, 200, 190),
        (240, 130, 30, 210), (80, 40, 200, 200),
    ]
    dot_positions = [
        (160, 140), (340, 220), (520, 340), (640, 480), (820, 180),
        (980, 400), (1100, 140), (200, 520), (460, 160), (760, 540),
        (1040, 520), (580, 80), (880, 350), (300, 390), (700, 260),
        (1150, 300), (100, 400), (440, 550), (960, 80),
    ]
    radii_dots = [22, 16, 28, 18, 24, 14, 20, 26, 12, 18, 22, 16, 20, 14, 24, 18, 12, 16, 20]
    for i, (px, py) in enumerate(dot_positions):
        col = jewel_cols[i % len(jewel_cols)]
        r = radii_dots[i % len(radii_dots)]
        dl2 = layer()
        dd2 = ImageDraw.Draw(dl2)
        dd2.ellipse([(px-r, py-r), (px+r, py+r)], fill=col, outline=(8, 8, 20, 200), width=2)
        base = comp(base, dl2)

    # 8. White highlight strokes — Franz Marc's luminous edge detail
    hl = layer()
    hd = ImageDraw.Draw(hl)
    hd.line([(320, 80), (520, 240)], fill=(255, 255, 255, 100), width=3)
    hd.line([(700, 100), (820, 280)], fill=(255, 255, 255, 80), width=2)
    hd.line([(200, 300), (380, 440)], fill=(255, 255, 255, 70), width=2)
    hd.line([(900, 200), (1050, 360)], fill=(255, 255, 255, 90), width=3)
    base = comp(base, hl)

    return base


def img_klee_20260326():
    """Paul Klee 'Polyphony' style — global network, India expansion, infrastructure cells."""
    base = Image.new("RGB", (W, H), (18, 22, 38))
    draw = ImageDraw.Draw(base)

    # 1. Irregular Klee-style colour grid — warm/cool zones suggesting global reach
    cell_w, cell_h = 80, 58
    cols = math.ceil(W / cell_w) + 1
    rows = math.ceil(H / cell_h) + 1

    india_palette   = [(200, 80, 30),  (220, 130, 40), (240, 160, 60), (210, 60, 80),
                       (190, 100, 40), (230, 90, 50),  (200, 150, 70), (215, 45, 55)]
    ocean_palette   = [(30, 80, 160),  (50, 110, 190), (70, 140, 210), (30, 60, 140),
                       (55, 130, 175), (75, 160, 200), (35, 95, 155),  (60, 75, 145)]
    infra_palette   = [(60, 140, 90),  (80, 160, 110), (100, 180, 130),(55, 120, 80),
                       (90, 150, 100), (70, 170, 120), (50, 130, 95),  (110, 165, 115)]

    for row in range(rows):
        y0 = row * cell_h
        y_center = y0 + cell_h // 2
        for col in range(cols):
            x0 = col * cell_w
            x_center = x0 + cell_w // 2
            # Zone by position: right=India warmth, left=infra green, centre=ocean blue
            if x_center > W * 0.65:
                palette = india_palette
            elif x_center < W * 0.30:
                palette = infra_palette
            else:
                palette = ocean_palette
            idx = (row * 3 + col * 2) % len(palette)
            bc = palette[idx]
            r = max(0, min(255, bc[0] + rng.randint(-18, 18)))
            g = max(0, min(255, bc[1] + rng.randint(-18, 18)))
            b = max(0, min(255, bc[2] + rng.randint(-18, 18)))
            draw.rectangle([(x0, y0), (x0 + cell_w, y0 + cell_h)], fill=(r, g, b))

    # 2. Dark grid lines
    for col in range(cols + 1):
        draw.line([(col * cell_w, 0), (col * cell_w, H)], fill=(8, 8, 16), width=2)
    for row in range(rows + 1):
        draw.line([(0, row * cell_h), (W, row * cell_h)], fill=(8, 8, 16), width=2)

    # 3. Node circles — key network/infrastructure nodes
    node_positions = [
        (120, 90),   # infrastructure hub (west)
        (240, 200),  # data centre node
        (380, 130),  # mid-Atlantic connection
        (520, 270),  # central network
        (660, 160),  # relay node
        (800, 310),  # east hub
        (960, 140),  # India gateway
        (1080, 250), # Bengaluru terminus
        (450, 400),  # south connection
        (700, 480),  # lower data path
        (280, 470),  # western anchor
    ]
    for nx, ny in node_positions:
        r_n = rng.randint(14, 22)
        nl = layer()
        nd = ImageDraw.Draw(nl)
        nd.ellipse([(nx - r_n, ny - r_n), (nx + r_n, ny + r_n)],
                   fill=(255, 255, 255, 220), outline=(200, 200, 200, 180), width=2)
        base = comp(base, nl)

    # 4. Connection lines between nodes (Klee's network motif)
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
        (3, 8), (8, 9), (9, 5), (1, 10), (10, 8),
    ]
    cl = layer()
    cd = ImageDraw.Draw(cl)
    for (i, j) in connections:
        nx1, ny1 = node_positions[i]
        nx2, ny2 = node_positions[j]
        cd.line([(nx1, ny1), (nx2, ny2)], fill=(255, 255, 255, 100), width=2)
    base = comp(base, cl)

    # 5. Larger accent circles (Klee's layered disc motifs)
    accent_specs = [
        (580, 220, 90, (255, 200, 80, 60)),
        (150, 350, 70, (80, 200, 140, 50)),
        (960, 300, 80, (240, 100, 60, 55)),
    ]
    for ax, ay, ar, acol in accent_specs:
        al = layer()
        ad = ImageDraw.Draw(al)
        ad.ellipse([(ax - ar, ay - ar), (ax + ar, ay + ar)], fill=acol)
        base = comp(base, al)

    # 6. Fine dot scatter — Klee's texture
    scatter_l = layer()
    scatter_d = ImageDraw.Draw(scatter_l)
    for _ in range(300):
        sx = rng.randint(0, W)
        sy = rng.randint(0, H)
        sr = rng.randint(2, 5)
        alpha = rng.randint(40, 100)
        scatter_d.ellipse([(sx - sr, sy - sr), (sx + sr, sy + sr)],
                          fill=(255, 255, 255, alpha))
    base = comp(base, scatter_l)

    return base


# ── February 2026 retrospective motif functions ───────────────────────────────

def img_klee_20260201():
    """Paul Klee colour-cell grid — Cowork Launch / agent networks."""
    base = Image.new("RGB", (W, H), (28, 22, 18))
    draw = ImageDraw.Draw(base)
    cols = [
        (210, 90, 40), (240, 160, 60), (60, 130, 200), (80, 180, 100),
        (200, 60, 90), (130, 200, 220), (220, 200, 80), (100, 60, 180),
    ]
    cw, ch = W // 8, H // 5
    for row in range(5):
        for col in range(8):
            c = cols[(row * 3 + col) % len(cols)]
            r, g, b = c
            alpha = rng.randint(170, 240)
            cell_layer = layer()
            cd = ImageDraw.Draw(cell_layer)
            cd.rectangle([(col * cw + 3, row * ch + 3), ((col + 1) * cw - 3, (row + 1) * ch - 3)], fill=(r, g, b, alpha))
            base = comp(base, cell_layer)
    node_layer = layer()
    nd = ImageDraw.Draw(node_layer)
    for row in range(6):
        for col in range(9):
            nx, ny = col * cw, row * ch
            nd.ellipse([(nx - 7, ny - 7), (nx + 7, ny + 7)], fill=(255, 255, 255, 200), outline=(0, 0, 0, 220), width=2)
    base = comp(base, node_layer)
    line_layer = layer()
    ld = ImageDraw.Draw(line_layer)
    connections = [(0,0,1,1),(1,0,2,1),(3,1,4,2),(5,2,6,1),(7,0,6,2),(2,3,3,2),(4,3,5,4)]
    for (c1,r1,c2,r2) in connections:
        ld.line([(c1*cw, r1*ch),(c2*cw, r2*ch)], fill=(255,255,255,120), width=2)
    base = comp(base, line_layer)
    return base


def img_leger_20260202():
    """Fernand Léger mechanical style — Data Residency / infrastructure."""
    base = Image.new("RGB", (W, H), (18, 18, 24))
    draw = ImageDraw.Draw(base)
    shapes = [
        ("rect", (80, 60, 380, 200), (220, 50, 30)),
        ("rect", (420, 80, 700, 260), (30, 100, 200)),
        ("rect", (740, 50, 1100, 220), (220, 180, 20)),
        ("rect", (100, 300, 500, 480), (40, 180, 100)),
        ("rect", (540, 320, 880, 500), (180, 50, 200)),
        ("rect", (900, 280, 1160, 460), (220, 120, 30)),
        ("rect", (200, 520, 600, 610), (30, 160, 220)),
        ("rect", (640, 540, 1000, 625), (200, 50, 60)),
    ]
    for kind, coords, col in shapes:
        outline_layer = layer()
        od = ImageDraw.Draw(outline_layer)
        od.rectangle(coords, fill=(*col, 200), outline=(255, 255, 255, 255), width=4)
        base = comp(base, outline_layer)
    gear_layer = layer()
    gd = ImageDraw.Draw(gear_layer)
    gd.ellipse([(300, 200), (560, 460)], outline=(255, 255, 255, 200), width=8)
    gd.ellipse([(320, 220), (540, 440)], outline=(220, 180, 20, 160), width=4)
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        cx, cy = 430, 330
        gd.line([(cx, cy), (cx + int(120 * math.cos(rad)), cy + int(120 * math.sin(rad)))], fill=(255, 255, 255, 100), width=3)
    base = comp(base, gear_layer)
    pipe_layer = layer()
    pd = ImageDraw.Draw(pipe_layer)
    pd.line([(0, 315), (W, 315)], fill=(255, 255, 255, 80), width=6)
    pd.line([(600, 0), (600, H)], fill=(255, 255, 255, 80), width=6)
    base = comp(base, pipe_layer)
    return base


def img_mondrian_20260203():
    """Piet Mondrian grid style — Haiku Sunset / structured transitions."""
    base = Image.new("RGB", (W, H), (245, 240, 225))
    draw = ImageDraw.Draw(base)
    YELLOW = (255, 215, 0)
    RED    = (200, 40, 40)
    BLUE   = (30, 70, 180)
    BLACK  = (20, 20, 20)
    verticals   = [180, 360, 580, 800, 980]
    horizontals = [120, 280, 420, 540]
    bw = 14
    for x in verticals:
        draw.rectangle([(x - bw//2, 0), (x + bw//2, H)], fill=BLACK)
    for y in horizontals:
        draw.rectangle([(0, y - bw//2), (W, y + bw//2)], fill=BLACK)
    cells = [(0, 0, 180, 120, RED), (360, 280, 580, 420, BLUE), (800, 0, 980, 280, YELLOW),
             (980, 540, W, H, RED), (0, 420, 180, H, BLUE), (580, 420, 800, H, YELLOW)]
    for x0, y0, x1, y1, c in cells:
        draw.rectangle([(x0 + bw, y0 + bw), (x1 - bw, y1 - bw)], fill=c)
    return base


def img_lissitzky_20260204():
    """El Lissitzky Constructivism — EU Expansion / developer platform."""
    base = Image.new("RGB", (W, H), (240, 235, 220))
    draw = ImageDraw.Draw(base)
    RED   = (210, 30, 30)
    BLACK = (20, 20, 20)
    bars = [
        (40, 80, 560, 150, RED),
        (640, 200, 1180, 270, BLACK),
        (100, 350, 480, 400, BLACK),
        (520, 460, 1100, 520, RED),
        (80, 540, 400, 580, RED),
    ]
    for x0, y0, x1, y1, c in bars:
        bar_layer = layer()
        bd = ImageDraw.Draw(bar_layer)
        bd.rectangle([(x0, y0), (x1, y1)], fill=(*c, 240))
        base = comp(base, bar_layer)
    circle_layer = layer()
    cd = ImageDraw.Draw(circle_layer)
    cd.ellipse([(800, 60), (1100, 360)], outline=RED, width=14)
    cd.ellipse([(820, 80), (1080, 340)], outline=BLACK, width=6)
    base = comp(base, circle_layer)
    tri_layer = layer()
    td = ImageDraw.Draw(tri_layer)
    td.polygon([(200, 480), (500, 180), (500, 480)], fill=(*RED, 200))
    base = comp(base, tri_layer)
    return base


def img_klimt_20260205():
    """Gustav Klimt gold spirals — Opus 4.6 / models and craftsmanship."""
    base = Image.new("RGB", (W, H), (10, 8, 14))
    gold_layer = layer()
    gd = ImageDraw.Draw(gold_layer)
    for i in range(80):
        cx = rng.randint(0, W)
        cy = rng.randint(0, H)
        r  = rng.randint(8, 60)
        gd.arc([(cx-r, cy-r), (cx+r, cy+r)], start=rng.randint(0,360), end=rng.randint(10,340),
               fill=(212, 175, 55, rng.randint(80, 200)), width=rng.randint(1, 5))
    base = comp(base, gold_layer)
    mosaic_layer = layer()
    md = ImageDraw.Draw(mosaic_layer)
    for _ in range(200):
        mx = rng.randint(0, W-20)
        my = rng.randint(0, H-20)
        sz = rng.randint(4, 18)
        mc = [(212,175,55), (0,128,128), (160,60,30), (200,180,80), (80,40,120)][rng.randint(0,4)]
        md.rectangle([(mx, my), (mx+sz, my+sz)], fill=(*mc, rng.randint(120, 220)))
    base = comp(base, mosaic_layer)
    face_layer = layer()
    fd = ImageDraw.Draw(face_layer)
    fd.ellipse([(440, 80), (760, 460)], fill=(212, 175, 55, 60), outline=(212, 175, 55, 180), width=6)
    fd.ellipse([(480, 120), (720, 420)], fill=(0, 0, 0, 0), outline=(160, 120, 20, 150), width=3)
    base = comp(base, face_layer)
    return base


def img_kandinsky_20260206():
    """Wassily Kandinsky Composition — Agent Teams / multi-agent coordination."""
    base = Image.new("RGB", (W, H), (22, 40, 80))
    grid_layer = layer()
    gd = ImageDraw.Draw(grid_layer)
    for off in range(-H, W+H, 55):
        gd.line([(off,0),(off+H,H)], fill=(255,255,255,18), width=1)
        gd.line([(off,0),(off-H,H)], fill=(255,255,255,18), width=1)
    base = comp(base, grid_layer)
    shapes = [
        ("circle", (800, 30, 1100, 330), (255, 200, 0, 220)),
        ("triangle", [(100, 540), (380, 540), (240, 200)], (220, 30, 50, 220)),
        ("circle", (60, 60), 90, (255, 120, 20, 200)),
        ("rect", (550, 200, 750, 420), (30, 100, 220, 200)),
    ]
    s1 = layer(); ImageDraw.Draw(s1).ellipse([(800,30),(1100,330)], fill=(255,200,0,220)); base = comp(base, s1)
    s2 = layer(); ImageDraw.Draw(s2).polygon([(100,540),(380,540),(240,200)], fill=(220,30,50,220)); base = comp(base, s2)
    s3 = layer(); ImageDraw.Draw(s3).ellipse([(60-90,60-90),(60+90,60+90)], fill=(255,120,20,200)); base = comp(base, s3)
    s4 = layer(); ImageDraw.Draw(s4).rectangle([(550,200),(750,420)], fill=(30,100,220,200)); base = comp(base, s4)
    s5 = layer(); ImageDraw.Draw(s5).pieslice([(850,380),(1160,600)], 200, 360, fill=(60,200,80,200)); base = comp(base, s5)
    lines = layer(); ld = ImageDraw.Draw(lines)
    ld.line([(0,400),(500,100)], fill=(0,0,0,255), width=5)
    ld.line([(400,600),(900,200)], fill=(255,255,255,200), width=3)
    base = comp(base, lines)
    return base


def img_calder_20260207():
    """Alexander Calder mobile — Scientific AI / balanced flexible agents."""
    base = Image.new("RGB", (W, H), (248, 245, 240))
    arm_layer = layer()
    ad = ImageDraw.Draw(arm_layer)
    ad.line([(200, 80), (1000, 80)], fill=(20,20,20,255), width=4)
    ad.line([(600, 80), (600, 220)], fill=(20,20,20,255), width=3)
    ad.line([(200, 80), (200, 200)], fill=(20,20,20,255), width=3)
    ad.line([(1000, 80), (1000, 200)], fill=(20,20,20,255), width=3)
    ad.line([(300, 300), (800, 300)], fill=(20,20,20,255), width=3)
    ad.line([(300, 300), (300, 440)], fill=(20,20,20,255), width=2)
    ad.line([(800, 300), (800, 440)], fill=(20,20,20,255), width=2)
    ad.line([(200, 200), (500, 200)], fill=(20,20,20,255), width=2)
    ad.line([(350, 200), (350, 370)], fill=(20,20,20,255), width=2)
    base = comp(base, arm_layer)
    shapes_data = [
        ((140,160,260,270), (220,40,40)),
        ((560,60,720,220), (20,80,200)),
        ((940,160,1080,290), (220,200,0)),
        ((250,400,390,530), (220,100,20)),
        ((730,395,880,530), (40,160,80)),
        ((300,320,420,430), (160,20,180)),
        ((160,200,280,310), (0,160,200)),
    ]
    for bounds, col in shapes_data:
        sl = layer(); ImageDraw.Draw(sl).ellipse(bounds, fill=(*col, 230)); base = comp(base, sl)
    return base


def img_seurat_20260208():
    """Georges Seurat pointillism — Agent Teams rollout / data density."""
    base = Image.new("RGB", (W, H), (14, 20, 50))
    dot_layer = layer()
    dd = ImageDraw.Draw(dot_layer)
    for _ in range(4000):
        dx = rng.randint(0, W)
        dy = rng.randint(0, H)
        cx, cy = W * 0.55, H * 0.45
        dist = math.hypot(dx - cx, dy - cy)
        brightness = max(0, 1 - dist / 500)
        r_base = int(20 + brightness * 235)
        g_base = int(40 + brightness * 180)
        b_base = int(100 + brightness * 155)
        hue_shift = rng.randint(-30, 30)
        dr = rng.randint(2, 6)
        dd.ellipse([(dx-dr, dy-dr), (dx+dr, dy+dr)],
                   fill=(min(255,r_base+hue_shift), min(255,g_base), min(255,b_base), rng.randint(160,240)))
    base = comp(base, dot_layer)
    ring_layer = layer()
    rd = ImageDraw.Draw(ring_layer)
    for radius in [80, 160, 240, 340]:
        rd.arc([(W//2-radius-300, H//2-radius), (W//2+radius-300, H//2+radius)],
               0, 360, fill=(255,220,100,60), width=3)
    base = comp(base, ring_layer)
    return base


def img_franz_marc_20260209():
    """Franz Marc jewel tones — Interpretability / AI wellbeing."""
    base = Image.new("RGB", (W, H), (10, 40, 80))
    for col, bounds in [
        ((0,120,160), [(0,0),(400,H)]),
        ((20,80,40), [(300,0),(750,H)]),
        ((100,20,120), [(650,0),(W,H)]),
    ]:
        sl = layer(); ImageDraw.Draw(sl).rectangle(bounds, fill=(*col, 120)); base = comp(base, sl)
    curves = [([(100,400),(300,200),(500,350),(700,150),(900,300),(1100,100)], (255,200,80)),
              ([(50,300),(250,500),(450,280),(650,480),(850,200),(1100,400)], (100,220,255)),]
    for pts, col in curves:
        cl = layer(); ImageDraw.Draw(cl).line(pts, fill=(*col, 180), width=6); base = comp(base, cl)
    for cx, cy, r, c in [(300,250,80,(255,200,80)),(700,380,100,(100,220,255)),(1000,200,70,(220,100,200))]:
        el = layer(); ImageDraw.Draw(el).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(*c, 160), outline=(255,255,255,100), width=3); base = comp(base, el)
    return base


def img_balla_20260210():
    """Giacomo Balla Futurism — Cowork Windows launch / speed and motion."""
    base = Image.new("RGB", (W, H), (8, 8, 12))
    vp_x, vp_y = 600, 315
    for i in range(24):
        angle = math.radians(i * 15)
        length = rng.randint(300, 700)
        ex = int(vp_x + length * math.cos(angle))
        ey = int(vp_y + length * math.sin(angle))
        colors = [(220,60,20),(255,140,0),(200,200,0),(60,200,220),(100,60,200),(220,20,100)]
        col = colors[i % len(colors)]
        pl = layer(); ImageDraw.Draw(pl).line([(vp_x, vp_y),(ex, ey)], fill=(*col, 140), width=rng.randint(2,8)); base = comp(base, pl)
    for i in range(12):
        angle = math.radians(i * 30 + 7)
        length = rng.randint(200, 500)
        end_x = int(vp_x + length * math.cos(angle))
        end_y = int(vp_y + length * math.sin(angle))
        pw = rng.randint(20, 80)
        ph = rng.randint(10, 40)
        colors2 = [(220,60,20),(255,140,0),(60,200,220),(200,200,0)]
        col2 = colors2[i % len(colors2)]
        sx = (vp_x + end_x) // 2
        sy = (vp_y + end_y) // 2
        pl2 = layer(); ImageDraw.Draw(pl2).ellipse([(sx-pw//2, sy-ph//2),(sx+pw//2, sy+ph//2)], fill=(*col2, 180)); base = comp(base, pl2)
    core = layer(); ImageDraw.Draw(core).ellipse([(vp_x-30, vp_y-30),(vp_x+30, vp_y+30)], fill=(255,255,255,240)); base = comp(base, core)
    return base


def img_delaunay_20260211():
    """Robert Delaunay spectral rings — Web Fetch / signals and dispatch."""
    base = Image.new("RGB", (W, H), (8, 8, 14))
    spectral = [(220,20,60),(255,80,0),(255,200,0),(40,220,40),(0,180,255),(80,0,255),(160,0,200)]
    for i, col in enumerate(spectral):
        r = 80 + i * 60
        cx1, cy1 = W // 3, H // 2
        ring1 = layer(); ImageDraw.Draw(ring1).arc([(cx1-r, cy1-r),(cx1+r, cy1+r)], 0, 360, fill=(*col, 130), width=22); base = comp(base, ring1)
    for i, col in enumerate(spectral):
        r = 60 + i * 50
        cx2, cy2 = 2 * W // 3, H // 2
        ring2 = layer(); ImageDraw.Draw(ring2).arc([(cx2-r, cy2-r),(cx2+r, cy2+r)], 0, 360, fill=(*col, 100), width=18); base = comp(base, ring2)
    overlap = layer(); ImageDraw.Draw(overlap).ellipse([(W//2-80, H//2-80),(W//2+80, H//2+80)], fill=(255,255,255,40)); base = comp(base, overlap)
    return base


def img_mondrian_20260212():
    """Piet Mondrian grid — MCP 10K servers / structured ecosystem."""
    base = Image.new("RGB", (W, H), (248, 242, 228))
    draw = ImageDraw.Draw(base)
    BLACK = (15, 15, 15)
    RED   = (210, 35, 35)
    BLUE  = (25, 65, 190)
    YELLOW= (255, 210, 0)
    verts = [90, 250, 430, 620, 820, 1020, 1150]
    horizs = [90, 210, 350, 480, 580]
    bw = 12
    for x in verts:
        draw.rectangle([(x-bw//2,0),(x+bw//2,H)], fill=BLACK)
    for y in horizs:
        draw.rectangle([(0,y-bw//2),(W,y+bw//2)], fill=BLACK)
    fills = [(0,0,90,210,RED),(250,210,430,350,BLUE),(620,0,820,210,YELLOW),
             (820,480,1020,H,RED),(0,350,90,H,BLUE),(1020,0,1150,350,YELLOW),
             (430,350,620,H,RED)]
    for x0,y0,x1,y1,c in fills:
        draw.rectangle([(x0+bw,y0+bw),(x1-bw,y1-bw)], fill=c)
    return base


def img_moholy_20260213():
    """László Moholy-Nagy Bauhaus — Analytics API / transparency and data."""
    base = Image.new("RGB", (W, H), (252, 250, 245))
    circles = [(300,315,240,(220,80,30)),(700,315,200,(30,80,200)),(1000,200,160,(220,180,20)),(500,450,140,(40,160,100))]
    for cx, cy, r, col in circles:
        for opacity in [40, 80, 150]:
            cl = layer(); ImageDraw.Draw(cl).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(*col,opacity), outline=(*col,220), width=4); base = comp(base, cl)
    rects = [(50,100,300,350,(30,80,200)),(800,200,1100,500,(220,80,30))]
    for x0,y0,x1,y1,col in rects:
        rl = layer(); ImageDraw.Draw(rl).rectangle([(x0,y0),(x1,y1)], fill=(*col,60), outline=(*col,200), width=5); base = comp(base, rl)
    ll = layer(); ld = ImageDraw.Draw(ll)
    ld.line([(0,315),(W,315)], fill=(0,0,0,180), width=3)
    ld.line([(600,0),(600,H)], fill=(0,0,0,180), width=3)
    base = comp(base, ll)
    return base


def img_malevich_20260214():
    """Kazimir Malevich geometric — Safety Research / absolutes."""
    base = Image.new("RGB", (W, H), (235, 228, 210))
    draw = ImageDraw.Draw(base)
    shapes = [
        ((150, 80, 520, 300), (20, 20, 20), 0),
        ((600, 150, 1050, 420), (200, 30, 30), -12),
        ((50, 380, 350, 600), (30, 50, 180), 8),
        ((800, 400, 1100, 590), (220, 180, 20), -5),
    ]
    for (x0,y0,x1,y1), col, angle in shapes:
        sl = layer()
        sd = ImageDraw.Draw(sl)
        cx, cy = (x0+x1)//2, (y0+y1)//2
        hw, hh = (x1-x0)//2, (y1-y0)//2
        pts = [(-hw,-hh),(hw,-hh),(hw,hh),(-hw,hh)]
        rad = math.radians(angle)
        rotated = [(int(cx + p[0]*math.cos(rad) - p[1]*math.sin(rad)),
                    int(cy + p[0]*math.sin(rad) + p[1]*math.cos(rad))) for p in pts]
        sd.polygon(rotated, fill=(*col, 240))
        base = comp(base, sl)
    return base


def img_klee_20260215():
    """Paul Klee grid — Risk Report / structured analysis cells."""
    base = Image.new("RGB", (W, H), (24, 18, 28))
    warm = [(200,80,40),(240,150,50),(180,100,60),(220,60,80)]
    cool = [(40,100,200),(60,160,220),(80,180,140),(100,80,200)]
    cw, ch = W // 10, H // 6
    for row in range(6):
        for col in range(10):
            palette = warm if (row + col) % 2 == 0 else cool
            c = palette[(row * 7 + col * 3) % len(palette)]
            alpha = rng.randint(160, 230)
            cl = layer(); ImageDraw.Draw(cl).rectangle([(col*cw+2,row*ch+2),((col+1)*cw-2,(row+1)*ch-2)], fill=(*c, alpha)); base = comp(base, cl)
    node_l = layer(); nd = ImageDraw.Draw(node_l)
    for row in range(7):
        for col in range(11):
            nd.ellipse([(col*cw-5, row*ch-5),(col*cw+5, row*ch+5)], fill=(255,255,255,180))
    base = comp(base, node_l)
    return base


def img_kandinsky_20260216():
    """Wassily Kandinsky — Economic Primitives / composition and reasoning."""
    base = Image.new("RGB", (W, H), (20, 35, 75))
    gl = layer(); gd = ImageDraw.Draw(gl)
    for off in range(-H, W+H, 50):
        gd.line([(off,0),(off+H,H)], fill=(255,255,255,15), width=1)
    base = comp(base, gl)
    el = layer(); ImageDraw.Draw(el).ellipse([(700,20),(1150,470)], fill=(255,210,0,210), outline=(0,0,0,255), width=6); base = comp(base, el)
    tl = layer(); ImageDraw.Draw(tl).polygon([(50,560),(350,560),(200,180)], fill=(60,180,220,210)); base = comp(base, tl)
    pl = layer(); ImageDraw.Draw(pl).pieslice([(880,350),(1180,580)], 180,340, fill=(30,100,220,190)); base = comp(base, pl)
    sl = layer(); sd = ImageDraw.Draw(sl)
    for px,py,c,r in [(120,100,(255,120,20,200),35),(400,60,(140,50,200,190),28),(550,300,(40,200,80,200),22),(700,500,(220,30,50,200),30)]:
        sd.ellipse([(px-r,py-r),(px+r,py+r)], fill=c, outline=(0,0,0,255), width=2)
    base = comp(base, sl)
    ll = layer(); ld = ImageDraw.Draw(ll)
    ld.line([(0,400),(450,90)], fill=(0,0,0,255), width=4)
    ld.line([(500,590),(950,200)], fill=(255,255,255,200), width=3)
    base = comp(base, ll)
    return base


def img_klimt_20260217():
    """Gustav Klimt — Sonnet 4.6 launch / model craftsmanship."""
    base = Image.new("RGB", (W, H), (12, 8, 18))
    for _ in range(100):
        cx = rng.randint(0, W); cy = rng.randint(0, H); r = rng.randint(6,50)
        al = layer(); ImageDraw.Draw(al).arc([(cx-r,cy-r),(cx+r,cy+r)], rng.randint(0,360), rng.randint(10,350), fill=(212,175,55,rng.randint(60,180)), width=rng.randint(1,4)); base = comp(base, al)
    for _ in range(250):
        mx = rng.randint(0,W-16); my = rng.randint(0,H-16); sz = rng.randint(3,14)
        mc = [(212,175,55),(0,140,140),(170,70,30),(210,190,90)][rng.randint(0,3)]
        ml = layer(); ImageDraw.Draw(ml).rectangle([(mx,my),(mx+sz,my+sz)], fill=(*mc, rng.randint(100,210))); base = comp(base, ml)
    fl = layer(); fd = ImageDraw.Draw(fl)
    fd.ellipse([(460,60),(780,440)], fill=(212,175,55,50), outline=(212,175,55,200), width=8)
    fd.ellipse([(500,100),(740,400)], outline=(100,80,20,120), width=3)
    base = comp(base, fl)
    return base


def img_calder_20260218():
    """Alexander Calder mobile — Opus Webinar / balanced adaptive thinking."""
    base = Image.new("RGB", (W, H), (250, 246, 240))
    al = layer(); ad = ImageDraw.Draw(al)
    ad.line([(100,100),(1100,100)], fill=(20,20,20,255), width=4)
    ad.line([(600,100),(600,260)], fill=(20,20,20,255), width=3)
    ad.line([(100,100),(100,220)], fill=(20,20,20,255), width=3)
    ad.line([(1100,100),(1100,220)], fill=(20,20,20,255), width=3)
    ad.line([(250,360),(750,360)], fill=(20,20,20,255), width=3)
    ad.line([(250,360),(250,490)], fill=(20,20,20,255), width=2)
    ad.line([(750,360),(750,490)], fill=(20,20,20,255), width=2)
    ad.line([(850,260),(1050,260)], fill=(20,20,20,255), width=2)
    ad.line([(850,260),(850,400)], fill=(20,20,20,255), width=2)
    ad.line([(1050,260),(1050,400)], fill=(20,20,20,255), width=2)
    base = comp(base, al)
    for bounds, col in [
        ((40,160,200,300),(220,40,40)), ((540,60,720,240),(20,80,200)),
        ((1040,160,1180,300),(220,200,0)), ((170,400,320,540),(220,100,20)),
        ((680,400,840,540),(40,160,80)), ((780,220,940,360),(160,20,180)),
        ((980,320,1120,460),(0,150,200)),
    ]:
        bl = layer(); ImageDraw.Draw(bl).ellipse(bounds, fill=(*col, 225)); base = comp(base, bl)
    return base


def img_lissitzky_20260219():
    """El Lissitzky — Model Sunset / CLI structured outputs."""
    base = Image.new("RGB", (W, H), (238, 232, 218))
    RED   = (215, 25, 25)
    BLACK = (18, 18, 18)
    for (x0,y0,x1,y1,c) in [(30,60,620,140,RED),(640,180,1180,260,BLACK),(80,320,520,385,BLACK),(560,440,1150,510,RED),(60,530,420,580,RED)]:
        bl = layer(); ImageDraw.Draw(bl).rectangle([(x0,y0),(x1,y1)], fill=(*c,240)); base = comp(base, bl)
    cl = layer(); cd = ImageDraw.Draw(cl)
    cd.ellipse([(820,40),(1100,320)], outline=RED, width=12)
    cd.ellipse([(835,55),(1085,305)], outline=BLACK, width=5)
    base = comp(base, cl)
    tl = layer(); ImageDraw.Draw(tl).polygon([(180,500),(460,220),(460,500)], fill=(*RED,190)); base = comp(base, tl)
    return base


def img_franz_marc_20260220():
    """Franz Marc — Transparency Hub / AI wellbeing and openness."""
    base = Image.new("RGB", (W, H), (8, 38, 76))
    for col, pts in [((0,110,150),[(0,0),(420,H)]),(( 15,72,36),[(310,0),(760,H)]),((95,15,115),[(660,0),(W,H)])]:
        sl = layer(); ImageDraw.Draw(sl).rectangle(pts, fill=(*col,115)); base = comp(base, sl)
    for pts, col in [([(80,420),(290,200),(510,360),(730,140),(960,290),(1160,80)],(255,210,80)),([(40,310),(260,510),(470,270),(680,470),(890,180),(1140,400)],(90,220,255))]:
        cl = layer(); ImageDraw.Draw(cl).line(pts, fill=(*col,175), width=6); base = comp(base, cl)
    for cx,cy,r,c in [(280,260,75,(255,210,80)),(680,370,95,(90,220,255)),(980,210,65,(210,95,195)),(180,460,50,(100,255,180))]:
        el = layer(); ImageDraw.Draw(el).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(*c,155), outline=(255,255,255,95), width=3); base = comp(base, el)
    return base


def img_rothko_20260221():
    """Mark Rothko colour field — Responsible Disclosure / depth and weight."""
    base = Image.new("RGB", (W, H), (30, 10, 10))
    bands = [
        (0,   0,   W, 160, (60, 10, 10)),
        (0, 140,   W, 340, (140, 30, 20)),
        (0, 310,   W, 490, (80, 20, 60)),
        (0, 460,   W, H,   (20, 10, 40)),
    ]
    for x0,y0,x1,y1,col in bands:
        for edge in range(20):
            fade = max(0, 255 - edge * 12)
            bl = layer(); ImageDraw.Draw(bl).rectangle([(x0, y0+edge),(x1, y0+edge+1)], fill=(*col, fade)); base = comp(base, bl)
        solid = layer(); ImageDraw.Draw(solid).rectangle([(x0,y0+20),(x1,y1-20)], fill=(*col,220)); base = comp(base, solid)
    lum_layer = layer(); ld = ImageDraw.Draw(lum_layer)
    for i in range(30):
        alpha = int(20 - i * 0.5)
        if alpha > 0:
            ld.rectangle([(80+i,150+i),(W-80-i,340-i)], fill=(200,80,40,alpha))
    base = comp(base, lum_layer)
    return base


def img_seurat_20260222():
    """Georges Seurat pointillism — Code Security / data density."""
    base = Image.new("RGB", (W, H), (10, 20, 45))
    dl = layer(); dd = ImageDraw.Draw(dl)
    for _ in range(5000):
        dx = rng.randint(0, W); dy = rng.randint(0, H)
        cx2, cy2 = W*0.6, H*0.4
        dist = math.hypot(dx-cx2, dy-cy2)
        bright = max(0, 1 - dist/480)
        rb = int(15+bright*240); gb = int(30+bright*200); bb = int(80+bright*175)
        dr2 = rng.randint(1,5)
        dd.ellipse([(dx-dr2,dy-dr2),(dx+dr2,dy+dr2)], fill=(min(255,rb+rng.randint(-20,20)), min(255,gb), min(255,bb), rng.randint(150,230)))
    base = comp(base, dl)
    rl = layer(); rd2 = ImageDraw.Draw(rl)
    for radius in [60,130,210,310,430]:
        rd2.arc([(W//2+100-radius,H//2-radius),(W//2+100+radius,H//2+radius)], 0,360, fill=(255,220,80,50), width=2)
    base = comp(base, rl)
    return base


def img_malevich_20260223():
    """Kazimir Malevich — IP Defence / security and absolutes."""
    base = Image.new("RGB", (W, H), (230, 224, 206))
    draw = ImageDraw.Draw(base)
    shapes2 = [
        ((100,60,500,280),(18,18,18),0),
        ((580,100,1080,380),(205,25,25),10),
        ((60,360,380,580),(25,45,170),-8),
        ((820,380,1140,580),(215,175,15),5),
        ((240,180,520,400),(80,80,80),18),
    ]
    for (x0,y0,x1,y1),col,angle in shapes2:
        sl = layer(); sd2 = ImageDraw.Draw(sl)
        cx2, cy2 = (x0+x1)//2,(y0+y1)//2; hw=(x1-x0)//2; hh=(y1-y0)//2
        rad2 = math.radians(angle)
        pts2 = [(int(cx2+p[0]*math.cos(rad2)-p[1]*math.sin(rad2)),int(cy2+p[0]*math.sin(rad2)+p[1]*math.cos(rad2))) for p in [(-hw,-hh),(hw,-hh),(hw,hh),(-hw,hh)]]
        sd2.polygon(pts2, fill=(*col,235))
        base = comp(base, sl)
    return base


def img_delaunay_20260224():
    """Robert Delaunay spectral rings — RSP v3.0 / signals and governance."""
    base = Image.new("RGB", (W, H), (6, 6, 12))
    spectral2 = [(220,20,60),(255,80,0),(255,200,0),(40,220,40),(0,180,255),(80,0,255),(160,0,200)]
    for i,col in enumerate(spectral2):
        r2 = 70+i*55
        cx3 = W//4
        rl2 = layer(); ImageDraw.Draw(rl2).arc([(cx3-r2,H//2-r2),(cx3+r2,H//2+r2)],0,360,fill=(*col,120),width=20); base=comp(base,rl2)
    for i,col in enumerate(spectral2):
        r3 = 55+i*45
        cx4 = 3*W//4
        rl3 = layer(); ImageDraw.Draw(rl3).arc([(cx4-r3,H//2-r3),(cx4+r3,H//2+r3)],0,360,fill=(*col,90),width=16); base=comp(base,rl3)
    ml = layer(); ImageDraw.Draw(ml).ellipse([(W//2-60,H//2-60),(W//2+60,H//2+60)],fill=(255,255,255,35)); base=comp(base,ml)
    gl = layer(); gd2 = ImageDraw.Draw(gl)
    gd2.line([(0,H//2),(W,H//2)], fill=(255,255,255,30), width=2)
    base=comp(base,gl)
    return base


def img_balla_20260225():
    """Giacomo Balla Futurism — Series G valuation / momentum and speed."""
    base = Image.new("RGB", (W, H), (6, 6, 10))
    vp2_x, vp2_y = 580, 310
    for i in range(28):
        angle2 = math.radians(i * (360/28))
        length2 = rng.randint(280, 650)
        ex2 = int(vp2_x + length2 * math.cos(angle2))
        ey2 = int(vp2_y + length2 * math.sin(angle2))
        cols3 = [(210,55,15),(250,135,0),(195,195,0),(55,195,215),(95,55,195),(215,15,95),(0,195,95)]
        col3 = cols3[i % len(cols3)]
        pl3 = layer(); ImageDraw.Draw(pl3).line([(vp2_x,vp2_y),(ex2,ey2)], fill=(*col3,135), width=rng.randint(2,9)); base=comp(base,pl3)
    for i in range(14):
        angle3 = math.radians(i * (360/14) + 13)
        length3 = rng.randint(180, 480)
        end_x3 = int(vp2_x + length3 * math.cos(angle3))
        end_y3 = int(vp2_y + length3 * math.sin(angle3))
        pw2 = rng.randint(18, 75); ph2 = rng.randint(9, 38)
        cols4 = [(210,55,15),(250,135,0),(55,195,215),(195,195,0)]
        col4 = cols4[i % len(cols4)]
        sx2 = (vp2_x+end_x3)//2; sy2 = (vp2_y+end_y3)//2
        pl4 = layer(); ImageDraw.Draw(pl4).ellipse([(sx2-pw2//2,sy2-ph2//2),(sx2+pw2//2,sy2+ph2//2)],fill=(*col4,175)); base=comp(base,pl4)
    core2 = layer(); ImageDraw.Draw(core2).ellipse([(vp2_x-28,vp2_y-28),(vp2_x+28,vp2_y+28)],fill=(255,255,255,235)); base=comp(base,core2)
    return base


def img_moholy_20260226():
    """László Moholy-Nagy Bauhaus — Open Letter / transparency and openness."""
    base = Image.new("RGB", (W, H), (252, 248, 243))
    circles2 = [(280,300,250,(215,75,25)),(720,300,210,(25,75,195)),(1020,190,165,(215,175,15)),(490,455,145,(35,155,95)),(900,430,120,(160,20,175))]
    for cx5,cy5,r5,col5 in circles2:
        for opacity2 in [38,78,145]:
            cl5 = layer(); ImageDraw.Draw(cl5).ellipse([(cx5-r5,cy5-r5),(cx5+r5,cy5+r5)],fill=(*col5,opacity2),outline=(*col5,215),width=4); base=comp(base,cl5)
    for x0b,y0b,x1b,y1b,col6 in [(45,90,290,345,(25,75,195)),(810,195,1115,495,(215,75,25))]:
        rl4 = layer(); ImageDraw.Draw(rl4).rectangle([(x0b,y0b),(x1b,y1b)],fill=(*col6,55),outline=(*col6,195),width=5); base=comp(base,rl4)
    ll2 = layer(); ld2 = ImageDraw.Draw(ll2)
    ld2.line([(0,300),(W,300)],fill=(0,0,0,175),width=3); ld2.line([(600,0),(600,H)],fill=(0,0,0,175),width=3)
    base=comp(base,ll2)
    return base


def img_kandinsky_20260227():
    """Wassily Kandinsky — Federal Access / structured composition."""
    base = Image.new("RGB", (W, H), (18, 32, 70))
    gl2 = layer(); gd3 = ImageDraw.Draw(gl2)
    for off2 in range(-H, W+H, 48):
        gd3.line([(off2,0),(off2+H,H)],fill=(255,255,255,12),width=1)
        gd3.line([(off2,0),(off2-H,H)],fill=(255,255,255,12),width=1)
    base=comp(base,gl2)
    e2 = layer(); ImageDraw.Draw(e2).ellipse([(780,10),(1160,390)],fill=(255,205,0,215),outline=(0,0,0,255),width=6); base=comp(base,e2)
    t2 = layer(); ImageDraw.Draw(t2).polygon([(60,550),(360,550),(210,170)],fill=(220,30,50,215)); base=comp(base,t2)
    p2 = layer(); ImageDraw.Draw(p2).pieslice([(860,360),(1180,590)],175,340,fill=(30,95,215,185)); base=comp(base,p2)
    s2 = layer(); sd3 = ImageDraw.Draw(s2)
    for px3,py3,c3,r6 in [(100,90,(255,115,15,195),32),(380,50,(135,45,195,185),25),(530,290,(35,195,75,195),20),(690,480,(215,25,45,195),27)]:
        sd3.ellipse([(px3-r6,py3-r6),(px3+r6,py3+r6)],fill=c3,outline=(0,0,0,255),width=2)
    base=comp(base,s2)
    l2 = layer(); ld3 = ImageDraw.Draw(l2)
    ld3.line([(0,380),(430,80)],fill=(0,0,0,255),width=4); ld3.line([(480,580),(930,190)],fill=(255,255,255,195),width=3)
    base=comp(base,l2)
    return base


def img_miro_20260228():
    """Joan Miró biomorphic — Market Share / cycles and consumer momentum."""
    base = Image.new("RGB", (W, H), (20, 18, 60))
    blobs = [(250,200,100,80,(220,50,50)),(650,300,130,90,(255,200,0)),(1000,180,90,70,(50,180,220)),(150,450,80,60,(50,200,80)),(800,450,110,80,(220,100,200)),(500,130,70,55,(255,140,0))]
    for cx7,cy7,rw,rh,col7 in blobs:
        bl2 = layer(); ImageDraw.Draw(bl2).ellipse([(cx7-rw,cy7-rh),(cx7+rw,cy7+rh)],fill=(*col7,230),outline=(0,0,0,255),width=5); base=comp(base,bl2)
    stars = [(350,100),(750,200),(1050,350),(200,320),(900,120),(600,480)]
    for sx3,sy3 in stars:
        stl = layer(); std = ImageDraw.Draw(stl)
        for angle4 in range(0,360,60):
            rad4 = math.radians(angle4)
            std.ellipse([(sx3+int(22*math.cos(rad4))-5,sy3+int(22*math.sin(rad4))-5),(sx3+int(22*math.cos(rad4))+5,sy3+int(22*math.sin(rad4))+5)],fill=(255,255,255,220))
        base=comp(base,stl)
    ll3 = layer(); ld4 = ImageDraw.Draw(ll3)
    ld4.line([(100,350),(400,150),(700,400),(1000,200),(1150,450)],fill=(0,0,0,255),width=4)
    base=comp(base,ll3)
    return base


# ── January 2026 retrospective motif functions ───────────────────────────────

def img_rothko_20260101():
    """Mark Rothko Colour Field — year in review, long contemplation."""
    base = Image.new("RGB", (W, H), (18, 10, 8))
    bands = [(30, 14, 6), (110, 35, 20), (180, 70, 30), (220, 120, 50), (160, 55, 25)]
    band_h = H // len(bands)
    for i, col in enumerate(bands):
        bl = layer(); ImageDraw.Draw(bl).rectangle([(0, i*band_h), (W, (i+1)*band_h+20)], fill=(*col, 200))
        base = comp(base, bl)
    glow = layer()
    for r in [200, 150, 100]:
        gl = layer(); ImageDraw.Draw(gl).ellipse([(W//2-r*3, H//2-r), (W//2+r*3, H//2+r)], fill=(220, 120, 50, 30)); base = comp(base, gl)
    edge = layer(); ed = ImageDraw.Draw(edge)
    for y in range(0, H, 4):
        alpha = int(30 * abs(math.sin(y / 40)))
        ed.line([(0, y), (W, y)], fill=(255, 200, 120, alpha), width=1)
    base = comp(base, edge)
    return base


def img_mondrian_20260102():
    """Piet Mondrian grid — SDK structured outputs."""
    base = Image.new("RGB", (W, H), (242, 238, 220))
    draw = ImageDraw.Draw(base)
    YELLOW, RED, BLUE, BLACK = (255, 210, 0), (215, 35, 35), (25, 75, 195), (15, 15, 15)
    gx = [0, 100, 220, 350, 480, 610, 730, 860, 980, 1100, W]
    gy = [0, 90, 180, 270, 360, 450, 540, H]
    bw = 14
    for x in gx[1:-1]: draw.rectangle([(x-bw//2,0),(x+bw//2,H)], fill=YELLOW)
    for y in gy[1:-1]: draw.rectangle([(0,y-bw//2),(W,y+bw//2)], fill=YELLOW)
    cells = [(0,0,RED),(2,2,BLUE),(4,1,RED),(6,3,BLUE),(1,4,RED),(5,0,BLUE),(3,5,RED),(7,2,BLUE),(1,1,YELLOW),(5,4,YELLOW)]
    for ci, cj, col in cells:
        x0 = gx[ci]+bw//2+2; y0 = gy[cj]+bw//2+2
        x1 = gx[ci+1]-bw//2-2; y1 = gy[cj+1]-bw//2-2
        if x1>x0 and y1>y0: draw.rectangle([(x0,y0),(x1,y1)], fill=col)
    for x in gx[1:-1]:
        for y in gy[1:-1]: draw.rectangle([(x-bw//2,y-bw//2),(x+bw//2,y+bw//2)], fill=BLACK)
    return base


def img_klimt_20260103():
    """Gustav Klimt mosaic — Haiku 4.5 launch, craftsmanship."""
    base = Image.new("RGB", (W, H), (12, 8, 6))
    spiral = layer(); sd = ImageDraw.Draw(spiral)
    for i in range(60):
        a = math.radians(i * 22)
        r2 = 20 + i * 8
        cx2 = int(600 + r2 * math.cos(a)); cy2 = int(315 + r2 * math.sin(a))
        sd.arc([(cx2-r2//2,cy2-r2//2),(cx2+r2//2,cy2+r2//2)], a*10, a*10+180, fill=(212,175,55,rng.randint(80,200)), width=rng.randint(1,4))
    base = comp(base, spiral)
    mosaic = layer(); md = ImageDraw.Draw(mosaic)
    for _ in range(300):
        mx = rng.randint(0,W-16); my = rng.randint(0,H-16); sz = rng.randint(4,16)
        mc = [(212,175,55),(0,120,120),(150,55,25),(190,170,70),(75,35,110)][rng.randint(0,4)]
        md.rectangle([(mx,my),(mx+sz,my+sz)], fill=(*mc, rng.randint(110,210)))
    base = comp(base, mosaic)
    face = layer(); fd = ImageDraw.Draw(face)
    fd.ellipse([(420,60),(780,450)], fill=(212,175,55,50), outline=(212,175,55,170), width=5)
    base = comp(base, face)
    glow2 = layer(); gd2 = ImageDraw.Draw(glow2)
    for _ in range(80):
        cx3=rng.randint(0,W); cy3=rng.randint(0,H); r3=rng.randint(6,50)
        gd2.arc([(cx3-r3,cy3-r3),(cx3+r3,cy3+r3)], rng.randint(0,360), rng.randint(10,340), fill=(212,175,55,rng.randint(60,180)), width=rng.randint(1,4))
    base = comp(base, glow2)
    return base


def img_miro_20260104():
    """Joan Miró biomorphic — team collaboration / Projects."""
    base = Image.new("RGB", (W, H), (18, 16, 55))
    blobs = [(220,180,90,70,(215,45,45)),(560,280,120,85,(255,195,0)),(950,170,85,65,(45,175,215)),(130,410,75,55,(45,195,75)),(750,420,105,75,(215,95,195)),(460,120,65,50,(255,135,0)),(1080,340,70,55,(255,90,90))]
    for cx,cy,rw,rh,col in blobs:
        bl = layer(); ImageDraw.Draw(bl).ellipse([(cx-rw,cy-rh),(cx+rw,cy+rh)], fill=(*col,225), outline=(0,0,0,255), width=4)
        base = comp(base, bl)
    for sx,sy in [(300,90),(720,190),(1000,340),(185,310),(870,115),(580,470),(420,350)]:
        stl = layer(); std = ImageDraw.Draw(stl)
        for ang in range(0,360,60):
            rad = math.radians(ang); std.ellipse([(sx+int(20*math.cos(rad))-4,sy+int(20*math.sin(rad))-4),(sx+int(20*math.cos(rad))+4,sy+int(20*math.sin(rad))+4)], fill=(255,255,255,215))
        base = comp(base, stl)
    ll = layer(); ld = ImageDraw.Draw(ll)
    ld.line([(80,340),(380,140),(680,390),(980,190),(1130,440)], fill=(0,0,0,255), width=4)
    base = comp(base, ll)
    return base


def img_delaunay_20260105():
    """Robert Delaunay rings — voice / webhooks / signals."""
    base = Image.new("RGB", (W, H), (12, 10, 28))
    centres = [(350, 300), (750, 280), (1050, 320), (180, 200)]
    spectrum = [(220,30,50),(255,120,0),(255,215,0),(40,200,80),(0,160,255),(120,40,220)]
    for cx, cy in centres:
        for i, col in enumerate(spectrum):
            r4 = 60 + i * 55
            rl = layer(); ImageDraw.Draw(rl).ellipse([(cx-r4,cy-r4),(cx+r4,cy+r4)], fill=(*col, 40), outline=(*col, 160), width=3)
            base = comp(base, rl)
    cross = layer(); cd = ImageDraw.Draw(cross)
    for cx,cy in centres:
        cd.line([(cx-90,cy),(cx+90,cy)], fill=(255,255,255,60), width=1)
        cd.line([(cx,cy-90),(cx,cy+90)], fill=(255,255,255,60), width=1)
    base = comp(base, cross)
    return base


def img_malevich_20260106():
    """Kazimir Malevich geometric — responsible use / security."""
    base = Image.new("RGB", (W, H), (235, 228, 210))
    shapes = [
        ([(150,100),(450,100),(480,350),(120,350)], (20,20,20)),
        ([(700,80),(950,80),(980,280),(670,280)], (200,30,30)),
        ([(550,350),(800,350),(820,530),(530,530)], (20,60,180)),
        ([(900,380),(1150,380),(1170,550),(880,550)], (220,190,0)),
        ([(100,420),(300,420),(320,580),(80,580)], (20,20,20)),
    ]
    for pts, col in shapes:
        sl = layer(); ImageDraw.Draw(sl).polygon(pts, fill=(*col,220), outline=(0,0,0,255)); base = comp(base, sl)
    return base


def img_seurat_20260107():
    """Georges Seurat pointillism — token analytics / developer data."""
    base = Image.new("RGB", (W, H), (16, 22, 52))
    dot_layer = layer(); dd = ImageDraw.Draw(dot_layer)
    for _ in range(5000):
        dx = rng.randint(0,W); dy = rng.randint(0,H)
        cx5,cy5 = W*0.5, H*0.5
        dist = math.hypot(dx-cx5, dy-cy5)
        bright = max(0, 1-dist/480)
        r5 = int(15+bright*240); g5 = int(30+bright*190); b5 = int(90+bright*165)
        hs = rng.randint(-25,25); dr5 = rng.randint(2,5)
        dd.ellipse([(dx-dr5,dy-dr5),(dx+dr5,dy+dr5)], fill=(min(255,r5+hs),min(255,g5),min(255,b5),rng.randint(150,235)))
    base = comp(base, dot_layer)
    rings = layer(); rd5 = ImageDraw.Draw(rings)
    for rad5 in [70,150,230,320,420]:
        rd5.arc([(W//2-rad5,H//2-rad5),(W//2+rad5,H//2+rad5)], 0, 360, fill=(255,210,90,50), width=2)
    base = comp(base, rings)
    return base


def img_calder_20260108():
    """Alexander Calder mobile — Azure / balanced infrastructure."""
    base = Image.new("RGB", (W, H), (246,243,238))
    arms = layer(); ad = ImageDraw.Draw(arms)
    ad.line([(180,70),(1020,70)], fill=(18,18,18,255), width=4)
    ad.line([(600,70),(600,210)], fill=(18,18,18,255), width=3)
    ad.line([(180,70),(180,190)], fill=(18,18,18,255), width=3)
    ad.line([(1020,70),(1020,190)], fill=(18,18,18,255), width=3)
    ad.line([(290,290),(810,290)], fill=(18,18,18,255), width=3)
    ad.line([(290,290),(290,430)], fill=(18,18,18,255), width=2)
    ad.line([(810,290),(810,430)], fill=(18,18,18,255), width=2)
    ad.line([(180,190),(480,190)], fill=(18,18,18,255), width=2)
    ad.line([(330,190),(330,360)], fill=(18,18,18,255), width=2)
    base = comp(base, arms)
    ellipses = [
        ((120,150,260,260),(215,40,40)),((560,50,720,210),(18,75,195)),((960,150,1080,280),(215,195,0)),
        ((240,390,380,520),(215,95,18)),((740,385,880,520),(38,155,75)),((290,310,410,420),(155,18,175)),
        ((155,190,275,300),(0,155,195)),
    ]
    for bounds,col in ellipses:
        el = layer(); ImageDraw.Draw(el).ellipse(bounds, fill=(*col,225)); base = comp(base, el)
    return base


def img_lissitzky_20260109():
    """El Lissitzky constructivist — Claude Code CLI / developer tooling."""
    base = Image.new("RGB", (W, H), (238, 232, 215))
    bars = [
        ((60,40,280,130), (185,20,20)),
        ((340,80,700,180), (20,20,20)),
        ((80,200,500,280), (185,20,20)),
        ((560,160,900,240), (20,20,20)),
        ((200,320,600,400), (185,20,20)),
        ((650,300,1100,380), (20,20,20)),
        ((100,440,420,510), (185,20,20)),
        ((480,420,850,500), (20,20,20)),
    ]
    for (x0,y0,x1,y1), col in bars:
        sl = layer(); ImageDraw.Draw(sl).rectangle([(x0,y0),(x1,y1)], fill=(*col,210)); base = comp(base, sl)
    circles = [(320,220,40,(185,20,20)),(800,120,55,(20,20,20)),(550,460,35,(185,20,20))]
    for cx,cy,r,col in circles:
        cl = layer(); ImageDraw.Draw(cl).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(*col,180), outline=(0,0,0,255), width=3); base = comp(base, cl)
    return base


def img_franz_marc_20260110():
    """Franz Marc jewel tones — model welfare / interpretability."""
    base = Image.new("RGB", (W, H), (8, 35, 75))
    panels = [((0,0,380,H),(0,115,155,115)),((350,0,730,H),(18,75,35,115)),((700,0,W,H),(95,18,115,115))]
    for r,c in [(b,col) for b,col in panels]:
        pl = layer(); ImageDraw.Draw(pl).rectangle(r, fill=c); base = comp(base, pl)
    for pts,col in [([(90,380),(280,190),(480,340),(680,140),(880,290),(1100,90)],(250,195,75)),
                    ([(40,280),(240,490),(440,265),(640,465),(840,185),(1100,380)],(90,215,255))]:
        ll = layer(); ImageDraw.Draw(ll).line(pts, fill=(*col,175), width=6); base = comp(base, ll)
    for cx,cy,r,col in [(290,240,75,(250,195,75)),(680,360,95,(90,215,255)),(980,185,65,(215,95,195))]:
        el = layer(); ImageDraw.Draw(el).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(*col,155), outline=(255,255,255,95), width=3); base = comp(base, el)
    return base


def img_balla_20260111():
    """Giacomo Balla Futurism — Cowork macOS launch / speed."""
    base = Image.new("RGB", (W, H), (7, 7, 11))
    vx, vy = 580, 310
    cols6 = [(215,55,18),(255,135,0),(195,195,0),(55,195,215),(95,55,195),(215,18,95)]
    for i in range(24):
        ang = math.radians(i*15); L = rng.randint(280,680)
        ex = int(vx+L*math.cos(ang)); ey = int(vy+L*math.sin(ang))
        pl = layer(); ImageDraw.Draw(pl).line([(vx,vy),(ex,ey)], fill=(*cols6[i%6],135), width=rng.randint(2,8)); base = comp(base, pl)
    for i in range(12):
        ang = math.radians(i*30+8); L2 = rng.randint(180,480)
        ex2 = int(vx+L2*math.cos(ang)); ey2 = int(vy+L2*math.sin(ang))
        pw = rng.randint(18,75); ph = rng.randint(9,38)
        sx5 = (vx+ex2)//2; sy5 = (vy+ey2)//2
        pl2 = layer(); ImageDraw.Draw(pl2).ellipse([(sx5-pw,sy5-ph),(sx5+pw,sy5+ph)], fill=(*cols6[i%4],95)); base = comp(base, pl2)
    core = layer(); ImageDraw.Draw(core).ellipse([(vx-18,vy-18),(vx+18,vy+18)], fill=(255,255,255,235)); base = comp(base, core)
    return base


def img_moholy_20260112():
    """László Moholy-Nagy Bauhaus — open source evals / transparency."""
    base = Image.new("RGB", (W, H), (250, 247, 242))
    circles_data = [(350,300,200,(255,80,20)),(700,280,180,(20,100,220)),(550,320,160,(220,200,0)),(900,250,140,(20,180,100)),(200,200,120,(180,20,180))]
    for cx,cy,r,col in circles_data:
        cl = layer(); ImageDraw.Draw(cl).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(*col,55), outline=(*col,180), width=4); base = comp(base, cl)
    rects = [(100,50,320,180,(20,100,220)),(750,100,970,250,(255,80,20)),(400,400,650,570,(20,180,100)),(900,380,1150,540,(220,200,0))]
    for x0,y0,x1,y1,col in rects:
        rl = layer(); ImageDraw.Draw(rl).rectangle([(x0,y0),(x1,y1)], fill=(*col,40), outline=(*col,160), width=3); base = comp(base, rl)
    ll = layer(); ld = ImageDraw.Draw(ll)
    ld.line([(0,H//2),(W,H//2)], fill=(20,20,20,100), width=2)
    ld.line([(W//2,0),(W//2,H)], fill=(20,20,20,100), width=2)
    base = comp(base, ll)
    return base


def img_kandinsky_20260113():
    """Wassily Kandinsky — extended thinking GA / prompting guide."""
    base = Image.new("RGB", (W, H), (16, 32, 68))
    grid = layer(); gd = ImageDraw.Draw(grid)
    for off in range(-H,W+H,58):
        gd.line([(off,0),(off+H,H)], fill=(255,255,255,22), width=1)
        gd.line([(off,0),(off-H,H)], fill=(255,255,255,22), width=1)
    base = comp(base, grid)
    s1 = layer(); ImageDraw.Draw(s1).ellipse([(610,10),(1080,380)], fill=(255,210,0,225)); base = comp(base, s1)
    s2 = layer(); ImageDraw.Draw(s2).polygon([(190,510),(460,510),(325,170)], fill=(215,28,48,215)); base = comp(base, s2)
    s3 = layer(); ImageDraw.Draw(s3).pieslice([(820,270),(1175,570)], 195, 355, fill=(28,88,215,195)); base = comp(base, s3)
    s4 = layer(); ImageDraw.Draw(s4).ellipse([(95,75),(255,235)], fill=(255,115,18,215)); base = comp(base, s4)
    s5 = layer(); ImageDraw.Draw(s5).polygon([(530,340),(625,245),(720,340),(625,435)], fill=(38,175,88,195)); base = comp(base, s5)
    ll = layer(); ld = ImageDraw.Draw(ll)
    ld.line([(0,395),(395,95)], fill=(0,0,0,255), width=4)
    ld.line([(495,595),(895,195)], fill=(255,255,255,195), width=3)
    base = comp(base, ll)
    return base


def img_leger_20260114():
    """Fernand Léger mechanical — Bedrock cross-region / infrastructure."""
    base = Image.new("RGB", (W, H), (20, 20, 25))
    outlines = [
        ((80,60,280,220), (220,50,50)),
        ((320,100,600,280), (255,160,0)),
        ((650,60,850,200), (50,180,220)),
        ((900,120,1150,300), (220,220,50)),
        ((100,320,380,520), (255,160,0)),
        ((420,360,700,560), (50,220,100)),
        ((750,340,1000,530), (220,50,50)),
    ]
    for (x0,y0,x1,y1), col in outlines:
        sl = layer(); ImageDraw.Draw(sl).rectangle([(x0,y0),(x1,y1)], fill=(*col,35), outline=(*col,220), width=5); base = comp(base, sl)
    circles2 = [(180,320,50,(255,160,0)),(550,190,60,(220,50,50)),(870,220,45,(50,220,100)),(1050,440,55,(50,180,220))]
    for cx,cy,r,col in circles2:
        cl = layer(); ImageDraw.Draw(cl).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(*col,55), outline=(*col,220), width=5); base = comp(base, cl)
    return base


def img_rothko_20260115():
    """Mark Rothko Colour Field — long context faithfulness / depth."""
    base = Image.new("RGB", (W, H), (10, 6, 14))
    bands2 = [(40,18,55), (90,40,120), (140,70,170), (80,30,110), (30,10,45)]
    bh2 = H//len(bands2)
    for i,col in enumerate(bands2):
        bl2 = layer(); ImageDraw.Draw(bl2).rectangle([(0,i*bh2),(W,(i+1)*bh2+18)], fill=(*col,205)); base = comp(base, bl2)
    for r6 in [180,130,80]:
        gl2 = layer(); ImageDraw.Draw(gl2).ellipse([(W//2-r6*3,H//2-r6),(W//2+r6*3,H//2+r6)], fill=(170,100,220,28)); base = comp(base, gl2)
    edge2 = layer(); ed2 = ImageDraw.Draw(edge2)
    for y2 in range(0,H,4):
        a2 = int(25*abs(math.sin(y2/38))); ed2.line([(0,y2),(W,y2)], fill=(200,150,255,a2), width=1)
    base = comp(base, edge2)
    return base


def img_klimt_20260116():
    """Gustav Klimt gold mosaic — Sonnet 4.5 update / refinement."""
    base = Image.new("RGB", (W, H), (10, 6, 4))
    spiral2 = layer(); sd2 = ImageDraw.Draw(spiral2)
    for i in range(55):
        a7 = math.radians(i*24); r7 = 18+i*9
        cx7 = int(550+r7*math.cos(a7)); cy7 = int(280+r7*math.sin(a7))
        sd2.arc([(cx7-r7//2,cy7-r7//2),(cx7+r7//2,cy7+r7//2)], a7*8, a7*8+200, fill=(200,165,45,rng.randint(75,195)), width=rng.randint(1,4))
    base = comp(base, spiral2)
    mos2 = layer(); md2 = ImageDraw.Draw(mos2)
    for _ in range(280):
        mx2=rng.randint(0,W-14); my2=rng.randint(0,H-14); sz2=rng.randint(4,15)
        mc2 = [(200,165,45),(0,110,110),(145,50,22),(185,165,65),(70,32,105)][rng.randint(0,4)]
        md2.rectangle([(mx2,my2),(mx2+sz2,my2+sz2)], fill=(*mc2,rng.randint(105,205)))
    base = comp(base, mos2)
    face2 = layer(); fd2 = ImageDraw.Draw(face2)
    fd2.ellipse([(900,60),(1160,400)], fill=(200,165,45,45), outline=(200,165,45,165), width=5)
    base = comp(base, face2)
    return base


def img_mondrian_20260117():
    """Piet Mondrian grid — structured outputs / JSON schema."""
    base = Image.new("RGB", (W, H), (240, 235, 218))
    draw17 = ImageDraw.Draw(base)
    Y2,R2,B2,BK2 = (255,205,0),(210,30,30),(20,70,190),(12,12,12)
    gx2 = [0,90,210,340,470,610,740,870,1000,1110,W]
    gy2 = [0,85,175,265,355,445,535,H]
    bw2 = 15
    for x in gx2[1:-1]: draw17.rectangle([(x-bw2//2,0),(x+bw2//2,H)], fill=Y2)
    for y in gy2[1:-1]: draw17.rectangle([(0,y-bw2//2),(W,y+bw2//2)], fill=Y2)
    cells2 = [(1,0,R2),(3,2,B2),(5,1,R2),(7,3,B2),(0,4,R2),(4,5,B2),(8,2,R2),(2,4,B2),(6,0,Y2)]
    for ci2,cj2,col17 in cells2:
        x02=gx2[ci2]+bw2//2+2; y02=gy2[cj2]+bw2//2+2; x12=gx2[ci2+1]-bw2//2-2; y12=gy2[cj2+1]-bw2//2-2
        if x12>x02 and y12>y02: draw17.rectangle([(x02,y02),(x12,y12)], fill=col17)
    for x in gx2[1:-1]:
        for y in gy2[1:-1]: draw17.rectangle([(x-bw2//2,y-bw2//2),(x+bw2//2,y+bw2//2)], fill=BK2)
    return base


def img_miro_20260118():
    """Joan Miró — chained automations / computer use multi-screen."""
    base = Image.new("RGB", (W, H), (16, 14, 52))
    blobs18 = [(200,190,85,68,(210,42,42)),(540,270,118,82,(255,190,0)),(920,165,82,62,(42,170,210)),(120,405,72,52,(42,190,72)),(720,415,102,72,(210,92,192)),(440,115,62,48,(255,130,0)),(1060,330,68,52,(255,85,85)),(330,450,58,44,(0,205,205))]
    for cx,cy,rw,rh,col in blobs18:
        bl = layer(); ImageDraw.Draw(bl).ellipse([(cx-rw,cy-rh),(cx+rw,cy+rh)], fill=(*col,222), outline=(0,0,0,255), width=4); base = comp(base, bl)
    for sx,sy in [(280,85),(700,185),(980,330),(175,305),(850,108),(560,465),(410,345),(900,430)]:
        stl = layer(); std = ImageDraw.Draw(stl)
        for ang in range(0,360,60):
            rad=math.radians(ang); std.ellipse([(sx+int(18*math.cos(rad))-4,sy+int(18*math.sin(rad))-4),(sx+int(18*math.cos(rad))+4,sy+int(18*math.sin(rad))+4)], fill=(255,255,255,212))
        base = comp(base, stl)
    ll18 = layer(); ld18 = ImageDraw.Draw(ll18)
    ld18.line([(75,325),(375,135),(675,380),(975,180),(1125,435)], fill=(0,0,0,255), width=4)
    base = comp(base, ll18)
    return base


def img_seurat_20260119():
    """Georges Seurat — 1M developers / data density."""
    base = Image.new("RGB", (W, H), (12, 18, 48))
    dl19 = layer(); dd19 = ImageDraw.Draw(dl19)
    for _ in range(5500):
        dx=rng.randint(0,W); dy=rng.randint(0,H)
        cx19,cy19 = W*0.45, H*0.5; dist19=math.hypot(dx-cx19,dy-cy19)
        bright19=max(0,1-dist19/460)
        r19=int(18+bright19*237); g19=int(35+bright19*195); b19=int(85+bright19*170)
        hs19=rng.randint(-28,28); dr19=rng.randint(2,5)
        dd19.ellipse([(dx-dr19,dy-dr19),(dx+dr19,dy+dr19)], fill=(min(255,r19+hs19),min(255,g19),min(255,b19),rng.randint(145,232)))
    base = comp(base, dl19)
    rl19 = layer(); rd19 = ImageDraw.Draw(rl19)
    for rad19 in [65,140,220,310,410]:
        rd19.arc([(W//2-rad19-80,H//2-rad19),(W//2+rad19-80,H//2+rad19)], 0, 360, fill=(255,205,85,48), width=2)
    base = comp(base, rl19)
    return base


def img_malevich_20260120():
    """Kazimir Malevich — prompt injection eval / safety."""
    base = Image.new("RGB", (W, H), (232, 225, 208))
    shapes20 = [
        ([(130,90),(430,90),(460,340),(100,340)], (18,18,18)),
        ([(680,70),(930,70),(960,270),(650,270)], (195,28,28)),
        ([(540,340),(790,340),(810,520),(520,520)], (18,58,178)),
        ([(890,370),(1140,370),(1160,540),(870,540)], (215,185,0)),
        ([(90,410),(290,410),(310,570),(70,570)], (195,28,28)),
    ]
    for pts,col in shapes20:
        sl = layer(); ImageDraw.Draw(sl).polygon(pts, fill=(*col,215), outline=(0,0,0,255)); base = comp(base, sl)
    return base


def img_delaunay_20260121():
    """Robert Delaunay rings — MCP 500 servers / signals."""
    base = Image.new("RGB", (W, H), (10, 8, 26))
    centres21 = [(320,295),(720,275),(1030,315),(165,195),(880,420)]
    spec21 = [(215,28,48),(255,115,0),(255,210,0),(38,195,78),(0,155,250),(115,38,215)]
    for cx,cy in centres21:
        for i,col in enumerate(spec21):
            r21=55+i*50; rl=layer(); ImageDraw.Draw(rl).ellipse([(cx-r21,cy-r21),(cx+r21,cy+r21)], fill=(*col,38), outline=(*col,155), width=3); base=comp(base,rl)
    return base


def img_balla_20260122():
    """Giacomo Balla Futurism — streaming TTFT / speed."""
    base = Image.new("RGB", (W, H), (6, 6, 10))
    vx2,vy2 = 620,305
    cols22 = [(210,52,16),(250,130,0),(190,190,0),(52,190,210),(92,52,190),(210,16,92)]
    for i in range(26):
        ang2=math.radians(i*13.8); L22=rng.randint(260,720)
        ex22=int(vx2+L22*math.cos(ang2)); ey22=int(vy2+L22*math.sin(ang2))
        pl22=layer(); ImageDraw.Draw(pl22).line([(vx2,vy2),(ex22,ey22)], fill=(*cols22[i%6],128), width=rng.randint(2,9)); base=comp(base,pl22)
    for i in range(14):
        ang3=math.radians(i*25.7+5); L23=rng.randint(160,460)
        ex23=int(vx2+L23*math.cos(ang3)); ey23=int(vy2+L23*math.sin(ang3))
        pw2=rng.randint(16,72); ph2=rng.randint(8,36)
        sx6=(vx2+ex23)//2; sy6=(vy2+ey23)//2
        pl23=layer(); ImageDraw.Draw(pl23).ellipse([(sx6-pw2,sy6-ph2),(sx6+pw2,sy6+ph2)], fill=(*cols22[i%4],88)); base=comp(base,pl23)
    core2=layer(); ImageDraw.Draw(core2).ellipse([(vx2-16,vy2-16),(vx2+16,vy2+16)], fill=(255,255,255,228)); base=comp(base,core2)
    return base


def img_klee_20260123():
    """Paul Klee colour grid — agent teams preview / multi-agent cells."""
    base = Image.new("RGB", (W, H), (30, 25, 18))
    WARM = [(220,120,40),(215,90,30),(200,150,50),(185,75,25),(230,170,60)]
    COOL = [(40,120,185),(30,90,160),(55,155,195),(25,75,145),(60,175,215)]
    gw, gh = W//10, H//7
    for ci in range(10):
        for cj in range(7):
            palette = WARM if (ci+cj)%2==0 else COOL
            col23 = palette[(ci*3+cj*2)%5]
            x0=ci*gw; y0=cj*gh; x1=x0+gw; y1=y0+gh
            cl23=layer(); ImageDraw.Draw(cl23).rectangle([(x0,y0),(x1,y1)], fill=(*col23, 185)); base=comp(base,cl23)
    nodes=layer(); nd=ImageDraw.Draw(nodes)
    for ci in range(1,10):
        for cj in range(1,7):
            r8=8; nd.ellipse([(ci*gw-r8,cj*gh-r8),(ci*gw+r8,cj*gh+r8)], fill=(255,255,255,200), outline=(40,40,40,255), width=2)
    base=comp(base,nodes)
    dark=layer(); dd2=ImageDraw.Draw(dark)
    for ci in range(11): dd2.line([(ci*gw,0),(ci*gw,H)], fill=(20,15,10,180), width=2)
    for cj in range(8): dd2.line([(0,cj*gh),(W,cj*gh)], fill=(20,15,10,180), width=2)
    base=comp(base,dark)
    return base


def img_leger_20260124():
    """Fernand Léger — Vertex AI expansion / cloud infrastructure."""
    base = Image.new("RGB", (W, H), (18, 18, 22))
    outlines24 = [
        ((70,55,270,215), (215,45,45)),
        ((310,95,590,275), (250,155,0)),
        ((640,55,840,195), (45,175,215)),
        ((890,115,1140,295), (215,215,45)),
        ((90,315,370,515), (250,155,0)),
        ((410,355,690,555), (45,215,95)),
        ((740,335,990,525), (215,45,45)),
        ((1010,310,1170,490), (45,175,215)),
    ]
    for (x0,y0,x1,y1),col in outlines24:
        sl=layer(); ImageDraw.Draw(sl).rectangle([(x0,y0),(x1,y1)], fill=(*col,32), outline=(*col,215), width=5); base=comp(base,sl)
    for cx,cy,r,col in [(165,315,48,(250,155,0)),(540,185,58,(215,45,45)),(860,215,43,(45,215,95)),(1040,435,52,(45,175,215))]:
        cl=layer(); ImageDraw.Draw(cl).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(*col,52), outline=(*col,215), width=5); base=comp(base,cl)
    return base


def img_moholy_20260125():
    """László Moholy-Nagy — Trust Center / open transparency."""
    base = Image.new("RGB", (W, H), (248,244,240))
    for cx,cy,r,col in [(340,295,195,(255,75,18)),(690,275,175,(18,95,215)),(540,315,158,(215,195,0)),(890,245,138,(18,175,95)),(195,195,118,(175,18,175))]:
        cl=layer(); ImageDraw.Draw(cl).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(*col,52), outline=(*col,178), width=4); base=comp(base,cl)
    for x0,y0,x1,y1,col in [(95,45,315,175,(18,95,215)),(740,95,960,245,(255,75,18)),(390,395,640,565,(18,175,95)),(890,375,1140,535,(215,195,0))]:
        rl=layer(); ImageDraw.Draw(rl).rectangle([(x0,y0),(x1,y1)], fill=(*col,38), outline=(*col,155), width=3); base=comp(base,rl)
    ll25=layer(); ld25=ImageDraw.Draw(ll25)
    ld25.line([(0,H//2),(W,H//2)], fill=(18,18,18,95), width=2)
    ld25.line([(W//2,0),(W//2,H)], fill=(18,18,18,95), width=2)
    base=comp(base,ll25)
    return base


def img_lissitzky_20260126():
    """El Lissitzky — CLAUDE.md v2 / permission management."""
    base = Image.new("RGB", (W, H), (235,228,212))
    bars26 = [
        ((55,38,275,128), (180,18,18)),
        ((335,78,695,178), (18,18,18)),
        ((75,198,495,278), (180,18,18)),
        ((555,158,895,238), (18,18,18)),
        ((195,318,595,398), (180,18,18)),
        ((645,298,1095,378), (18,18,18)),
        ((95,438,415,508), (18,18,18)),
        ((475,418,845,498), (180,18,18)),
    ]
    for (x0,y0,x1,y1),col in bars26:
        sl=layer(); ImageDraw.Draw(sl).rectangle([(x0,y0),(x1,y1)], fill=(*col,205)); base=comp(base,sl)
    for cx,cy,r,col in [(315,218,38,(180,18,18)),(790,118,52,(18,18,18)),(545,458,32,(180,18,18))]:
        cl=layer(); ImageDraw.Draw(cl).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(*col,175), outline=(0,0,0,255), width=3); base=comp(base,cl)
    return base


def img_klimt_20260127():
    """Gustav Klimt — character consistency / ethics update."""
    base = Image.new("RGB", (W, H), (8, 4, 2))
    spiral27=layer(); sd27=ImageDraw.Draw(spiral27)
    for i in range(65):
        a27=math.radians(i*20); r27=22+i*7
        cx27=int(500+r27*math.cos(a27)); cy27=int(320+r27*math.sin(a27))
        sd27.arc([(cx27-r27//2,cy27-r27//2),(cx27+r27//2,cy27+r27//2)], a27*9, a27*9+185, fill=(205,168,48,rng.randint(72,188)), width=rng.randint(1,4))
    base=comp(base,spiral27)
    mos27=layer(); md27=ImageDraw.Draw(mos27)
    for _ in range(320):
        mx27=rng.randint(0,W-15); my27=rng.randint(0,H-15); sz27=rng.randint(3,14)
        mc27=[(205,168,48),(0,105,105),(142,48,20),(182,162,62),(68,30,102)][rng.randint(0,4)]
        md27.rectangle([(mx27,my27),(mx27+sz27,my27+sz27)], fill=(*mc27,rng.randint(100,202)))
    base=comp(base,mos27)
    face27=layer(); fd27=ImageDraw.Draw(face27)
    fd27.ellipse([(100,50),(420,420)], fill=(205,168,48,42), outline=(205,168,48,162), width=5)
    base=comp(base,face27)
    return base


def img_kandinsky_20260128():
    """Wassily Kandinsky — budget_tokens / reasoning guide."""
    base = Image.new("RGB", (W, H), (14, 30, 64))
    grid28=layer(); gd28=ImageDraw.Draw(grid28)
    for off in range(-H,W+H,55):
        gd28.line([(off,0),(off+H,H)], fill=(255,255,255,20), width=1)
        gd28.line([(off,0),(off-H,H)], fill=(255,255,255,20), width=1)
    base=comp(base,grid28)
    s1=layer(); ImageDraw.Draw(s1).ellipse([(580,15),(1060,385)], fill=(255,205,0,222)); base=comp(base,s1)
    s2=layer(); ImageDraw.Draw(s2).polygon([(180,505),(455,505),(318,165)], fill=(212,26,46,212)); base=comp(base,s2)
    s3=layer(); ImageDraw.Draw(s3).pieslice([(815,265),(1170,565)], 192, 352, fill=(26,85,212,192)); base=comp(base,s3)
    s4=layer(); ImageDraw.Draw(s4).ellipse([(88,72),(248,232)], fill=(255,112,16,212)); base=comp(base,s4)
    s5=layer(); ImageDraw.Draw(s5).arc([(48,48),(548,548)], 255, 68, fill=(0,0,0,255), width=8); base=comp(base,s5)
    ll28=layer(); ld28=ImageDraw.Draw(ll28)
    ld28.line([(0,392),(392,92)], fill=(0,0,0,255), width=4)
    ld28.line([(492,592),(892,192)], fill=(255,255,255,192), width=3)
    base=comp(base,ll28)
    return base


def img_calder_20260129():
    """Alexander Calder mobile — JetBrains IDE beta / adaptive tools."""
    base = Image.new("RGB", (W, H), (244,241,236))
    arms29=layer(); ad29=ImageDraw.Draw(arms29)
    ad29.line([(160,65),(1040,65)], fill=(16,16,16,255), width=4)
    ad29.line([(600,65),(600,205)], fill=(16,16,16,255), width=3)
    ad29.line([(160,65),(160,185)], fill=(16,16,16,255), width=3)
    ad29.line([(1040,65),(1040,185)], fill=(16,16,16,255), width=3)
    ad29.line([(270,285),(820,285)], fill=(16,16,16,255), width=3)
    ad29.line([(270,285),(270,425)], fill=(16,16,16,255), width=2)
    ad29.line([(820,285),(820,425)], fill=(16,16,16,255), width=2)
    ad29.line([(160,185),(460,185)], fill=(16,16,16,255), width=2)
    ad29.line([(310,185),(310,355)], fill=(16,16,16,255), width=2)
    base=comp(base,arms29)
    ellipses29 = [
        ((100,145,240,255),(212,38,38)),((560,45,720,205),(16,72,192)),((980,145,1100,275),(212,192,0)),
        ((230,385,370,515),(212,92,16)),((750,380,890,515),(36,152,72)),((270,305,390,415),(152,16,172)),
        ((145,185,265,295),(0,152,192)),
    ]
    for bounds,col in ellipses29:
        el=layer(); ImageDraw.Draw(el).ellipse(bounds, fill=(*col,222)); base=comp(base,el)
    return base


def img_kandinsky_20260328():
    """Wassily Kandinsky — subscriber growth / partner network theme."""
    base = Image.new("RGB", (W, H), (18, 34, 72))
    # 1. Diagonal grid (Kandinsky signature)
    grid28b = layer(); gd28b = ImageDraw.Draw(grid28b)
    for off in range(-H, W + H, 58):
        gd28b.line([(off, 0), (off + H, H)], fill=(255, 255, 255, 18), width=1)
        gd28b.line([(off, 0), (off - H, H)], fill=(255, 255, 255, 18), width=1)
    base = comp(base, grid28b)
    # 2. Concentric growth rings (subscriber expansion)
    rings28 = layer(); rd28 = ImageDraw.Draw(rings28)
    cx28, cy28 = 820, 210
    for i, (r28, alpha28) in enumerate([(260, 180), (200, 140), (148, 110), (98, 80), (52, 60)]):
        col28 = [(255, 210, 0), (255, 160, 30), (255, 100, 40), (220, 60, 20), (180, 30, 10)][i]
        rd28.arc([(cx28 - r28, cy28 - r28), (cx28 + r28, cy28 + r28)],
                 0, 360, fill=(*col28, alpha28), width=4)
    base = comp(base, rings28)
    # 3. Large bold circle (main growth symbol)
    c28 = layer(); ImageDraw.Draw(c28).ellipse([(580, 30), (1080, 420)],
        fill=(255, 205, 0, 48), outline=(255, 205, 0, 210), width=7)
    base = comp(base, c28)
    # 4. Red upward triangle (growth arrow / momentum)
    t28 = layer(); ImageDraw.Draw(t28).polygon(
        [(160, 520), (420, 520), (290, 175)],
        fill=(215, 28, 48, 215), outline=(0, 0, 0, 255))
    base = comp(base, t28)
    # 5. Network nodes + connector lines (partner network)
    net28 = layer(); nd28 = ImageDraw.Draw(net28)
    nodes28 = [(110, 155), (310, 80), (510, 190), (680, 95), (460, 360), (250, 430)]
    for i28, (nx28, ny28) in enumerate(nodes28):
        for j28 in range(i28 + 1, len(nodes28)):
            if abs(i28 - j28) <= 2:
                nd28.line([(nx28, ny28), nodes28[j28]], fill=(0, 220, 255, 80), width=2)
    for nx28, ny28 in nodes28:
        nd28.ellipse([(nx28 - 10, ny28 - 10), (nx28 + 10, ny28 + 10)],
                     fill=(0, 220, 255, 200), outline=(255, 255, 255, 180), width=2)
    base = comp(base, net28)
    # 6. Blue pie slice (Kandinsky structural element)
    p28 = layer(); ImageDraw.Draw(p28).pieslice(
        [(820, 310), (1160, 595)], start=195, end=345,
        fill=(30, 90, 215, 185), outline=(0, 0, 0, 220), width=4)
    base = comp(base, p28)
    # 7. Scatter primaries (Kandinsky scatter dots)
    sc28 = layer(); scd28 = ImageDraw.Draw(sc28)
    positions28 = [(155, 330), (325, 415), (495, 150), (705, 65), (860, 510),
                   (960, 195), (1055, 85), (1110, 460), (65, 490), (430, 310)]
    colors28 = [(255, 215, 0), (220, 30, 50), (255, 255, 255), (0, 240, 255),
                (255, 120, 20), (150, 50, 200), (50, 220, 50), (255, 215, 0),
                (0, 240, 255), (220, 30, 50)]
    for (px28, py28), pc28 in zip(positions28, colors28):
        r28s = rng.randint(8, 18)
        scd28.ellipse([(px28 - r28s, py28 - r28s), (px28 + r28s, py28 + r28s)],
                      fill=(*pc28, 210), outline=(0, 0, 0, 180), width=2)
    base = comp(base, sc28)
    return base


def img_mondrian_20260329():
    """Piet Mondrian Broadway Boogie Woogie style — Economic Index / learning curves theme."""
    base = Image.new("RGB", (W, H), (245, 241, 228))
    draw = ImageDraw.Draw(base)

    YELLOW = (255, 210, 0)
    RED    = (214, 36, 36)
    BLUE   = (26, 72, 192)
    BLACK  = (18, 18, 18)
    BW     = 14

    # 1. Vertical grid lines (representing data columns / time axis)
    vx = [0, 150, 310, 470, 620, 790, 950, 1100, W]
    for x in vx[1:-1]:
        draw.rectangle([(x - BW // 2, 0), (x + BW // 2, H)], fill=YELLOW)

    # 2. Horizontal grid lines (representing metric bands)
    hy = [0, 105, 220, 335, 445, 550, H]
    for y in hy[1:-1]:
        draw.rectangle([(0, y - BW // 2), (W, y + BW // 2)], fill=YELLOW)

    # 3. Coloured rectangles in selected cells (ascending pattern = learning curve)
    inset = BW // 2 + 2
    coloured = [
        (0, 4, RED),    (0, 3, BLUE),
        (1, 4, BLUE),   (1, 2, RED),
        (2, 3, RED),    (3, 1, BLUE),
        (3, 3, RED),    (4, 0, YELLOW),
        (4, 2, BLUE),   (5, 0, RED),
        (5, 1, BLUE),   (6, 0, BLUE),
        (6, 2, RED),    (7, 0, RED),
        (7, 1, YELLOW),
    ]
    for ci, ri, col in coloured:
        if ci < len(vx) - 1 and ri < len(hy) - 1:
            x0 = vx[ci] + inset
            y0 = hy[ri] + inset
            x1 = vx[ci + 1] - inset
            y1 = hy[ri + 1] - inset
            draw.rectangle([(x0, y0), (x1, y1)], fill=col)

    # 4. Intersection dots — small coloured squares at grid crossings (Broadway Boogie detail)
    dot_cycle = [RED, BLUE, YELLOW, RED, BLUE, YELLOW, RED]
    dot_size = 6
    for i, x in enumerate(vx[1:-1]):
        for j, y in enumerate(hy[1:-1]):
            col = dot_cycle[(i + j) % len(dot_cycle)]
            draw.rectangle(
                [(x - dot_size, y - dot_size), (x + dot_size, y + dot_size)],
                fill=col
            )

    # 5. Bold black grid overlay lines (Mondrian structural frame)
    for x in vx[1:-1]:
        draw.line([(x, 0), (x, H)], fill=BLACK, width=2)
    for y in hy[1:-1]:
        draw.line([(0, y), (W, y)], fill=BLACK, width=2)

    return base


def img_seurat_20260130():
    """Georges Seurat — January performance report / caching analytics."""
    base = Image.new("RGB", (W, H), (14, 20, 50))
    dl30=layer(); dd30=ImageDraw.Draw(dl30)
    for _ in range(5200):
        dx=rng.randint(0,W); dy=rng.randint(0,H)
        cx30,cy30=W*0.6,H*0.42; dist30=math.hypot(dx-cx30,dy-cy30)
        bright30=max(0,1-dist30/490)
        r30=int(16+bright30*239); g30=int(32+bright30*188); b30=int(88+bright30*167)
        hs30=rng.randint(-27,27); dr30=rng.randint(2,5)
        dd30.ellipse([(dx-dr30,dy-dr30),(dx+dr30,dy+dr30)], fill=(min(255,r30+hs30),min(255,g30),min(255,b30),rng.randint(148,236)))
    base=comp(base,dl30)
    rl30=layer(); rd30=ImageDraw.Draw(rl30)
    for rad30 in [68,148,228,318,418]:
        rd30.arc([(W//2-rad30+100,H//2-rad30),(W//2+rad30+100,H//2+rad30)], 0, 360, fill=(255,205,88,46), width=2)
    base=comp(base,rl30)
    return base


def img_franz_marc_20260131():
    """Franz Marc jewel tones — January safety summary / welfare."""
    base = Image.new("RGB", (W, H), (6, 32, 72))
    panels31 = [((0,0,370,H),(0,112,148,112)),((340,0,720,H),(16,72,32,112)),((690,0,W,H),(92,16,112,112))]
    for r,c in panels31:
        pl=layer(); ImageDraw.Draw(pl).rectangle(r, fill=c); base=comp(base,pl)
    for pts,col in [([(85,375),(275,185),(475,330),(675,130),(875,280),(1095,82)],(245,188,68)),
                    ([(35,272),(235,482),(435,258),(635,458),(835,178),(1095,372)],(82,208,248))]:
        ll=layer(); ImageDraw.Draw(ll).line(pts, fill=(*col,172), width=6); base=comp(base,ll)
    for cx,cy,r,col in [(278,232,72,(245,188,68)),(668,352,92,(82,208,248)),(968,178,62,(208,92,188))]:
        el=layer(); ImageDraw.Draw(el).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(*col,148), outline=(255,255,255,92), width=3); base=comp(base,el)
    return base


def img_franz_marc_20251225():
    """Franz Marc jewel tones — DOE science partnership / safety compliance."""
    base = Image.new("RGB", (W, H), (6, 28, 68))
    # 1. Three rich jewel-tone background panels
    panels = [((0,0,380,H),(0,108,142,112)),((350,0,730,H),(14,68,28,112)),((700,0,W,H),(88,14,108,112))]
    for r, c in panels:
        pl = layer(); ImageDraw.Draw(pl).rectangle(r, fill=c); base = comp(base, pl)
    # 2. Stylised mountain / landscape shapes (Franz Marc nature)
    mtn = layer(); md = ImageDraw.Draw(mtn)
    md.polygon([(0,H),(200,250),(400,H)], fill=(0,168,198,148))
    md.polygon([(250,H),(520,160),(790,H)], fill=(22,148,42,130))
    md.polygon([(600,H),(880,200),(W,H)], fill=(168,28,128,120))
    base = comp(base, mtn)
    # 3. Gold spiral / sun-disc
    sun = layer(); sd = ImageDraw.Draw(sun)
    for r25 in range(90,8,-12):
        sd.arc([(820-r25,80-r25),(820+r25,80+r25)], 0, 360, fill=(218,178,48,int(210*(1-r25/90))), width=3)
    sd.ellipse([(800,60),(840,100)], fill=(218,178,48,220))
    base = comp(base, sun)
    # 4. Stylised animal silhouette (deer / reindeer — Christmas touch)
    deer = layer(); dd = ImageDraw.Draw(deer)
    dd.ellipse([(140,180),(260,260)], fill=(218,148,28,180))  # body
    dd.ellipse([(238,148),(288,198)], fill=(218,148,28,180))  # head
    dd.line([(260,148),(278,108),(298,88)], fill=(218,148,28,160), width=5)   # antler left
    dd.line([(278,108),(300,98)], fill=(218,148,28,140), width=4)
    dd.line([(260,148),(242,108),(222,88)], fill=(218,148,28,160), width=5)   # antler right
    for lx, ly in [(152,260),(172,260),(210,260),(228,260)]:
        dd.line([(lx,260),(lx-4,310)], fill=(218,148,28,150), width=4)
    base = comp(base, deer)
    # 5. Jewel mosaic scatter
    mos = layer(); mosd = ImageDraw.Draw(mos)
    for _ in range(280):
        mx = rng.randint(0,W-12); my = rng.randint(0,H-12); sz = rng.randint(2,10)
        mc = [(218,178,48),(0,168,198),(142,28,168),(22,148,42),(168,88,28)][rng.randint(0,4)]
        mosd.rectangle([(mx,my),(mx+sz,my+sz)], fill=(*mc,rng.randint(90,188)))
    base = comp(base, mos)
    return base


def img_klee_20251226():
    """Paul Klee warm/cool grid — model migration / Haiku deprecation."""
    base = Image.new("RGB", (W, H), (24, 20, 32))
    # 1. Grid of coloured cells
    cols26 = [(188,88,28),(28,128,188),(188,168,28),(88,28,168),(28,168,88),(168,28,88),(28,88,168),(168,128,28)]
    cw, ch = W // 10, H // 7
    cl = layer(); cd = ImageDraw.Draw(cl)
    for row in range(8):
        for col in range(11):
            cx26 = col * cw; cy26 = row * ch
            base_col = cols26[(row * 3 + col * 2) % len(cols26)]
            alpha26 = rng.randint(120, 195)
            cd.rectangle([(cx26, cy26), (cx26+cw-2, cy26+ch-2)], fill=(*base_col, alpha26))
    base = comp(base, cl)
    # 2. Dark grid lines
    gl = layer(); gd = ImageDraw.Draw(gl)
    for col in range(12):
        gd.line([(col*cw, 0), (col*cw, H)], fill=(0,0,0,180), width=2)
    for row in range(9):
        gd.line([(0, row*ch), (W, row*ch)], fill=(0,0,0,180), width=2)
    base = comp(base, gl)
    # 3. White node circles at grid intersections
    nl = layer(); nd = ImageDraw.Draw(nl)
    for row in range(1, 8):
        for col in range(1, 11):
            if rng.random() > 0.55:
                nd.ellipse([(col*cw-8,row*ch-8),(col*cw+8,row*ch+8)],
                           fill=(255,255,255,200), outline=(0,0,0,180), width=2)
    base = comp(base, nl)
    # 4. Larger accent circles (model nodes)
    al = layer(); ad = ImageDraw.Draw(al)
    for cx26, cy26, r26, col26 in [(cw*3,ch*2,28,(255,220,60)),(cw*7,ch*4,22,(60,200,255)),(cw*5,ch*6,18,(255,80,120))]:
        ad.ellipse([(cx26-r26,cy26-r26),(cx26+r26,cy26+r26)],
                   fill=(*col26,220), outline=(255,255,255,200), width=3)
    base = comp(base, al)
    return base


def img_moholy_20251227():
    """László Moholy-Nagy Bauhaus — transparency / year-end tips."""
    base = Image.new("RGB", (W, H), (248, 245, 238))
    # 1. Large overlapping translucent circles
    circles27 = [(280,220,190,(220,40,40)),(580,180,160,(40,100,200)),(820,300,140,(40,180,80)),(420,420,170,(180,40,180))]
    for cx27, cy27, r27, col27 in circles27:
        cl = layer(); ImageDraw.Draw(cl).ellipse([(cx27-r27,cy27-r27),(cx27+r27,cy27+r27)],
                                                  fill=(*col27,70), outline=(*col27,160), width=4)
        base = comp(base, cl)
    # 2. Overlapping rectangles (Bauhaus geometry)
    rects27 = [((100,80,400,320),(40,100,200,80)),((700,180,1000,480),(220,40,40,70)),((350,350,750,580),(40,180,80,60))]
    for bounds27, col27 in rects27:
        rl = layer(); ImageDraw.Draw(rl).rectangle(bounds27, fill=col27, outline=(col27[0],col27[1],col27[2],200), width=3)
        base = comp(base, rl)
    # 3. Thin black structural lines
    ll = layer(); ld = ImageDraw.Draw(ll)
    for pts27 in [[(150,0),(150,H)],[(0,180),(W,180)],[(900,0),(900,H)],[(0,450),(W,450)],[(500,0),(500,H)]]:
        ld.line(pts27, fill=(20,20,20,120), width=2)
    base = comp(base, ll)
    # 4. Small primary-colour squares scatter
    sl = layer(); sd27 = ImageDraw.Draw(sl)
    for _ in range(40):
        sx27 = rng.randint(0,W-20); sy27 = rng.randint(0,H-20); ssz27 = rng.randint(8,22)
        sc27 = [(220,40,40),(40,100,200),(240,190,0),(40,180,80)][rng.randint(0,3)]
        sd27.rectangle([(sx27,sy27),(sx27+ssz27,sy27+ssz27)], fill=(*sc27,160))
    base = comp(base, sl)
    return base


def img_lissitzky_20251228():
    """El Lissitzky Constructivism — API patterns / developer tooling."""
    base = Image.new("RGB", (W, H), (245, 240, 228))
    # 1. Bold red diagonal bar
    rb = layer(); ImageDraw.Draw(rb).polygon([(80,0),(320,0),(240,H),(0,H)], fill=(188,28,28,230))
    base = comp(base, rb)
    # 2. Large black circle
    bc = layer(); ImageDraw.Draw(bc).ellipse([(550,40),(950,440)], fill=(0,0,0,0), outline=(20,20,20,220), width=18)
    base = comp(base, bc)
    # 3. Solid black rectangle (Lissitzky structure)
    br = layer(); ImageDraw.Draw(br).rectangle([(680,280),(1060,580)], fill=(20,20,20,210))
    base = comp(base, br)
    # 4. Red rectangle accent
    rr = layer(); ImageDraw.Draw(rr).rectangle([(380,200),(580,360)], fill=(188,28,28,200))
    base = comp(base, rr)
    # 5. Diagonal black bars
    db = layer(); dbd = ImageDraw.Draw(db)
    dbd.line([(380,H),(W,120)], fill=(20,20,20,200), width=12)
    dbd.line([(0,380),(420,80)], fill=(20,20,20,120), width=6)
    base = comp(base, db)
    # 6. Small white squares (Constructivist detail)
    ws = layer(); wsd = ImageDraw.Draw(ws)
    for wx28, wy28, wsz28 in [(440,420,32),(820,480,24),(950,120,20),(180,320,18),(600,500,28)]:
        wsd.rectangle([(wx28,wy28),(wx28+wsz28,wy28+wsz28)], fill=(245,240,228,220))
    base = comp(base, ws)
    return base


def img_leger_20251229():
    """Fernand Léger — APIs / MCP / infrastructure year review."""
    base = Image.new("RGB", (W, H), (20, 18, 28))
    # 1. Bold mechanical cylinder shapes
    cyl = layer(); cd29 = ImageDraw.Draw(cyl)
    for cx29, cy29, cw29, ch29, col29 in [(80,60,160,300,(212,38,38)),(320,20,140,260,(28,100,212)),(560,100,180,320,(212,168,0)),(820,40,160,280,(28,168,68))]:
        cd29.rounded_rectangle([(cx29,cy29),(cx29+cw29,cy29+ch29)], radius=cw29//2, fill=(*col29,210), outline=(255,255,255,60), width=3)
    base = comp(base, cyl)
    # 2. Black mechanical outlines / bolts
    ol = layer(); od29 = ImageDraw.Draw(ol)
    od29.arc([(60,40),(280,260)], 0, 360, fill=(0,0,0,200), width=6)
    od29.arc([(300,0),(500,200)], 0, 360, fill=(0,0,0,180), width=5)
    od29.rectangle([(820,300),(1100,550)], fill=(0,0,0,0), outline=(0,0,0,180), width=6)
    base = comp(base, ol)
    # 3. Flat primary colour blocks (Léger flat areas)
    blocks29 = [((1040,0,W,180),(212,38,38)),((0,420,160,H),(28,100,212)),((1040,400,W,H),(212,168,0))]
    for b29, c29 in blocks29:
        bl = layer(); ImageDraw.Draw(bl).rectangle(b29, fill=(*c29,190)); base = comp(base, bl)
    # 4. White bold horizontal lines (industrial grid)
    hl = layer(); hd29 = ImageDraw.Draw(hl)
    for y29 in [150, 300, 450]:
        hd29.line([(0,y29),(W,y29)], fill=(255,255,255,40), width=2)
    base = comp(base, hl)
    # 5. Small gear-like circles
    gl29 = layer(); gd29 = ImageDraw.Draw(gl29)
    for gx29, gy29, gr29 in [(700,520,30),(140,520,24),(480,430,20),(960,460,18)]:
        for angle29 in range(0,360,45):
            rad29 = math.radians(angle29)
            tx29 = gx29 + int((gr29+8)*math.cos(rad29)); ty29 = gy29 + int((gr29+8)*math.sin(rad29))
            gd29.ellipse([(tx29-5,ty29-5),(tx29+5,ty29+5)], fill=(255,255,255,140))
        gd29.arc([(gx29-gr29,gy29-gr29),(gx29+gr29,gy29+gr29)], 0, 360, fill=(255,255,255,160), width=3)
    base = comp(base, gl29)
    return base


def img_balla_20251230():
    """Giacomo Balla Futurism — streaming speed / batch throughput."""
    base = Image.new("RGB", (W, H), (12, 10, 20))
    # 1. Radiating speed lines from vanishing point
    vp30 = (W * 0.72, H * 0.38)
    sl30 = layer(); sd30 = ImageDraw.Draw(sl30)
    speed_cols30 = [(212,38,38),(38,100,212),(212,168,0),(38,168,68),(168,68,212),(68,188,212)]
    for angle30 in range(0, 360, 14):
        rad30 = math.radians(angle30)
        ex30 = vp30[0] + math.cos(rad30)*W; ey30 = vp30[1] + math.sin(rad30)*W
        col30 = speed_cols30[angle30 // 60 % len(speed_cols30)]
        sd30.line([(vp30[0], vp30[1]), (ex30, ey30)], fill=(*col30, rng.randint(40,120)), width=rng.randint(2,8))
    base = comp(base, sl30)
    # 2. Overlapping speed planes (futurist motion)
    for pts30, col30 in [
        ([(0,0),(350,0),(vp30[0],vp30[1])], (212,38,38,130)),
        ([(W,0),(650,0),(vp30[0],vp30[1])], (38,100,212,110)),
        ([(0,H),(300,H),(vp30[0],vp30[1])], (212,168,0,100)),
        ([(W,H),(900,H),(vp30[0],vp30[1])], (38,168,68,90)),
    ]:
        pl30 = layer(); ImageDraw.Draw(pl30).polygon(pts30, fill=col30); base = comp(base, pl30)
    # 3. Motion blur ellipses
    ml30 = layer(); md30 = ImageDraw.Draw(ml30)
    for _ in range(18):
        mx30 = rng.randint(100,W-100); my30 = rng.randint(80,H-80)
        mw30 = rng.randint(60,200); mh30 = rng.randint(12,35)
        mc30 = speed_cols30[rng.randint(0,len(speed_cols30)-1)]
        md30.ellipse([(mx30-mw30,my30-mh30),(mx30+mw30,my30+mh30)], fill=(*mc30,rng.randint(60,130)))
    base = comp(base, ml30)
    # 4. Bright core at vanishing point
    core30 = layer(); ImageDraw.Draw(core30).ellipse(
        [(vp30[0]-40,vp30[1]-40),(vp30[0]+40,vp30[1]+40)], fill=(255,240,200,230))
    base = comp(base, core30)
    return base


def img_kandinsky_20251231():
    """Wassily Kandinsky — year in review / agents / composition."""
    base = Image.new("RGB", (W, H), (16, 32, 68))
    # 1. Double diagonal grid (Kandinsky signature)
    grid31 = layer(); gd31 = ImageDraw.Draw(grid31)
    for off in range(-H, W+H, 52):
        gd31.line([(off,0),(off+H,H)], fill=(255,255,255,16), width=1)
        gd31.line([(off,0),(off-H,H)], fill=(255,255,255,16), width=1)
    base = comp(base, grid31)
    # 2. Large gold year-circle
    yc31 = layer(); ImageDraw.Draw(yc31).ellipse([(580,20),(1100,440)], fill=(255,208,0,52), outline=(255,208,0,215), width=8)
    base = comp(base, yc31)
    # 3. Red upward triangle (achievement / growth)
    tr31 = layer(); ImageDraw.Draw(tr31).polygon([(155,525),(435,525),(295,170)], fill=(212,28,48,215), outline=(0,0,0,255))
    base = comp(base, tr31)
    # 4. Blue arc (horizon / future)
    arc31 = layer(); ImageDraw.Draw(arc31).arc([(40,40),(560,560)], start=250, end=72, fill=(0,0,0,255), width=9)
    base = comp(base, arc31)
    # 5. Green diamond (balance / insight)
    dm31 = layer(); ImageDraw.Draw(dm31).polygon([(545,355),(638,252),(728,355),(638,458)], fill=(38,178,88,200), outline=(0,0,0,255), width=4)
    base = comp(base, dm31)
    # 6. Orange circle (the year / the cycle)
    oc31 = layer(); ImageDraw.Draw(oc31).ellipse([(92,75),(258,241)], fill=(255,115,18,215), outline=(0,0,0,255), width=5)
    base = comp(base, oc31)
    # 7. Scatter constellation of small circles
    sc31 = layer(); scd31 = ImageDraw.Draw(sc31)
    pos31 = [(148,328),(318,412),(492,148),(708,62),(862,508),(958,192),(1052,82),(1108,458),(62,492),(428,308)]
    cols31 = [(255,208,0),(212,28,48),(255,255,255),(0,238,255),(255,115,18),(148,48,198),(48,218,48),(255,208,0),(0,238,255),(212,28,48)]
    for (px31,py31),pc31 in zip(pos31,cols31):
        rs31 = rng.randint(8,18)
        scd31.ellipse([(px31-rs31,py31-rs31),(px31+rs31,py31+rs31)], fill=(*pc31,208), outline=(0,0,0,172), width=2)
    base = comp(base, sc31)
    return base


def img_miro_20251218():
    """Joan Miró — Agent Skills enterprise / open standard / marketplace."""
    base = Image.new("RGB", (W, H), (28, 24, 68))
    # 1. Deep-indigo background wash
    wash = layer(); ImageDraw.Draw(wash).rectangle([(0,0),(W,H)], fill=(28,24,68,255)); base = comp(base, wash)
    # 2. Bold biomorphic blobs (agent skill shapes)
    blobs = [
        ([(180,120),(380,120),(440,220),(380,340),(180,340),(120,220)], (212,38,38,210)),
        ([(680,80),(820,80),(880,180),(820,300),(680,300),(620,180)], (38,130,212,200)),
        ([(900,280),(1060,280),(1120,390),(1060,510),(900,510),(840,390)], (212,192,0,200)),
        ([(300,380),(460,380),(520,470),(460,570),(300,570),(240,470)], (38,192,88,190)),
        ([(100,400),(220,400),(260,490),(220,570),(100,570),(60,490)], (192,38,192,180)),
    ]
    for pts18, col18 in blobs:
        bl = layer(); ImageDraw.Draw(bl).polygon(pts18, fill=col18, outline=(0,0,0,200)); base = comp(base, bl)
    # 3. Black outlines / connecting lines (network of skills)
    nl = layer(); nd = ImageDraw.Draw(nl)
    nd.line([(280,230),(680,180)], fill=(0,0,0,200), width=3)
    nd.line([(820,190),(900,390)], fill=(0,0,0,180), width=3)
    nd.line([(380,460),(460,470)], fill=(0,0,0,160), width=2)
    base = comp(base, nl)
    # 4. Stars (Miró signature stars)
    sl18 = layer(); sd18 = ImageDraw.Draw(sl18)
    for sx18, sy18, sr18 in [(550,150,12),(750,500,10),(200,300,8),(1050,180,10),(440,80,8)]:
        for a18 in range(0,360,72):
            r18 = math.radians(a18)
            x18 = sx18+int(sr18*math.cos(r18)); y18 = sy18+int(sr18*math.sin(r18))
            sd18.line([(sx18,sy18),(x18,y18)], fill=(255,240,80,220), width=2)
        sd18.ellipse([(sx18-4,sy18-4),(sx18+4,sy18+4)], fill=(255,240,80,230))
    base = comp(base, sl18)
    # 5. White dot nodes
    dn18 = layer(); dnd18 = ImageDraw.Draw(dn18)
    for dx18, dy18 in [(280,230),(680,180),(820,190),(900,390),(380,460),(460,470),(160,490)]:
        dnd18.ellipse([(dx18-9,dy18-9),(dx18+9,dy18+9)], fill=(255,255,255,210), outline=(0,0,0,180), width=2)
    base = comp(base, dn18)
    return base


def img_delaunay_20251219():
    """Robert Delaunay — Claude in Chrome / cross-device / signals."""
    base = Image.new("RGB", (W, H), (16, 14, 28))
    # 1. Large overlapping spectral disc rings
    discs19 = [
        (380, 290, 260, [(255,0,0),(255,120,0),(255,220,0),(0,200,80),(0,150,255),(120,0,255)]),
        (780, 200, 210, [(255,80,0),(255,200,0),(80,220,0),(0,180,200),(60,0,240),(200,0,180)]),
        (1000, 420, 190, [(220,0,0),(255,160,0),(200,240,0),(0,240,120),(0,100,255),(140,0,220)]),
    ]
    for dcx19, dcy19, dr19, colors19 in discs19:
        for i19, col19 in enumerate(colors19):
            r19 = dr19 - i19 * (dr19 // len(colors19))
            if r19 > 0:
                dl = layer(); ImageDraw.Draw(dl).ellipse([(dcx19-r19,dcy19-r19),(dcx19+r19,dcy19+r19)],
                    fill=(*col19, 90), outline=(*col19,140), width=2)
                base = comp(base, dl)
    # 2. Bright centre dots
    for dcx19, dcy19, _ in [(380,290,0),(780,200,0),(1000,420,0)]:
        cl = layer(); ImageDraw.Draw(cl).ellipse([(dcx19-18,dcy19-18),(dcx19+18,dcy19+18)], fill=(255,255,255,220))
        base = comp(base, cl)
    # 3. Radiating signal arcs
    rl = layer(); rd19 = ImageDraw.Draw(rl)
    for rad19 in [60, 110, 170, 230]:
        rd19.arc([(180-rad19,290-rad19),(180+rad19,290+rad19)], 270, 450, fill=(255,255,255,30), width=2)
    base = comp(base, rl)
    # 4. Dark separator bands
    bl19 = layer(); bd19 = ImageDraw.Draw(bl19)
    for y19 in [H//3, 2*H//3]:
        bd19.line([(0,y19),(W,y19)], fill=(0,0,0,60), width=1)
    base = comp(base, bl19)
    return base


def img_calder_20251220():
    """Alexander Calder mobile — CLAUDE.md / adaptive context / flexible memory."""
    base = Image.new("RGB", (W, H), (242, 238, 230))
    # 1. Mobile arm structure
    arms20 = layer(); ad20 = ImageDraw.Draw(arms20)
    ad20.line([(120,60),(1080,60)], fill=(16,16,16,255), width=5)
    ad20.line([(600,60),(600,210)], fill=(16,16,16,255), width=4)
    ad20.line([(120,60),(120,190)], fill=(16,16,16,255), width=4)
    ad20.line([(1080,60),(1080,190)], fill=(16,16,16,255), width=4)
    ad20.line([(260,310),(840,310)], fill=(16,16,16,255), width=3)
    ad20.line([(260,310),(260,450)], fill=(16,16,16,255), width=3)
    ad20.line([(840,310),(840,450)], fill=(16,16,16,255), width=3)
    ad20.line([(160,190),(460,190)], fill=(16,16,16,255), width=3)
    ad20.line([(310,190),(310,370)], fill=(16,16,16,255), width=2)
    ad20.line([(460,190),(680,190)], fill=(16,16,16,255), width=2)
    ad20.line([(570,190),(570,440)], fill=(16,16,16,255), width=2)
    base = comp(base, arms20)
    # 2. Primary coloured shapes
    shapes20 = [
        ((60,148,200,268),(212,38,38)),((540,45,700,205),(16,72,196)),
        ((1018,148,1140,278),(212,192,0)),((228,385,368,525),(212,92,16)),
        ((760,395,900,535),(36,152,72)),((270,320,390,430),(152,16,172)),
        ((148,190,268,298),(0,156,198)),((380,185,498,305),(212,38,38)),
        ((510,182,628,302),(212,192,0)),((736,370,856,490),(16,72,196)),
    ]
    for bounds20, col20 in shapes20:
        el = layer(); ImageDraw.Draw(el).ellipse(bounds20, fill=(*col20,222)); base = comp(base, el)
    return base


def img_mondrian_20251221():
    """Piet Mondrian — multimodal document grids / structured analysis."""
    base = Image.new("RGB", (W, H), (245, 242, 230))
    # 1. Yellow band
    yb = layer(); ImageDraw.Draw(yb).rectangle([(0,0),(W,110)], fill=(255,210,0,240)); base = comp(base, yb)
    # 2. Bold black grid lines
    gl = layer(); gd21 = ImageDraw.Draw(gl)
    for x21 in [0, 200, 440, 700, 920, W]:
        gd21.line([(x21,0),(x21,H)], fill=(10,10,10,255), width=8)
    for y21 in [0, 110, 260, 420, H]:
        gd21.line([(0,y21),(W,y21)], fill=(10,10,10,255), width=8)
    base = comp(base, gl)
    # 3. Red and blue rectangles
    rects21 = [
        ((0,110,200,260),(195,30,30,230)),((440,260,700,420),(30,60,195,220)),
        ((920,0,W,260),(195,30,30,210)),((0,420,440,H),(30,60,195,200)),
        ((700,0,920,110),(30,60,195,190)),((200,420,440,H),(195,160,0,180)),
    ]
    for r21, c21 in rects21:
        rl = layer(); ImageDraw.Draw(rl).rectangle(r21, fill=c21); base = comp(base, rl)
    # 4. Re-draw grid lines on top to keep clean
    gl2 = layer(); gd21b = ImageDraw.Draw(gl2)
    for x21 in [0, 200, 440, 700, 920, W]:
        gd21b.line([(x21,0),(x21,H)], fill=(10,10,10,255), width=8)
    for y21 in [0, 110, 260, 420, H]:
        gd21b.line([(0,y21),(W,y21)], fill=(10,10,10,255), width=8)
    base = comp(base, gl2)
    return base


def img_seurat_20251222():
    """Georges Seurat pointillist — evaluation pipelines / data density / analytics."""
    base = Image.new("RGB", (W, H), (14, 20, 44))
    # 1. Dense pointillist dots building a quality-metric graph shape
    dl22 = layer(); dd22 = ImageDraw.Draw(dl22)
    for _ in range(6000):
        dx22 = rng.randint(0, W); dy22 = rng.randint(0, H)
        # Curve shape: quality line from lower-left to upper-right
        cx22 = dx22 / W; cy22 = dy22 / H
        on_curve = abs(cy22 - (1 - cx22 * 0.7)) < 0.25
        bright22 = 0.8 if on_curve else max(0, 0.3 - abs(cy22 - 0.6) * 0.4)
        r22 = int(20 + bright22 * 235); g22 = int(40 + bright22 * 180); b22 = int(100 + bright22 * 155)
        hs22 = rng.randint(-20, 20); dr22 = rng.randint(2, 5)
        dd22.ellipse([(dx22-dr22,dy22-dr22),(dx22+dr22,dy22+dr22)],
                     fill=(min(255,r22+hs22),min(255,g22),min(255,b22),rng.randint(140,230)))
    base = comp(base, dl22)
    # 2. Bright data-point clusters (eval scores)
    for cx22, cy22, cr22 in [(960,120,35),(760,200,28),(540,310,22),(320,440,18)]:
        cl = layer(); ImageDraw.Draw(cl).ellipse([(cx22-cr22,cy22-cr22),(cx22+cr22,cy22+cr22)],
                                                  fill=(255,220,60,200))
        base = comp(base, cl)
    # 3. Faint grid (eval axis)
    gl22 = layer(); gd22b = ImageDraw.Draw(gl22)
    for x22 in range(0, W, W//6):
        gd22b.line([(x22,0),(x22,H)], fill=(255,255,255,18), width=1)
    for y22 in range(0, H, H//5):
        gd22b.line([(0,y22),(W,y22)], fill=(255,255,255,18), width=1)
    base = comp(base, gl22)
    return base


def img_klimt_20251223():
    """Gustav Klimt — copyright / ethics / AI craftsmanship and IP."""
    base = Image.new("RGB", (W, H), (12, 8, 18))
    # 1. Gold spiral background
    gs23 = layer(); gsd23 = ImageDraw.Draw(gs23)
    for _ in range(220):
        gx23 = rng.randint(0, W); gy23 = rng.randint(0, H)
        gr23 = rng.randint(6, 28)
        gsd23.arc([(gx23-gr23,gy23-gr23),(gx23+gr23,gy23+gr23)],
                  rng.randint(0,360), rng.randint(180,540),
                  fill=(205,168,48,rng.randint(60,180)), width=rng.randint(1,3))
    base = comp(base, gs23)
    # 2. Mosaic tile scatter
    ms23 = layer(); msd23 = ImageDraw.Draw(ms23)
    for _ in range(360):
        mx23 = rng.randint(0, W-16); my23 = rng.randint(0, H-16); sz23 = rng.randint(3, 14)
        mc23 = [(205,168,48),(0,108,108),(142,48,20),(185,162,62),(68,28,105)][rng.randint(0,4)]
        msd23.rectangle([(mx23,my23),(mx23+sz23,my23+sz23)], fill=(*mc23,rng.randint(100,200)))
    base = comp(base, ms23)
    # 3. Large teal/rust accent panels
    pl23 = layer(); pd23 = ImageDraw.Draw(pl23)
    pd23.rectangle([(0,0),(320,H)], fill=(0,88,100,88))
    pd23.rectangle([(880,0),(W,H)], fill=(148,44,18,78))
    base = comp(base, pl23)
    # 4. Gold face oval / medallion
    face23 = layer(); fd23 = ImageDraw.Draw(face23)
    fd23.ellipse([(440,60),(760,420)], fill=(205,168,48,35), outline=(205,168,48,160), width=6)
    for rc23 in [50,90,130,175]:
        fd23.arc([(600-rc23,240-rc23),(600+rc23,240+rc23)], 0, 360, fill=(205,168,48,40), width=2)
    base = comp(base, face23)
    return base


def img_malevich_20251224():
    """Kazimir Malevich — Christmas Eve / prompt library / structure and safety."""
    base = Image.new("RGB", (W, H), (242, 238, 224))
    # 1. Large bold black tilted square (Suprematist anchor)
    bs24 = layer()
    angle24 = 18
    cx24, cy24, s24 = W//2-50, H//2-30, 220
    pts24 = []
    for ax24, ay24 in [(-s24//2,-s24//2),(s24//2,-s24//2),(s24//2,s24//2),(-s24//2,s24//2)]:
        r24 = math.radians(angle24)
        pts24.append((cx24 + int(ax24*math.cos(r24)-ay24*math.sin(r24)),
                      cy24 + int(ax24*math.sin(r24)+ay24*math.cos(r24))))
    ImageDraw.Draw(bs24).polygon(pts24, fill=(18,18,18,235))
    base = comp(base, bs24)
    # 2. Red rectangle (diagonal)
    rr24 = layer(); rrd24 = ImageDraw.Draw(rr24)
    rr24_pts = [(80,80),(340,80),(440,260),(180,260)]
    rrd24.polygon(rr24_pts, fill=(188,28,28,220))
    base = comp(base, rr24)
    # 3. Navy bar
    nb24 = layer(); nbd24 = ImageDraw.Draw(nb24)
    nb24_pts = [(820,60),(1100,60),(1140,220),(860,220)]
    nbd24.polygon(nb24_pts, fill=(28,28,142,210))
    base = comp(base, nb24)
    # 4. Yellow accent
    ya24 = layer(); yad24 = ImageDraw.Draw(ya24)
    yad24.polygon([(140,500),(360,500),(400,580),(180,580)], fill=(220,188,0,200))
    base = comp(base, ya24)
    # 5. Small circle (Christmas star / prompt origin)
    sc24 = layer(); ImageDraw.Draw(sc24).ellipse([(320,80),(400,160)], fill=(18,18,18,220))
    base = comp(base, sc24)
    return base


def img_leger_20251211():
    """Fernand Léger industrial style — MCP infrastructure & Accenture partnership theme."""
    rng2 = Random(42)
    base = Image.new("RGB", (W, H), (14, 16, 22))
    draw = ImageDraw.Draw(base)
    # 1. Industrial pipe horizontals
    for y in [120, 220, 360, 470, 560]:
        col = rng2.choice([(220,60,40),(40,120,220),(30,190,80),(220,180,30)])
        draw.rectangle([(0, y-16), (W, y+16)], fill=col)
        draw.rectangle([(0, y-18), (W, y-14)], fill=(0,0,0))
        draw.rectangle([(0, y+14), (W, y+18)], fill=(0,0,0))
    # 2. Bold vertical columns
    for x in [180, 480, 780, 1040]:
        col = rng2.choice([(200,50,30),(30,100,200),(180,160,20)])
        lv = layer(); ImageDraw.Draw(lv).rectangle([(x-28,0),(x+28,H)], fill=col+(200,))
        base = comp(base, lv)
    # 3. Bold mechanical circle joints
    for cx, cy, r in [(180,120,44),(480,360,52),(780,220,38),(1040,470,46),(600,560,34)]:
        lc = layer(); d = ImageDraw.Draw(lc)
        d.ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=(240,240,240,230))
        d.ellipse([(cx-r//2,cy-r//2),(cx+r//2,cy+r//2)], fill=(14,16,22,230))
        base = comp(base, lc)
    # 4. Gear-like notched rectangle (flat mechanical)
    gx, gy = 860, 80
    lg = layer(); dg = ImageDraw.Draw(lg)
    dg.rectangle([(gx, gy),(gx+280, gy+180)], fill=(220,60,40,210))
    for nx in range(gx, gx+280, 40):
        dg.rectangle([(nx, gy-18),(nx+20, gy+8)], fill=(220,60,40,200))
        dg.rectangle([(nx, gy+172),(nx+20, gy+198)], fill=(220,60,40,200))
    base = comp(base, lg)
    # 5. Black outline grid overlay (Léger's bold outlines)
    for x in range(0, W, 80):
        draw.line([(x,0),(x,H)], fill=(0,0,0), width=2)
    for y in range(0, H, 80):
        draw.line([(0,y),(W,y)], fill=(0,0,0), width=2)
    return base


def img_lissitzky_20251212():
    """El Lissitzky Constructivist style — MCP developer guide / tooling theme."""
    rng2 = Random(42)
    base = Image.new("RGB", (W, H), (245, 240, 228))
    draw = ImageDraw.Draw(base)
    # 1. Bold diagonal red bars
    for i in range(5):
        x0 = rng2.randint(-100, 800)
        y0 = rng2.randint(-80, 400)
        lr = layer(); dr = ImageDraw.Draw(lr)
        pts = [(x0,y0),(x0+260,y0),(x0+340,y0+90),(x0+80,y0+90)]
        dr.polygon(pts, fill=(200,28,28,220))
        base = comp(base, lr)
    # 2. Black geometric bars (vertical + horizontal)
    for x in [120, 420, 740, 1050]:
        draw.rectangle([(x-12, 0),(x+12, H)], fill=(20,20,20))
    for y in [80, 240, 440]:
        draw.rectangle([(0, y-10),(W, y+10)], fill=(20,20,20))
    # 3. Large red circle (Lissitzky's proun circle)
    lcirc = layer(); ImageDraw.Draw(lcirc).ellipse([(820,80),(1100,360)], fill=(200,28,28,180))
    base = comp(base, lcirc)
    # 4. White rectangle cutting through red
    lw = layer(); ImageDraw.Draw(lw).rectangle([(870,160),(1050,280)], fill=(245,240,228,240))
    base = comp(base, lw)
    # 5. Small black squares (constructivist nodes)
    for sx, sy in [(160,300),(460,480),(780,520),(1080,420),(340,160)]:
        draw.rectangle([(sx-18,sy-18),(sx+18,sy+18)], fill=(20,20,20))
    return base


def img_klee_20251213():
    """Paul Klee grid style — Claude Code in Slack / agent network theme."""
    rng2 = Random(42)
    base = Image.new("RGB", (W, H), (28, 24, 34))
    draw = ImageDraw.Draw(base)
    CELL_W, CELL_H = 80, 70
    cols_grid = W // CELL_W + 1
    rows_grid = H // CELL_H + 1
    warm_cool = [
        (220,80,40),(200,130,30),(80,180,60),(40,160,200),(120,60,180),
        (200,60,120),(240,200,40),(30,140,160),(180,80,160),(60,200,140),
        (220,160,60),(40,80,200),(200,100,80),(80,220,180),(160,40,120),
    ]
    # 1. Colour grid cells
    for row in range(rows_grid):
        for col in range(cols_grid):
            colour = warm_cool[rng2.randint(0, len(warm_cool)-1)]
            alpha = rng2.randint(140, 220)
            lc = layer()
            x0, y0 = col*CELL_W, row*CELL_H
            ImageDraw.Draw(lc).rectangle([(x0+2,y0+2),(x0+CELL_W-2,y0+CELL_H-2)], fill=colour+(alpha,))
            base = comp(base, lc)
    # 2. Dark grid lines
    for x in range(0, W, CELL_W):
        draw.line([(x,0),(x,H)], fill=(28,24,34), width=3)
    for y in range(0, H, CELL_H):
        draw.line([(0,y),(W,y)], fill=(28,24,34), width=3)
    # 3. White node circles at grid intersections (selected)
    node_positions = [(rng2.randint(1,cols_grid-1)*CELL_W, rng2.randint(1,rows_grid-1)*CELL_H) for _ in range(18)]
    for nx, ny in node_positions:
        ln = layer(); ImageDraw.Draw(ln).ellipse([(nx-10,ny-10),(nx+10,ny+10)], fill=(255,255,255,220))
        base = comp(base, ln)
    # 4. Connecting lines between nodes (agent links)
    for i in range(len(node_positions)-1):
        x0,y0 = node_positions[i]; x1,y1 = node_positions[i+1]
        ll = layer(); ImageDraw.Draw(ll).line([(x0,y0),(x1,y1)], fill=(255,255,255,80), width=2)
        base = comp(base, ll)
    return base


def img_kandinsky_20251214():
    """Wassily Kandinsky 'Composition' style — extended thinking / reasoning theme."""
    rng2 = Random(42)
    base = Image.new("RGB", (W, H), (18, 34, 72))
    draw = ImageDraw.Draw(base)
    # 1. Diagonal grid lines
    for i in range(-10, 20):
        x = i * 80
        draw.line([(x, 0),(x+H, H)], fill=(255,255,255,30), width=1)
        draw.line([(x, 0),(x-H, H)], fill=(255,255,255,30), width=1)
    # 2. Large primary circles
    for cx, cy, r, col in [
        (200, 200, 120, (220,60,40,180)),
        (700, 150, 90, (40,140,220,160)),
        (1000, 380, 110, (220,180,30,170)),
        (400, 480, 75, (40,180,100,160)),
    ]:
        lc = layer(); ImageDraw.Draw(lc).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=col)
        base = comp(base, lc)
    # 3. Bold triangles (reasoning angles)
    for pts, col in [
        ([(580,80),(720,80),(650,200)], (220,60,40,200)),
        ([(900,440),(1100,440),(1000,280)], (40,140,220,200)),
        ([(60,400),(180,400),(120,550)], (220,180,30,200)),
    ]:
        lt = layer(); ImageDraw.Draw(lt).polygon(pts, fill=col)
        base = comp(base, lt)
    # 4. Black arcs (compositional rhythm)
    for cx, cy, r in [(400,300,160),(800,480,120),(150,120,80)]:
        la = layer(); ImageDraw.Draw(la).arc([(cx-r,cy-r),(cx+r,cy+r)], 30, 270, fill=(0,0,0,180), width=8)
        base = comp(base, la)
    # 5. Small accent circles (thought nodes)
    for _ in range(22):
        ax = rng2.randint(40, W-40); ay = rng2.randint(40, H-40)
        ar = rng2.randint(6, 18)
        col = rng2.choice([(220,60,40),(40,140,220),(220,180,30),(255,255,255)])
        ls = layer(); ImageDraw.Draw(ls).ellipse([(ax-ar,ay-ar),(ax+ar,ay+ar)], fill=col+(200,))
        base = comp(base, ls)
    return base


def img_balla_20251215():
    """Giacomo Balla Futurist style — enterprise partnerships / momentum theme."""
    rng2 = Random(42)
    base = Image.new("RGB", (W, H), (10, 10, 14))
    VPX, VPY = W // 2, H // 2
    # 1. Radiating coloured planes from VP
    colours = [
        (220,60,40),(240,180,30),(40,200,80),(40,120,220),(180,40,200),
        (220,120,30),(30,200,180),(200,40,100),(240,220,40),(60,160,240),
    ]
    for i, col in enumerate(colours):
        angle = i * (360 / len(colours))
        rad = math.radians(angle)
        spread = math.radians(18)
        r1 = math.radians(angle - 9)
        r2 = math.radians(angle + 9)
        ex1 = int(VPX + math.cos(r1) * 900)
        ey1 = int(VPY + math.sin(r1) * 900)
        ex2 = int(VPX + math.cos(r2) * 900)
        ey2 = int(VPY + math.sin(r2) * 900)
        lp = layer()
        ImageDraw.Draw(lp).polygon([(VPX,VPY),(ex1,ey1),(ex2,ey2)], fill=col+(160,))
        base = comp(base, lp)
    # 2. Motion lines (speed streaks)
    for _ in range(30):
        sx = rng2.randint(0, W); sy = rng2.randint(0, H)
        angle_m = math.atan2(sy - VPY, sx - VPX)
        length = rng2.randint(60, 180)
        ex = sx + int(math.cos(angle_m) * length)
        ey = sy + int(math.sin(angle_m) * length)
        col_m = rng2.choice(colours)
        lm = layer(); ImageDraw.Draw(lm).line([(sx,sy),(ex,ey)], fill=col_m+(120,), width=rng2.randint(2,5))
        base = comp(base, lm)
    # 3. Bright central burst
    for r in [80, 55, 32, 14]:
        alpha = 100 + (80 - r) * 2
        lb = layer()
        ImageDraw.Draw(lb).ellipse([(VPX-r,VPY-r),(VPX+r,VPY+r)], fill=(255,255,255,min(255,alpha)))
        base = comp(base, lb)
    # 4. Secondary velocity nodes
    for nx, ny in [(300,180),(900,200),(250,460),(960,430),(500,540)]:
        ln = layer(); ImageDraw.Draw(ln).ellipse([(nx-22,ny-22),(nx+22,ny+22)], fill=(240,200,30,180))
        base = comp(base, ln)
    return base


def img_rothko_20251216():
    """Mark Rothko Colour Field style — Dario Amodei / DealBook / AI investment depth theme."""
    base = Image.new("RGB", (W, H), (20, 12, 8))
    draw = ImageDraw.Draw(base, "RGBA")
    # 1. Three hazy colour bands (classic Rothko)
    bands = [
        (0,        0,        H//3+30,  (140, 30,  20)),    # deep burgundy top
        (H//3-30,  H//3-30,  2*H//3+30,(70,  50,  120)),   # indigo middle
        (2*H//3-30,2*H//3-30,H,        (180, 100, 20)),    # amber base
    ]
    for y0, fy0, y1, col in bands:
        lb = layer()
        ImageDraw.Draw(lb).rectangle([(0, fy0),(W, y1)], fill=col+(200,))
        base = comp(base, lb)
    # 2. Luminous soft edges (Rothko's glow)
    for cx, cy, rw, rh, col in [
        (W//2, H//3,    500, 60, (220, 60, 40, 80)),
        (W//2, 2*H//3,  480, 55, (220, 150, 30, 80)),
        (W//2, H//2,    420, 50, (150, 80, 200, 60)),
    ]:
        for spread in [1.8, 1.4, 1.0]:
            le = layer()
            rw_s = int(rw * spread); rh_s = int(rh * spread)
            alpha = int(40 / spread)
            ImageDraw.Draw(le).ellipse([(cx-rw_s, cy-rh_s),(cx+rw_s, cy+rh_s)], fill=col[:3]+(alpha,))
            base = comp(base, le)
    # 3. Fine horizontal texture lines (Rothko's brushstroke texture)
    for y in range(0, H, 6):
        alpha = 20 + (y % 40)
        draw.line([(0,y),(W,y)], fill=(255,255,255,alpha), width=1)
    # 4. Dark separating lines between bands
    for y in [H//3, 2*H//3]:
        ld = layer(); ImageDraw.Draw(ld).rectangle([(0, y-3),(W, y+3)], fill=(10,8,6,200))
        base = comp(base, ld)
    return base


def img_moholy_20251217():
    """László Moholy-Nagy Bauhaus style — structured outputs / transparency theme."""
    rng2 = Random(42)
    base = Image.new("RGB", (W, H), (248, 246, 240))
    # 1. Large overlapping translucent circles (primary colours)
    circle_specs = [
        (280, 220, 200, (220, 40,  40,  80)),
        (600, 180, 180, (30,  80,  200, 80)),
        (900, 300, 220, (220, 180, 30,  80)),
        (400, 420, 160, (30,  180, 80,  80)),
        (750, 460, 190, (180, 40,  180, 70)),
    ]
    for cx, cy, r, col in circle_specs:
        lc = layer(); ImageDraw.Draw(lc).ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill=col)
        base = comp(base, lc)
    # 2. Overlapping translucent rectangles
    rect_specs = [
        (100, 80,  550, 380, (30,  80,  200, 50)),
        (650, 150, 1150, 480,(220, 40,  40,  50)),
        (200, 350, 800,  580,(220, 180, 30,  50)),
    ]
    for x0,y0,x1,y1,col in rect_specs:
        lr = layer(); ImageDraw.Draw(lr).rectangle([(x0,y0),(x1,y1)], fill=col)
        base = comp(base, lr)
    # 3. Black structural lines (Bauhaus grid)
    draw = ImageDraw.Draw(base)
    for x in [200, 550, 900]:
        draw.line([(x,0),(x,H)], fill=(20,20,20), width=3)
    for y in [160, 340, 500]:
        draw.line([(0,y),(W,y)], fill=(20,20,20), width=3)
    # 4. Small primary accent dots
    for _ in range(20):
        ax = rng2.randint(50, W-50); ay = rng2.randint(50, H-50)
        col = rng2.choice([(220,40,40),(30,80,200),(220,180,30),(30,180,80)])
        la = layer(); ImageDraw.Draw(la).ellipse([(ax-8,ay-8),(ax+8,ay+8)], fill=col+(220,))
        base = comp(base, la)
    return base


# ── Saving logic ─────────────────────────────────────────────────────────────

DAYS = [
    ("2025-12-11", img_leger_20251211,      "MCP Standard",    "Fernand Léger"),
    ("2025-12-12", img_lissitzky_20251212,  "MCP Dev Guide",   "El Lissitzky"),
    ("2025-12-13", img_klee_20251213,       "Claude in Slack", "Paul Klee"),
    ("2025-12-14", img_kandinsky_20251214,  "Deep Reasoning",  "Wassily Kandinsky"),
    ("2025-12-15", img_balla_20251215,      "Partnerships",    "Giacomo Balla"),
    ("2025-12-16", img_rothko_20251216,     "AI Investment",   "Mark Rothko"),
    ("2025-12-17", img_moholy_20251217,     "Struct Outputs",  "László Moholy-Nagy"),
    ("2025-12-18", img_miro_20251218,       "Agent Skills",    "Joan Miró"),
    ("2025-12-19", img_delaunay_20251219,   "Chrome Tips",     "Robert Delaunay"),
    ("2025-12-20", img_calder_20251220,     "CLAUDE.md",       "Alexander Calder"),
    ("2025-12-21", img_mondrian_20251221,   "Doc Analysis",    "Piet Mondrian"),
    ("2025-12-22", img_seurat_20251222,     "Eval Pipelines",  "Georges Seurat"),
    ("2025-12-23", img_klimt_20251223,      "Copyright",       "Gustav Klimt"),
    ("2025-12-24", img_malevich_20251224,   "Prompt Library",  "Kazimir Malevich"),
    ("2025-12-25", img_franz_marc_20251225, "Science & Safety", "Franz Marc"),
    ("2025-12-26", img_klee_20251226,       "Model Migration",  "Paul Klee"),
    ("2025-12-27", img_moholy_20251227,     "Year-End Tips",    "László Moholy-Nagy"),
    ("2025-12-28", img_lissitzky_20251228,  "API Patterns",     "El Lissitzky"),
    ("2025-12-29", img_leger_20251229,      "2025 Review",      "Fernand Léger"),
    ("2025-12-30", img_balla_20251230,      "Speed & Batch",    "Giacomo Balla"),
    ("2025-12-31", img_kandinsky_20251231,  "Year in Review",   "Wassily Kandinsky"),
    ("2026-01-01", img_rothko_20260101,     "Year Review",     "Mark Rothko"),
    ("2026-01-02", img_mondrian_20260102,   "SDK Update",      "Piet Mondrian"),
    ("2026-01-03", img_klimt_20260103,      "Haiku 4.5",       "Gustav Klimt"),
    ("2026-01-04", img_miro_20260104,       "Team Projects",   "Joan Miró"),
    ("2026-01-05", img_delaunay_20260105,   "Voice Webhooks",  "Robert Delaunay"),
    ("2026-01-06", img_malevich_20260106,   "Responsible Use", "Kazimir Malevich"),
    ("2026-01-07", img_seurat_20260107,     "500B Tokens",     "Georges Seurat"),
    ("2026-01-08", img_calder_20260108,     "Azure GA",        "Alexander Calder"),
    ("2026-01-09", img_lissitzky_20260109,  "Claude Code v2",  "El Lissitzky"),
    ("2026-01-10", img_franz_marc_20260110, "Model Welfare",   "Franz Marc"),
    ("2026-01-11", img_balla_20260111,      "Cowork macOS",    "Giacomo Balla"),
    ("2026-01-12", img_moholy_20260112,     "Open Evals",      "László Moholy-Nagy"),
    ("2026-01-13", img_kandinsky_20260113,  "Thinking GA",     "Wassily Kandinsky"),
    ("2026-01-14", img_leger_20260114,      "Bedrock Infra",   "Fernand Léger"),
    ("2026-01-15", img_rothko_20260115,     "Long Context",    "Mark Rothko"),
    ("2026-01-16", img_klimt_20260116,      "Sonnet Update",   "Gustav Klimt"),
    ("2026-01-17", img_mondrian_20260117,   "Struct Outputs",  "Piet Mondrian"),
    ("2026-01-18", img_miro_20260118,       "Automations",     "Joan Miró"),
    ("2026-01-19", img_seurat_20260119,     "1M Developers",   "Georges Seurat"),
    ("2026-01-20", img_malevich_20260120,   "Injection Eval",  "Kazimir Malevich"),
    ("2026-01-21", img_delaunay_20260121,   "MCP 500",         "Robert Delaunay"),
    ("2026-01-22", img_balla_20260122,      "TTFT Speed",      "Giacomo Balla"),
    ("2026-01-23", img_klee_20260123,       "Agent Preview",   "Paul Klee"),
    ("2026-01-24", img_leger_20260124,      "Vertex GA",       "Fernand Léger"),
    ("2026-01-25", img_moholy_20260125,     "Trust Center",    "László Moholy-Nagy"),
    ("2026-01-26", img_lissitzky_20260126,  "CLAUDE.md v2",    "El Lissitzky"),
    ("2026-01-27", img_klimt_20260127,      "Character",       "Gustav Klimt"),
    ("2026-01-28", img_kandinsky_20260128,  "Budget Tokens",   "Wassily Kandinsky"),
    ("2026-01-29", img_calder_20260129,     "JetBrains Beta",  "Alexander Calder"),
    ("2026-01-30", img_seurat_20260130,     "Perf Report",     "Georges Seurat"),
    ("2026-01-31", img_franz_marc_20260131, "Safety Summary",  "Franz Marc"),
    ("2026-02-01", img_klee_20260201,        "Cowork Launch",   "Paul Klee"),
    ("2026-02-02", img_leger_20260202,       "Data Residency",  "Fernand Léger"),
    ("2026-02-03", img_mondrian_20260203,    "Haiku Sunset",    "Piet Mondrian"),
    ("2026-02-04", img_lissitzky_20260204,   "EU Expansion",    "El Lissitzky"),
    ("2026-02-05", img_klimt_20260205,       "Opus 4.6",        "Gustav Klimt"),
    ("2026-02-06", img_kandinsky_20260206,   "Agent Teams",     "Wassily Kandinsky"),
    ("2026-02-07", img_calder_20260207,      "Science AI",      "Alexander Calder"),
    ("2026-02-08", img_seurat_20260208,      "Flag Rollout",    "Georges Seurat"),
    ("2026-02-09", img_franz_marc_20260209,  "Interpretability","Franz Marc"),
    ("2026-02-10", img_balla_20260210,       "Windows Launch",  "Giacomo Balla"),
    ("2026-02-11", img_delaunay_20260211,    "Web Fetch",       "Robert Delaunay"),
    ("2026-02-12", img_mondrian_20260212,    "10K Servers",     "Piet Mondrian"),
    ("2026-02-13", img_moholy_20260213,      "Analytics API",   "László Moholy-Nagy"),
    ("2026-02-14", img_malevich_20260214,    "Safety Research", "Kazimir Malevich"),
    ("2026-02-15", img_klee_20260215,        "Risk Report",     "Paul Klee"),
    ("2026-02-16", img_kandinsky_20260216,   "Economic Model",  "Wassily Kandinsky"),
    ("2026-02-17", img_klimt_20260217,       "Sonnet 4.6",      "Gustav Klimt"),
    ("2026-02-18", img_calder_20260218,      "Opus Webinar",    "Alexander Calder"),
    ("2026-02-19", img_lissitzky_20260219,   "Model Sunset",    "El Lissitzky"),
    ("2026-02-20", img_franz_marc_20260220,  "Transparency",    "Franz Marc"),
    ("2026-02-21", img_rothko_20260221,      "Disclosure",      "Mark Rothko"),
    ("2026-02-22", img_seurat_20260222,      "Code Security",   "Georges Seurat"),
    ("2026-02-23", img_malevich_20260223,    "IP Defence",      "Kazimir Malevich"),
    ("2026-02-24", img_delaunay_20260224,    "RSP v3",          "Robert Delaunay"),
    ("2026-02-25", img_balla_20260225,       "Series G",        "Giacomo Balla"),
    ("2026-02-26", img_moholy_20260226,      "Open Letter",     "László Moholy-Nagy"),
    ("2026-02-27", img_kandinsky_20260227,   "Federal Access",  "Wassily Kandinsky"),
    ("2026-02-28", img_miro_20260228,        "Market Share",    "Joan Miró"),
    ("2026-03-01", img_klimt_20260301,       "App Store No.1",  "Gustav Klimt"),
    ("2026-03-02", img_mondrian_20260302,   "Outage & Memory", "Piet Mondrian"),
    ("2026-03-03", img_rothko_20260303,     "Governance",      "Mark Rothko"),
    ("2026-03-04", img_malevich_20260304,   "Supply Chain",    "Kazimir Malevich"),
    ("2026-03-05", img_lissitzky_20260305,  "Public Statement","El Lissitzky"),
    ("2026-03-06", img_balla_20260306,      "1M Sign-Ups",     "Giacomo Balla"),
    ("2026-03-07", img_klee_20260307,       "Whoa Moment",     "Paul Klee"),
    ("2026-03-08", img_delaunay_20260308,   "Prompt Caching",  "Robert Delaunay"),
    ("2026-03-09", img_miro_20260309,       "Lawsuit Filed",   "Joan Miró"),
    ("2026-03-10", img_franz_marc_20260310,  "APAC Expansion",  "Franz Marc"),
    ("2026-03-11", img_calder_20260311,      "Balance",         "Alexander Calder"),
    ("2026-03-12", img_rothko_20260312,      "Certification",   "Mark Rothko"),
    ("2026-03-13", img_kandinsky,  "Getting Started",  "Wassily Kandinsky"),
    ("2026-03-14", img_mondrian,   "1M Context",       "Piet Mondrian"),
    ("2026-03-15", img_futurism,   "Fast Mode",        "Giacomo Balla"),
    ("2026-03-16", img_klimt,      "Sonnet 4.6",       "Gustav Klimt"),
    ("2026-03-17", img_klee,       "Agent Teams",      "Paul Klee"),
    ("2026-03-18", img_delaunay,   "Dispatch",         "Robert Delaunay"),
    ("2026-03-19", img_miro,       "/ loop",           "Joan Miro"),
    ("2026-03-20", img_malevich,          "Security",    "Kazimir Malevich"),
    ("2026-03-21", img_seurat_20260321,   "Channels",    "Georges Seurat"),
    ("2026-03-22", img_leger_20260322,       "Policy",        "Fernand Léger"),
    ("2026-03-23", img_lissitzky_20260323,  "Computer Use",  "El Lissitzky"),
    ("2026-03-24", img_moholy_20260324,     "IPO & Court",   "László Moholy-Nagy"),
    ("2026-03-25", img_franz_marc_20260325, "Voices",        "Franz Marc"),
    ("2026-03-26", img_klee_20260326,       "Global Network", "Paul Klee"),
    ("2026-03-27", img_rothko_20260327,     "Mythos",         "Mark Rothko"),
    ("2026-03-28", img_kandinsky_20260328, "Growth Network",  "Wassily Kandinsky"),
    ("2026-03-29", img_mondrian_20260329,  "Learning Curves", "Piet Mondrian"),
]

for date, fn, kw, artist in DAYS:
    yyyy, mm, _ = date.split("-")
    out_dir = os.path.join(BASE, "articles", yyyy, mm)
    os.makedirs(out_dir, exist_ok=True)
    print(f"  Generating {date} ({artist})...")
    img = fn()
    img = add_badge(img, date, kw, artist)

    main_path  = os.path.join(out_dir, f"{date}.png")
    thumb_path = os.path.join(out_dir, f"{date}-thumb.png")

    img.save(main_path,  optimize=True)
    make_thumb(img).save(thumb_path, optimize=True)

    print(f"  OK  {date}  ->  {main_path}")
    print(f"      {date}-thumb  ->  {thumb_path}")

print(f"\nDone! All {len(DAYS) * 2} files generated.")
