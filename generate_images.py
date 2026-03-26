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


# ── Saving logic ─────────────────────────────────────────────────────────────

DAYS = [
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
