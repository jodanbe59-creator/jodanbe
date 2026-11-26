import math, random
random.seed(11)
W,H=400,500; VPX,VPY=200,212; F=286; CAM=1.5
def P(X,Y,Z): return (VPX+X*F/Z, VPY+(CAM-Y)*F/Z)
paths=[]
def jit(pts,amt=.6,step=5):
    out=[]
    for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
        n=max(1,int(math.hypot(x2-x1,y2-y1)/step))
        for i in range(n):
            t=i/n; out.append((x1+(x2-x1)*t+random.uniform(-amt,amt),y1+(y2-y1)*t+random.uniform(-amt,amt)))
    out.append(pts[-1]); return out
def L2(pts,w=.9,op=.8,passes=2,amt=.55,over=2.5):
    for k in range(passes):
        p=list(pts)
        if over and len(p)==2:
            (x1,y1),(x2,y2)=p; d=math.hypot(x2-x1,y2-y1) or 1; ux,uy=(x2-x1)/d,(y2-y1)/d
            p=[(x1-ux*random.uniform(0,over),y1-uy*random.uniform(0,over)),(x2+ux*random.uniform(0,over),y2+uy*random.uniform(0,over))]
        q=jit(p,amt)
        paths.append(('M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in q),round(w*random.uniform(.85,1.12),2),round(op*random.uniform(.78,1),2)))
def L3(a,b,**kw): L2([P(*a),P(*b)],**kw)
def poly3(pts,close=True,**kw):
    for a,b in zip(pts,pts[1:]+([pts[0]] if close else [])): L3(a,b,**kw)
def box(x0,x1,y0,y1,z0,z1,**kw):
    c=[(x,y,z) for x in (x0,x1) for y in (y0,y1) for z in (z0,z1)]
    edges=[(0,1),(2,3),(4,5),(6,7),(0,2),(1,3),(4,6),(5,7),(0,4),(1,5),(2,6),(3,7)]
    # skip hidden back-bottom edges roughly: draw all but the far-bottom-left/right when occluded is overkill; draw all lightly
    for i,j in edges: L3(c[i],c[j],**kw)
def ell3(cx,cy,cz,r,plane='ceil',n=36,**kw):
    pts=[]
    for i in range(n+1):
        a=2*math.pi*i/n
        pts.append(P(cx+r*math.cos(a),cy,cz+r*math.sin(a)) if plane in('ceil','floor') else P(cx+r*math.cos(a),cy+r*math.sin(a),cz))
    L2(pts,over=0,**kw)
def hatch2(region,x0,x1,y0,y1,gap=3.4,ang=-35,w=.42,op=.32):
    a=math.radians(ang); dx,dy=math.cos(a),math.sin(a); cy=(y0+y1)/2
    for c in range(int(x0-(y1-y0)*2),int(x1+(y1-y0)*2),1):
        if (c%int(gap)): continue
        seg=None
        for t in range(-600,600,2):
            x=c+dx*t; y=cy+dy*t; ok=x0<=x<=x1 and y0<=y<=y1 and region(x,y)
            if ok and seg is None: seg=[(x,y)]
            elif not ok and seg is not None:
                seg.append((x,y))
                if math.hypot(seg[1][0]-seg[0][0],seg[1][1]-seg[0][1])>2.5: L2(seg,w=w,op=op,passes=1,amt=.3,over=0)
                seg=None
RW,RH,ZB=2.2,3.2,9.0
# room edges
for X in (-RW,RW):
    for Y in (0,RH): L3((X,Y,1.15),(X,Y,ZB),w=1.05)
poly3([(-RW,0,ZB),(RW,0,ZB),(RW,RH,ZB),(-RW,RH,ZB)],w=1.05)
# ceiling cove + downlights
L3((-RW+.15,RH,ZB-.05),(RW-.15,RH,ZB-.05),w=.5,op=.45,passes=1)
for z in (3.0,4.8,6.6):
    for x in (-1.0,1.0): ell3(x,RH,z,.13,w=.6,op=.55,passes=1)
# floor tiles
for x in (-1.1,0,1.1): L3((x,0,1.3),(x,0,ZB),w=.4,op=.28,passes=1,over=0)
for z in (2.2,3.0,4.0,5.2,6.6,8.0): L3((-RW,0,z),(RW,0,z),w=.4,op=.26,passes=1,over=0)
# back wall sign plate (blank) + light strip
poly3([(-.75,2.15,ZB),(.75,2.15,ZB),(.75,2.55,ZB),(-.75,2.55,ZB)],w=.8,op=.7)
L3((-.6,2.35,ZB),(.6,2.35,ZB),w=.45,op=.4,passes=1,over=0)
# reception desk: lower front counter + raised transaction ledge
box(-1.35,1.35,0,0.78,7.4,8.1,w=1.05)
box(-1.35,1.35,0.78,1.08,7.75,8.1,w=1.0)
L3((-1.35,0.12,7.4),(1.35,0.12,7.4),w=.5,op=.45,passes=1,over=0)       # kick light line
# monitors behind ledge
for x in (-.75,.45):
    poly3([(x,1.1,8.25),(x+.38,1.1,8.25),(x+.38,1.36,8.25),(x,1.36,8.25)],w=.7,op=.65)
# shadow under desk
a,b=P(-1.35,0,7.4),P(1.35,0,7.4); hatch2(lambda x,y:True,a[0],b[0],a[1]-3,a[1]+5,gap=3,ang=-25)
# left wall: two consultation room doors with plates + handles
for z0 in (3.3,5.6):
    z1=z0+1.0
    poly3([(-RW,0,z0),(-RW,2.15,z0),(-RW,2.15,z1),(-RW,0,z1)],close=False,w=1)
    L3((-RW,2.15,z0),(-RW,2.15,z1),w=1)
    L3((-RW,1.0,z1-.12),(-RW,1.0,z1-.28),w=1.1,op=.9,passes=1,over=0)              # handle
    poly3([(-RW,1.55,z0+.25),(-RW,1.55,z0+.65),(-RW,1.72,z0+.65),(-RW,1.72,z0+.25)],w=.6,op=.6)   # room plate
    p1,p2,p3=P(-RW,0,z0),P(-RW,2.15,z0),P(-RW,2.15,z0+.08)
# light strip along left wall
L3((-RW,2.6,2.0),(-RW,2.6,ZB),w=.5,op=.4,passes=1,over=0)
# right wall: row of waiting chairs (seat box + back panel)
for z in (2.9,3.6,4.3):
    box(1.45,2.05,0.42,0.5,z,z+.6,w=.9)
    box(1.95,2.05,0.5,0.92,z,z+.6,w=.9)
    for zz in (z+.06,z+.54): L3((1.5,0,zz),(1.5,.42,zz),w=.7,op=.75,passes=1)
    a,b=P(1.45,0,z),P(2.05,0,z+.6)
    hatch2(lambda x,y:True,min(a[0],b[0]),max(a[0],b[0]),min(a[1],b[1]),max(a[1],b[1])+2,gap=3,ang=-40,w=.38,op=.28)
# potted plant front-left
px,pz=-1.75,2.5
ell3(px,0.5,pz,.22,plane='floor',w=.9); L3((px-.22,.5,pz),(px-.18,0,pz),w=.9); L3((px+.22,.5,pz),(px+.18,0,pz),w=.9)
ell3(px,0.0,pz,.18,plane='floor',w=.5,op=.5,passes=1)
for i in range(9):
    ang=math.radians(-150+i*15); ln=random.uniform(.55,.9)
    base=P(px,.5,pz); tip=P(px+math.cos(ang)*ln*.5, .5+abs(math.sin(ang))*ln+.3, pz)
    mid=((base[0]+tip[0])/2+random.uniform(-4,4),(base[1]+tip[1])/2-6)
    L2([base,mid,tip],w=.7,op=.7,passes=1,over=0)
# wall shading hatch on left wall far part
hatch2(lambda x,y: True, 0, P(-RW,0,ZB)[0]-2, P(-RW,RH,4.0)[1], P(-RW,0,4.0)[1], gap=6, ang=-62, w=.35, op=.13)
out=[f'<path d="{d}" stroke-width="{w}" stroke-opacity="{op}" pathLength="1" style="--i:{i}"/>' for i,(d,w,op) in enumerate(paths)]
svg=f'''<svg class="sketch" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Pencil sketch of a clinic lobby">
<defs><filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 .2  0 0 0 0 .18  0 0 0 0 .16  0 0 0 .07 0"/></filter>
<filter id="graphite"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="9" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="0.9"/></filter></defs>
<rect width="{W}" height="{H}" fill="#f3f0e9"/><rect width="{W}" height="{H}" filter="url(#paper)"/>
<g fill="none" stroke="#2f2d2a" stroke-linecap="round" stroke-linejoin="round" filter="url(#graphite)">{''.join(out)}</g></svg>'''
open('/tmp/claude-0/-home-user-jodanbe/915969be-0688-537e-bd34-9584e58873ca/scratchpad/sketch.svg','w').write(svg); print(len(paths))
