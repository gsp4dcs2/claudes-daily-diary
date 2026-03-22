import math
import os
from random import Random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = r"D:\Tresorit\z_Keepass\GSP\AI\Claude\ws02_Claudes_Daily_Diary"
OUT  = os.path.join(BASE, "archives", "2026", "03")
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


# ── Saving logic ─────────────────────────────────────────────────────────────

DAYS = [
    ("2026-03-13", img_kandinsky,  "Getting Started",  "Wassily Kandinsky"),
    ("2026-03-14", img_mondrian,   "1M Context",       "Piet Mondrian"),
    ("2026-03-15", img_futurism,   "Fast Mode",        "Giacomo Balla"),
    ("2026-03-16", img_klimt,      "Sonnet 4.6",       "Gustav Klimt"),
    ("2026-03-17", img_klee,       "Agent Teams",      "Paul Klee"),
    ("2026-03-18", img_delaunay,   "Dispatch",         "Robert Delaunay"),
    ("2026-03-19", img_miro,       "/ loop",           "Joan Miro"),
    ("2026-03-20", img_malevich,          "Security",    "Kazimir Malevich"),
    ("2026-03-21", img_seurat_20260321,   "Channels",    "Georges Seurat"),
    ("2026-03-22", img_leger_20260322,    "Policy",      "Fernand Léger"),
]

os.makedirs(OUT, exist_ok=True)

for date, fn, kw, artist in DAYS:
    print(f"  Generating {date} ({artist})...")
    img = fn()
    img = add_badge(img, date, kw, artist)

    main_path  = os.path.join(OUT, f"{date}.png")
    thumb_path = os.path.join(OUT, f"{date}-thumb.png")

    img.save(main_path,  optimize=True)
    make_thumb(img).save(thumb_path, optimize=True)

    print(f"  OK  {date}  ->  {main_path}")
    print(f"      {date}-thumb  ->  {thumb_path}")

print("\nDone! All 16 files generated.")
