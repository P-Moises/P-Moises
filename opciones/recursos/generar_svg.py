# Genera los SVG animados de las opciones de portada (P-Moises/P-Moises, carpeta opciones/recursos).
# Solo CSS dentro del SVG (GitHub no ejecuta JavaScript en imágenes). Fuentes del sistema.
import os, sys

OUT = sys.argv[1]
SANS = "'Segoe UI Variable Display','Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Helvetica,sans-serif"
MONO = "ui-monospace,'Cascadia Mono',Consolas,'SFMono-Regular',Menlo,monospace"
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',Georgia,serif"
EASE_OUT = "cubic-bezier(0.23,1,0.32,1)"
EASE_IO = "cubic-bezier(0.77,0,0.175,1)"


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg.strip() + "\n")


def typing(x, y, size, phrases, color, bg, cursor, prefix="", prefix_color=None, cycle=12.0):
    """Frases que se escriben letra por letra y rotan. Devuelve (css, svg)."""
    n = len(phrases)
    win = cycle / n
    type_t = 1.4
    p_type = type_t / cycle * 100
    p_hold = (win - 0.35) / cycle * 100
    p_out = win / cycle * 100
    cw = size * 0.62
    px = 0
    pre = ""
    if prefix:
        pre = f'<text x="{x}" y="{y}" class="ty" fill="{prefix_color or cursor}">{prefix}</text>'
        px = len(prefix) * cw
    css = f"""
.ty{{font-family:{MONO};font-size:{size}px}}
.ph{{opacity:0;animation:ph {cycle}s linear infinite}}
@keyframes ph{{0%{{opacity:1}}{p_hold:.2f}%{{opacity:1}}{p_out:.2f}%{{opacity:0}}100%{{opacity:0}}}}
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
"""
    body = [pre]
    for i, ph in enumerate(phrases):
        dist = len(ph) * cw + 8
        delay = 0 if i == 0 else -(cycle - win * i)
        css += f""".cv{i}{{animation:cv{i} {cycle}s infinite;animation-delay:{delay}s}}
@keyframes cv{i}{{0%{{transform:translateX(0);animation-timing-function:steps({len(ph)},end)}}{p_type:.2f}%{{transform:translateX({dist:.1f}px)}}100%{{transform:translateX({dist:.1f}px)}}}}
"""
        tx = x + px
        body.append(
            f'<g class="ph ph{i}" style="animation-delay:{delay}s">'
            f'<text x="{tx}" y="{y}" class="ty" fill="{color}">{ph}</text>'
            f'<g class="cv{i}"><rect x="{tx}" y="{y - size}" width="{dist + 40:.0f}" height="{size * 1.4:.0f}" fill="{bg}"/>'
            f'<rect class="cur" x="{tx + 1}" y="{y - size * 0.82:.1f}" width="{size * 0.5:.1f}" height="{size * 0.95:.1f}" fill="{cursor}"/></g>'
            f"</g>"
        )
    css += f"""@media (prefers-reduced-motion:reduce){{.ph{{animation:none}}.ph0{{opacity:1}}
{''.join(f'.cv{i}{{animation:none;transform:translateX(2000px)}}' for i in range(n))}}}
"""
    return css, "\n".join(body)


# ---------------------------------------------------------------- Opción 2: Estudio (oscuro + lima)
INK2, BONE2, MUTE2, LIME = "#0F100D", "#EDEBE4", "#8C8A82", "#C6F432"
t_css, t_svg = typing(56, 232, 22, ["Analista de negocio", "Diseñador de productos", "Del problema al producto probado"],
                      BONE2, INK2, LIME, prefix="> ", prefix_color=LIME)
save("estudio-encabezado.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="320" viewBox="0 0 900 320" role="img" aria-labelledby="t">
<title id="t">Moisés — Analista de negocio y diseñador de productos</title>
<defs>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{BONE2}" opacity="0.08"/></pattern>
<clipPath id="card"><rect width="900" height="320" rx="18"/></clipPath>
</defs>
<style>
.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
.rise{{animation:rise .7s {EASE_OUT} both}}
.d1{{animation-delay:.08s}} .d2{{animation-delay:.16s}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
.orb{{transform-box:view-box;transform-origin:760px 160px;animation:spin linear infinite}}
.o1{{animation-duration:16s}} .o2{{animation-duration:28s;animation-direction:reverse}} .o3{{animation-duration:44s}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2.8s {EASE_OUT} infinite}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.6}}100%{{transform:scale(3.2);opacity:0}}}}
{t_css}
@media (prefers-reduced-motion:reduce){{.rise,.orb,.pulse{{animation:none}}}}
</style>
<g clip-path="url(#card)">
<rect width="900" height="320" fill="{INK2}"/>
<rect width="900" height="320" fill="url(#dots)"/>
<text x="56" y="66" class="mono rise" font-size="13" letter-spacing="2" fill="{MUTE2}">P-MOISES  /  BOLIVIA</text>
<text x="50" y="172" class="sans rise d1" font-size="96" font-weight="700" letter-spacing="-2" fill="{BONE2}">Moisés</text>
<g class="rise d2">{t_svg}</g>
<line x1="56" y1="268" x2="520" y2="268" stroke="{BONE2}" stroke-opacity="0.12"/>
<text x="56" y="292" class="mono" font-size="12" letter-spacing="1.5" fill="{MUTE2}">ANÁLISIS · PRODUCTO · UX/UI · PRUEBAS EN DISPOSITIVO REAL</text>
<g fill="none" stroke="{BONE2}" stroke-opacity="0.16">
<circle cx="760" cy="160" r="42"/><circle cx="760" cy="160" r="78" stroke-dasharray="2 6"/><circle cx="760" cy="160" r="114"/>
</g>
<g class="orb o1"><circle cx="802" cy="160" r="4" fill="{BONE2}"/></g>
<g class="orb o2"><circle cx="760" cy="82" r="5" fill="{LIME}"/></g>
<g class="orb o3"><circle cx="646" cy="160" r="3.5" fill="{BONE2}" opacity="0.7"/><circle cx="874" cy="160" r="3" fill="{MUTE2}"/></g>
<circle class="pulse" cx="760" cy="160" r="7" fill="{LIME}"/>
<circle cx="760" cy="160" r="7" fill="{LIME}"/>
<text x="760" y="300" text-anchor="middle" class="mono" font-size="11" letter-spacing="3" fill="{MUTE2}">MULTIVERSO</text>
</g>
</svg>""")

STEPS = [("Entender", "el problema"), ("Estudiar la", "competencia"), ("Diseñar", "la experiencia"),
         ("Construir", "el producto"), ("Probar en un", "celular real")]


def node_kf(name, p_on, prop_off, prop_on):
    return (f"@keyframes {name}{{0%{{{prop_off}}}{max(p_on - 0.5, 0):.2f}%{{{prop_off}}}{p_on:.2f}%{{{prop_on}}}"
            f"92%{{{prop_on}}}97%{{{prop_off}}}100%{{{prop_off}}}}}")


# Proceso, opción 2: línea que avanza y enciende cada paso
cyc, run = 9.0, 6.0
x0, x1, y = 90, 810, 64
css_nodes, nodes = "", ""
for i, (a, b) in enumerate(STEPS):
    cx = x0 + (x1 - x0) * i / 4
    p_on = run * i / 4 / cyc * 100
    css_nodes += f".n{i}{{animation:n{i} {cyc}s infinite}}" + node_kf(f"n{i}", p_on, "fill:" + INK2, "fill:" + LIME) + "\n"
    nodes += (f'<circle class="n{i}" cx="{cx}" cy="{y}" r="7" fill="{INK2}" stroke="{LIME}" stroke-width="2"/>'
              f'<text x="{cx}" y="{y + 40}" text-anchor="middle" class="mono" font-size="12" fill="{LIME}">0{i + 1}</text>'
              f'<text x="{cx}" y="{y + 64}" text-anchor="middle" class="sans" font-size="15" fill="{BONE2}">{a}</text>'
              f'<text x="{cx}" y="{y + 84}" text-anchor="middle" class="sans" font-size="15" fill="{MUTE2}">{b}</text>')
p_run = run / cyc * 100
save("estudio-proceso.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="180" viewBox="0 0 900 180" role="img" aria-labelledby="t">
<title id="t">Cómo trabajo: entender el problema, estudiar la competencia, diseñar, construir y probar en un celular real</title>
<style>
.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
.bar{{transform-box:view-box;transform-origin:{x0}px {y}px;animation:bar {cyc}s infinite}}
@keyframes bar{{0%{{transform:scaleX(0);animation-timing-function:{EASE_IO}}}{p_run:.2f}%{{transform:scaleX(1)}}92%{{transform:scaleX(1);opacity:1}}97%{{opacity:0}}100%{{transform:scaleX(0);opacity:0}}}}
{css_nodes}
@media (prefers-reduced-motion:reduce){{.bar{{animation:none}}{''.join(f'.n{i}{{animation:none;fill:{LIME}}}' for i in range(5))}}}
</style>
<rect width="900" height="180" rx="18" fill="{INK2}"/>
<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{BONE2}" stroke-opacity="0.14" stroke-width="2"/>
<line class="bar" x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{LIME}" stroke-width="2"/>
{nodes}
</svg>""")

# ---------------------------------------------------------------- Opción 3: Editorial (papel + terracota)
PAPER, INK3, MUTE3, TERRA = "#F3EEE4", "#1D1B18", "#7A746B", "#B8492A"
lines = ["Analizo el negocio.", "Diseño el producto.", "Lo pruebo en un celular real."]
cyc3 = 9.0
u_css, u_svg = "", ""
for i, txt in enumerate(lines):
    yy = 214 + i * 38
    w = len(txt) * 24 * 0.435
    s = (0.3 + i * 0.9) / cyc3 * 100
    e = s + 0.8 / cyc3 * 100
    u_css += (f".u{i}{{transform-box:fill-box;transform-origin:left center;animation:u{i} {cyc3}s infinite}}"
              f"@keyframes u{i}{{0%{{transform:scaleX(0)}}{s:.2f}%{{transform:scaleX(0);animation-timing-function:{EASE_OUT}}}"
              f"{e:.2f}%{{transform:scaleX(1)}}88%{{transform:scaleX(1);opacity:1}}96%{{opacity:0}}100%{{transform:scaleX(0);opacity:0}}}}\n")
    u_svg += (f'<rect class="u{i}" x="58" y="{yy + 6}" width="{w:.0f}" height="3" fill="{TERRA}"/>'
              f'<text x="58" y="{yy}" class="serif" font-size="24" fill="{INK3}">{txt}</text>')
save("editorial-encabezado.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="340" viewBox="0 0 900 340" role="img" aria-labelledby="t">
<title id="t">Moisés — Analizo el negocio. Diseño el producto. Lo pruebo en un celular real.</title>
<defs><path id="ring" d="M760,170 m-84,0 a84,84 0 1,1 168,0 a84,84 0 1,1 -168,0"/></defs>
<style>
.sans{{font-family:{SANS}}} .serif{{font-family:{SERIF}}}
.seal{{transform-box:view-box;transform-origin:760px 170px;animation:spin 36s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.rise{{animation:rise .7s {EASE_OUT} both}}
@keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
{u_css}
@media (prefers-reduced-motion:reduce){{.seal,.rise{{animation:none}}{''.join(f'.u{i}{{animation:none}}' for i in range(3))}}}
</style>
<rect x="0.5" y="0.5" width="899" height="339" rx="18" fill="{PAPER}" stroke="{INK3}" stroke-opacity="0.12"/>
<text x="58" y="60" class="sans" font-size="12" letter-spacing="3" fill="{MUTE3}">PERFIL PROFESIONAL  —  BOLIVIA</text>
<line x1="58" y1="76" x2="560" y2="76" stroke="{INK3}" stroke-opacity="0.2"/>
<text x="52" y="160" class="serif rise" font-size="100" letter-spacing="-2" fill="{INK3}">Moisés</text>
{u_svg}
<g class="seal"><text class="sans" font-size="12.5" letter-spacing="3.2" fill="{INK3}"><textPath href="#ring" textLength="522" lengthAdjust="spacing">ANALISTA DE NEGOCIO · DISEÑADOR DE PRODUCTOS · </textPath></text></g>
<circle cx="760" cy="170" r="62" fill="none" stroke="{INK3}" stroke-opacity="0.25"/>
<text x="760" y="192" text-anchor="middle" class="serif" font-size="64" font-style="italic" fill="{TERRA}">M</text>
</svg>""")

# Proceso, opción 3: marcador que salta de paso en paso
cyc3p = 10.0
xs = [58 + i * 168 for i in range(5)]
hold = cyc3p / 5
kf = []
for i, xx in enumerate(xs):
    a = i * hold / cyc3p * 100
    b = a + (hold - 0.6) / cyc3p * 100
    kf.append(f"{a:.2f}%{{transform:translateX({xx - 58}px)}}{b:.2f}%{{transform:translateX({xx - 58}px);animation-timing-function:{EASE_IO}}}")
kf.append("100%{transform:translateX(0)}")
items = ""
for i, ((a, b), xx) in enumerate(zip(STEPS, xs)):
    items += (f'<text x="{xx}" y="58" class="serif" font-size="30" font-style="italic" fill="{TERRA}">0{i + 1}</text>'
              f'<text x="{xx}" y="112" class="sans" font-size="15" font-weight="600" fill="{INK3}">{a}</text>'
              f'<text x="{xx}" y="132" class="sans" font-size="15" fill="{MUTE3}">{b}</text>')
save("editorial-proceso.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="170" viewBox="0 0 900 170" role="img" aria-labelledby="t">
<title id="t">Cómo trabajo: entender el problema, estudiar la competencia, diseñar, construir y probar en un celular real</title>
<style>
.sans{{font-family:{SANS}}} .serif{{font-family:{SERIF}}}
.mk{{animation:mk {cyc3p}s infinite}}
@keyframes mk{{{''.join(kf)}}}
@media (prefers-reduced-motion:reduce){{.mk{{animation:none}}}}
</style>
<rect x="0.5" y="0.5" width="899" height="169" rx="18" fill="{PAPER}" stroke="{INK3}" stroke-opacity="0.12"/>
<line x1="58" y1="80" x2="842" y2="80" stroke="{INK3}" stroke-opacity="0.2"/>
<rect class="mk" x="58" y="78" width="132" height="4" fill="{TERRA}"/>
{items}
</svg>""")

# ---------------------------------------------------------------- Opción 4: Plano técnico (azul plano + ámbar)
NAVY, LINE, WHITE, AMBER, MUTE4 = "#0C1A2A", "#7FB8DE", "#E8F1F8", "#F2B134", "#6F8BA3"
t4_css, t4_svg = typing(60, 236, 18, ["levantando requisitos", "diseñando el flujo", "probando en un celular real"],
                        WHITE, NAVY, AMBER, prefix="$ ", prefix_color=AMBER)
rows = [("PROYECTO", "Perfil profesional"), ("AUTOR", "Moisés (P-Moises)"), ("LUGAR", "Bolivia"),
        ("ESTADO", "Construyendo Multiverso")]
tb = ""
for i, (k, v) in enumerate(rows):
    yy = 196 + i * 26
    tb += (f'<text x="572" y="{yy + 17}" class="mono" font-size="11" letter-spacing="1" fill="{MUTE4}">{k}</text>'
           f'<text x="664" y="{yy + 17}" class="mono" font-size="13" fill="{WHITE}">{v}</text>')
    if i:
        tb += f'<line x1="560" y1="{yy}" x2="860" y2="{yy}" stroke="{LINE}" stroke-opacity="0.35"/>'
save("plano-encabezado.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="340" viewBox="0 0 900 340" role="img" aria-labelledby="t">
<title id="t">Moisés — Analista de negocio y diseñador de productos. Bolivia.</title>
<defs>
<pattern id="g1" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{LINE}" stroke-opacity="0.06"/></pattern>
<pattern id="g2" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M100 0H0V100" fill="none" stroke="{LINE}" stroke-opacity="0.12"/></pattern>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LINE}" stop-opacity="0"/><stop offset="1" stop-color="{LINE}" stop-opacity="0.18"/></linearGradient>
<clipPath id="card"><rect width="900" height="340" rx="14"/></clipPath>
</defs>
<style>
.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
.draw{{stroke-dasharray:400;stroke-dashoffset:400;animation:draw 1.2s {EASE_OUT} .2s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.scan{{animation:scan 7s linear infinite}}
@keyframes scan{{from{{transform:translateY(-80px)}}to{{transform:translateY(340px)}}}}
.ring{{transform-box:view-box;transform-origin:710px 100px;animation:spin 20s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.ping{{animation:ping 2.4s steps(1) infinite}}
@keyframes ping{{50%{{opacity:.25}}}}
{t4_css}
@media (prefers-reduced-motion:reduce){{.scan,.ring,.ping{{animation:none}}.draw{{animation:none;stroke-dashoffset:0}}}}
</style>
<g clip-path="url(#card)">
<rect width="900" height="340" fill="{NAVY}"/>
<rect width="900" height="340" fill="url(#g1)"/><rect width="900" height="340" fill="url(#g2)"/>
<rect class="scan" x="0" y="0" width="900" height="80" fill="url(#scan)"/>
<rect x="20" y="20" width="860" height="300" fill="none" stroke="{LINE}" stroke-opacity="0.4"/>
<text x="60" y="64" class="mono" font-size="12" letter-spacing="2" fill="{MUTE4}">HOJA 01 / 01  ·  ESCALA 1:1</text>
<text x="56" y="150" class="sans" font-size="80" font-weight="600" letter-spacing="3" fill="{WHITE}">MOISÉS</text>
<g stroke="{AMBER}" stroke-width="1.2" fill="none">
<path class="draw" d="M60 172V186M60 179H420M420 172V186"/>
</g>
<text x="60" y="204" class="mono" font-size="12" letter-spacing="1" fill="{AMBER}">ANALISTA DE NEGOCIO + DISEÑADOR DE PRODUCTOS</text>
{t4_svg}
<g fill="none" stroke="{LINE}">
<circle cx="710" cy="100" r="44" stroke-opacity="0.5"/>
<circle class="ring" cx="710" cy="100" r="58" stroke-opacity="0.6" stroke-dasharray="4 8"/>
<path d="M650 100H770M710 40V160" stroke-opacity="0.35"/>
</g>
<circle class="ping" cx="710" cy="100" r="5" fill="{AMBER}"/>
<rect x="560" y="196" width="300" height="104" fill="{NAVY}" stroke="{LINE}" stroke-opacity="0.6"/>
<line x1="652" y1="196" x2="652" y2="300" stroke="{LINE}" stroke-opacity="0.35"/>
{tb}
</g>
</svg>""")

# Proceso, opción 4: cajas conectadas con flujo continuo y foco ámbar que recorre
cyc4 = 7.5
bw, gap, by = 140, 30, 40
xs4 = [25 + i * (bw + gap) for i in range(5)]
boxes, css4 = "", ""
for i, ((a, b), xx) in enumerate(zip(STEPS, xs4)):
    s = i / 5 * 100
    e = (i + 1) / 5 * 100
    css4 += (f".h{i}{{animation:h{i} {cyc4}s infinite}}@keyframes h{i}{{0%{{opacity:0}}{s:.2f}%{{opacity:0}}"
             f"{s + 2:.2f}%{{opacity:1}}{e - 2:.2f}%{{opacity:1}}{e:.2f}%{{opacity:0}}100%{{opacity:0}}}}\n")
    boxes += (f'<rect x="{xx}" y="{by}" width="{bw}" height="96" rx="4" fill="{NAVY}" stroke="{LINE}" stroke-opacity="0.55"/>'
              f'<rect class="h{i}" x="{xx}" y="{by}" width="{bw}" height="96" rx="4" fill="none" stroke="{AMBER}" stroke-width="1.5"/>'
              f'<text x="{xx + 14}" y="{by + 26}" class="mono" font-size="11" letter-spacing="1" fill="{AMBER}">PASO 0{i + 1}</text>'
              f'<text x="{xx + 14}" y="{by + 58}" class="sans" font-size="15" fill="{WHITE}">{a}</text>'
              f'<text x="{xx + 14}" y="{by + 78}" class="sans" font-size="15" fill="{MUTE4}">{b}</text>')
    if i < 4:
        boxes += f'<path class="flow" d="M{xx + bw} {by + 48}H{xx + bw + gap}" stroke="{LINE}" stroke-width="1.5" stroke-dasharray="4 4"/>'
save("plano-proceso.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="176" viewBox="0 0 900 176" role="img" aria-labelledby="t">
<title id="t">Cómo trabajo: entender el problema, estudiar la competencia, diseñar, construir y probar en un celular real</title>
<defs><pattern id="g1" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{LINE}" stroke-opacity="0.06"/></pattern></defs>
<style>
.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
.flow{{animation:flow .8s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-8}}}}
{css4}
@media (prefers-reduced-motion:reduce){{.flow{{animation:none}}{''.join(f'.h{i}{{animation:none;opacity:0}}' for i in range(5))}}}
</style>
<rect width="900" height="176" rx="14" fill="{NAVY}"/>
<rect width="900" height="176" rx="14" fill="url(#g1)"/>
{boxes}
</svg>""")
print("ok")
