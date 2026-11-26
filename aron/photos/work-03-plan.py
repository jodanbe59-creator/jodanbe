import math
W,H=400,500
P=[]   # (d, width, opacity, cls)
T=[]   # labels
def L(pts,w=1,op=1,cls='f'):
    P.append(('M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts),w,op,cls))
def R(x0,y0,x1,y1,**kw): L([(x0,y0),(x1,y0),(x1,y1),(x0,y1),(x0,y0)],**kw)
def C(cx,cy,r,a0=0,a1=360,n=36,ry=None,**kw):
    ry=ry or r; L([(cx+r*math.cos(math.radians(a0+(a1-a0)*i/n)),cy+ry*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+1)],**kw)
def wall(pts): L(pts,w=6,op=.92,cls='w')
def door(hx,hy,r,a0,a1):   # hinge at (hx,hy), leaf + swing arc
    L([(hx,hy),(hx+r*math.cos(math.radians(a1)),hy+r*math.sin(math.radians(a1)))],w=1.1,op=.85)
    C(hx,hy,r,a0,a1,n=16,w=.55,op=.55)
def lab(x,y,t,s=6.6): T.append((x,y,t,s))
X0,Y0,X1,Y1=44,58,356,444
# ── outer walls (gaps for entrance at bottom 182-222)
wall([(182,Y1),(X0,Y1),(X0,Y0),(X1,Y0),(X1,Y1),(222,Y1)])
# interior walls
wall([(X0,176),(118,176)]); wall([(144,176),(208,176)]); wall([(234,176),(252,176)])     # corridor top (door gaps)
wall([(150,Y0),(150,176)]); wall([(252,Y0),(252,190)]); wall([(252,216),(252,300)])
wall([(252,300),(286,300)]); wall([(310,300),(X1,300)])
wall([(252,330),(252,372)]); wall([(252,372),(290,372)]); wall([(314,372),(X1,372)]); wall([(252,398),(252,Y1)])
wall([(252,206),(276,206)]); wall([(300,206),(X1,206)])
# doors
door(118,176,26,180,270); door(208,176,26,180,270)          # consult 1 / 2
door(252,190,26,90,0) if False else door(252,216,26,270,360) # treatment
door(286,300,24,0,-90); door(290,372,24,0,-90)               # x-ray / restroom
door(252,372,26,90,180) if False else door(252,398,26,270,180)
L([(182,Y1),(182,Y1-28)],w=1.1,op=.85); C(182,Y1,28,-90,0,n=14,w=.55,op=.55)      # entrance double door
L([(222,Y1),(222,Y1-28)],w=1.1,op=.85); C(222,Y1,28,180,270,n=14,w=.55,op=.55)
# ── consult rooms: desk + chairs + exam bed
for x in (44,150):
    R(x+12,Y0+14,x+58,Y0+34,w=.8,op=.75); C(x+35,Y0+44,5,w=.7,op=.7); C(x+26,Y0+24,0.1,w=.1,op=0)
    C(x+24,Y0+52,4.5,w=.7,op=.6); C(x+46,Y0+52,4.5,w=.7,op=.6)
    R(x+72,Y0+12,x+96,Y0+70,w=.8,op=.75); L([(x+72,Y0+22),(x+96,Y0+22)],w=.5,op=.55)
# treatment: two beds + curtain tracks
for y in (Y0+16,Y0+78):
    R(268,y,340,y+24,w=.8,op=.75); L([(268,y),(268,y+24)],w=1.4,op=.7)
    L([(262,y-4),(346,y-4)],w=.5,op=.45); L([(262,y+30),(346,y+30)],w=.5,op=.45)
# x-ray / imaging
R(268,222,336,262,w=.8,op=.75); C(302,242,9,w=.7,op=.6); R(320,272,346,292,w=.7,op=.6)
# restroom: two wc + sinks
for x in (270,318):
    C(x+10,352,6,ry=8,w=.8,op=.75); R(x+4,334,x+16,340,w=.7,op=.7)
R(330,310,352,326,w=.7,op=.65); C(341,318,4.5,w=.6,op=.6)
# office
R(276,408,336,426,w=.8,op=.75); C(306,400,5,w=.7,op=.65)
# ── lobby / waiting: curved reception desk, sofas, round tables, plants
C(198,232,52,200,340,n=30,w=1.4,op=.85); C(198,232,38,200,340,n=30,w=.8,op=.7)
L([(149,214),(162,219)],w=1.1,op=.8); L([(247,214),(234,219)],w=1.1,op=.8)
C(198,224,4,w=.6,op=.6); C(176,226,4,w=.6,op=.6); C(220,226,4,w=.6,op=.6)
R(54,262,70,392,w=.9,op=.8); L([(62,262),(62,392)],w=.4,op=.4)        # banquette along left wall
for y in (284,322,360): L([(54,y),(70,y)],w=.45,op=.5)
C(140,346,40,180,360,n=30,w=1.2,op=.8); C(140,346,28,180,360,n=30,w=.7,op=.65)   # curved sofa
C(140,350,11,w=.8,op=.75)                                                        # round table
C(96,300,8,w=.7,op=.65); C(226,312,9,w=.6,op=.55); C(226,312,4,w=.6,op=.55)       # side table + plant
C(64,420,9,w=.6,op=.55); C(64,420,4,w=.5,op=.5)
# floor zoning hint (ripple rings under the lounge — ARON water motif)
for r in (52,66): C(140,350,r,205,335,n=30,w=.4,op=.3)
# ── dimension line (top) + ticks
L([(X0,40),(X1,40)],w=.5,op=.6); L([(X0,35),(X0,45)],w=.5,op=.6); L([(X1,35),(X1,45)],w=.5,op=.6)
for x in (150,252): L([(x,37),(x,43)],w=.5,op=.6)
lab(97,35,'4,200',6); lab(201,35,'4,200',6); lab(304,35,'4,000',6)
# side dimension
L([(372,Y0),(372,Y1)],w=.5,op=.6); L([(367,Y0),(377,Y0)],w=.5,op=.6); L([(367,Y1),(377,Y1)],w=.5,op=.6)
# north arrow + scale bar
C(30,470,9,w=.6,op=.7); L([(30,480),(30,458)],w=.8,op=.8); L([(26,464),(30,458),(34,464)],w=.8,op=.8)
L([(300,470),(356,470)],w=.6,op=.7)
for i,x in enumerate((300,314,328,342,356)): L([(x,466),(x,474 if i%2==0 else 471)],w=.5,op=.7)
lab(328,482,'0     1     2     3     4 m',5)
# labels
for x,y,t in [(97,150,'CONSULT 01'),(201,150,'CONSULT 02'),(304,176,'TREATMENT'),(302,282,'IMAGING'),(304,364,'RESTROOM'),(306,438,'OFFICE'),(198,208,'RECEPTION'),(150,410,'WAITING'),(202,436,'ENTRANCE'),(150,193,'CORRIDOR')]:
    lab(x,y,t)
lab(200,482,'ARON  ·  CLINIC FLOOR PLAN  ·  1:100',6.4)
paths=''.join(f'<path class="{c}" d="{d}" stroke-width="{w}" stroke-opacity="{op}" pathLength="1" style="--i:{i}"/>' for i,(d,w,op,c) in enumerate(P))
texts=''.join(f'<text x="{x}" y="{y}" font-size="{s}" text-anchor="middle">{t}</text>' for x,y,t,s in T)
grid=''.join(f'<path d="M{x} 0V{H}"/>' for x in range(0,W+1,20))+''.join(f'<path d="M0 {y}H{W}"/>' for y in range(0,H+1,20))
svg=f'''<svg class="sketch plan" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Clinic interior floor plan">
<rect width="{W}" height="{H}" fill="#f4f2ed"/><g stroke="#2f2d2a" stroke-opacity=".05" stroke-width=".5">{grid}</g>
<g fill="none" stroke="#2a2826" stroke-linecap="square" stroke-linejoin="miter">{paths}</g>
<g class="plan-t" fill="#5d5952" font-family="Jost, Inter, sans-serif" letter-spacing="1.2">{texts}</g></svg>'''
open('/tmp/claude-0/-home-user-jodanbe/915969be-0688-537e-bd34-9584e58873ca/scratchpad/plan.svg','w').write(svg); print(len(P))
