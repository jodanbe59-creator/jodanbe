import math, sys, os
TRACED=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'traced-r-path.txt')).read()
T,B=40,240; H=B-T
def P(pts): return 'M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in pts)+' Z'
def stroke(xt,xb,wt,wb):
    # a straight stroke from top centre xt to bottom centre xb, width wt at the top and wb at the bottom (horizontal widths)
    return [(xt-wt/2,T),(xt+wt/2,T),(xb+wb/2,B),(xb-wb/2,B)]
def letters(t1,t2,k,ko=None,desk=None):
    ko=ko or k
    # k = how much heavier the bottom is (1 = even)
    L={}
    # A: apex at 102, feet at 20 / 184
    # A gets heavier toward the TOP: wide near the apex, fine at the feet
    L['A']=P(stroke(100,20,t1*k*1.1,t1*0.55))+' '+P(stroke(104,184,t2*k*1.2,t2*0.55))
    # R: thin top bar + bowl + middle bar (stroke), leg widening to a flat foot
    x0,xb,r=230,300,50
    L['Rs']=f'M{x0} {T+t1/2} H{xb} A{r-t1/2} {r-t1/2} 0 0 1 {xb} {T+2*r-t1/2} H{x0+44}'
    jy=T+2*r-t1/2; jx=xb-8
    # R also heavier at the top: a stronger top bar, and the leg tapers toward the foot
    L['R']=P([(jx-t2*k*0.55,jy),(jx+t2*k*0.55,jy),(jx+62+t2*0.3,B),(jx+62-t2*0.3,B)])
    L['Rt']=P([(x0,T),(xb,T),(xb,T+t1),(x0,T+t1*k*1.25)])
    L['Rd']=''; L['Rh']=''
    if desk=='top':      # a slightly thicker table top that overhangs to the left, with a short leg at its end
        L['Rd']=P([(x0-16,T-1),(xb,T-1),(xb,T+t1*1.9),(x0-16,T+t1*1.9)])+' '+P([(x0-12,T),(x0-12+t1,T),(x0-12+t1,T+58),(x0-12,T+58)])
    if desk=='round':    # the R's head becomes a wide, low desk counter with rounded corners, standing on two legs
        x0_,x1_,y0_,y1_,r=222,346,T,T+78,32
        def rrect(xa,ya,xb2,yb,rad):
            return (f'M{xa+rad} {ya} H{xb2-rad} A{rad} {rad} 0 0 1 {xb2} {ya+rad} V{yb-rad} A{rad} {rad} 0 0 1 {xb2-rad} {yb} '
                    f'H{xa+rad} A{rad} {rad} 0 0 1 {xa} {yb-rad} V{ya+rad} A{rad} {rad} 0 0 1 {xa+rad} {ya} Z')
        L['Rs']=''; L['Rt']=''; L['R']=''
        L['Rd']=rrect(x0_,y0_,x1_,y1_,r)+' '+rrect(x0_+t1*1.2,y0_+t1*1.6,x1_-t1*1.6,y1_-t1,r-t1*1.3)
        L['Rd']+=' '+P([(x0_+22,y1_-1),(x0_+22+t1,y1_-1),(x0_+22+t1,B),(x0_+22,B)])                 # straight leg
        L['Rd']+=' '+P([(x1_-52,y1_-2),(x1_-52+t2,y1_-2),(x1_+14+t2*0.5,B),(x1_+14-t2*0.5,B)])      # R's diagonal leg
    if desk=='horseshoe':   # the R's head is a horseshoe counter: round on the right, open to the left, on two legs
        xL,xc,Ro,w=224,298,42,9
        Ri=Ro-w; yb=T+2*Ro
        L['Rs']=''; L['Rt']=''; L['R']=''
        L['Rd']=(f'M{xL} {T} H{xc} A{Ro} {Ro} 0 0 1 {xc} {yb} H{xL} V{yb-w} H{xc} A{Ri} {Ri} 0 0 0 {xc} {T+w} H{xL} Z')
        L['Rd']+=' '+P([(xL+16,yb-1),(xL+16+t1,yb-1),(xL+16+t1,B),(xL+16,B)])                    # straight leg under the open end
        L['Rd']+=' '+P([(xc-8,yb-1),(xc-8+t2,yb-1),(xc+50+t2*0.5,B),(xc+50-t2*0.5,B)])            # R's diagonal leg
    if desk in ('elegant','elegant_all'):   # R from the reference: serifed stem, top bar into a stressed bowl, a hairline that drops and sweeps right
        x0,sw=228,t2*0.95; xh=x0+34; xb=xh+30; r=48; yb=T+2*r; hl=t1*0.55
        L['Rs']=''; L['Rt']=''; L['R']=''
        d=P([(x0,T),(x0+sw,T),(x0+sw,B),(x0,B)])                                              # stem
        d+=' '+P([(x0-9,T),(x0+sw+4,T),(x0+sw+4,T+hl*1.6),(x0-9,T+hl*1.6)])                    # top serif
        d+=' '+P([(x0-9,B-hl*1.6),(x0+sw+9,B-hl*1.6),(x0+sw+9,B),(x0-9,B)])                    # foot serif
        d+=' '+P([(x0,T),(xb,T),(xb,T+hl*1.8),(x0,T+hl*1.8)])                                   # top bar
        # bowl: outer circle r, inner circle shifted left so the right side is heavy
        d+=(f' M{xb} {T} A{r} {r} 0 0 1 {xb} {yb} L{xb} {yb-hl*1.6} A{r-t2*1.1} {r-hl*1.7} 0 0 0 {xb} {T+hl*1.8} Z')
        d+=' '+P([(xh,yb-hl*1.6),(xb,yb-hl*1.6),(xb,yb),(xh,yb)])                                # bowl closes onto the hairline
        L['Rd']=d
        L['Rh']=f'M{xh+hl/2} {T} V{B-30} Q{xh+hl/2} {B-hl/2} {xh+34} {B-hl/2} H{xh+78}'           # hairline leg
    if desk in ('elegant_all','traced_serif'):   # A and N in the same serif language as the elegant R
        hl=t1*0.55; sw=t2*0.95; sf=hl*1.6
        # A: hairline left leg, solid right leg, flat serifs at both feet (still no crossbar)
        A=P([(100,T),(102,T),(20+hl*2.2,B),(20,B)])+' '+P([(100,T),(100+sw*0.9,T),(184,B),(184-sw*1.25,B)])
        A+=' '+P([(8,B-sf),(36,B-sf),(36,B),(8,B)])+' '+P([(184-sw*1.25-12,B-sf),(194,B-sf),(194,B),(184-sw*1.25-12,B)])
        L['A']=A
        # N: hairline verticals with serifs, solid diagonal
        xl,xr=638,768
        N=P([(xl,T),(xl+hl*1.4,T),(xl+hl*1.4,B),(xl,B)])+' '+P([(xr-hl*1.4,T),(xr,T),(xr,B),(xr-hl*1.4,B)])
        N+=' '+P([(xl,T),(xl+sw*1.25,T),(xr,B),(xr-sw*1.25,B)])
        N+=' '+P([(xl-12,T),(xl+sw*1.25,T),(xl+sw*1.25,T+sf),(xl-12,T+sf)])+' '+P([(xl-12,B-sf),(xl+14,B-sf),(xl+14,B),(xl-12,B)])
        N+=' '+P([(xr-14,T),(xr+12,T),(xr+12,T+sf),(xr-14,T+sf)])
        L['N']=N
    if desk in ('traced','traced_serif'):   # the exact reference R (traced vector), scaled to cap height
        k_=200/136.2243; tx=226-27.8884*k_; ty=T-25.88*k_
        L['Rs']=''; L['Rt']=''; L['R']=''; L['Rd']=''
        L['Rx']=f'<path d="{TRACED}" transform="translate({tx:.2f} {ty:.2f}) scale({k_:.4f})" fill-rule="evenodd"/>'
        L['shift']=26
    if desk=='stem':     # cantilever desk: the stem is the leg, the top overhangs it on the left
        L['Rd']=P([(x0-22,T-1),(xb,T-1),(xb,T+t1*1.9),(x0-22,T+t1*1.9)])+' '+P([(x0+10,T),(x0+10+t1,T),(x0+10+t1,B),(x0+10,B)])
    # O: old-style diagonal stress — thick at lower-left and upper-right, thin at upper-left and lower-right
    cx,cy,rx,ry=496,140,96,100
    th=math.radians(-24); a=rx-t2*ko*0.95; b=ry-t1*1.1
    p1=(cx-a*math.cos(th),cy-a*math.sin(th)); p2=(cx+a*math.cos(th),cy+a*math.sin(th))
    rot=math.degrees(th)
    L['O']=(f'M{cx-rx} {cy} A{rx} {ry} 0 1 0 {cx+rx} {cy} A{rx} {ry} 0 1 0 {cx-rx} {cy} Z '
            f'M{p1[0]:.2f} {p1[1]:.2f} A{a:.2f} {b:.2f} {rot:.1f} 1 1 {p2[0]:.2f} {p2[1]:.2f} A{a:.2f} {b:.2f} {rot:.1f} 1 1 {p1[0]:.2f} {p1[1]:.2f} Z')
    # N: verticals and diagonal all widen toward the bottom
    xl,xr=638,768
    L['N']=(P(stroke(xl+t1*0.3,xl+t1*k/2,t1*0.6,t1*k))+' '+P(stroke(xr-t1*0.3,xr-t1*k/2,t1*0.6,t1*k))+' '+
            P([(xl,T),(xl+t2*1.2,T),(xr,B),(xr-t2*k*1.5,B)]))
    L['t1']=t1; return L
def svg(L,ink,grad,gid):
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient></defs>'
            f'<path d="{L["A"]}" fill="{ink}"/><path d="{L["Rs"] or "M0 0"}" fill="none" stroke="{ink}" stroke-width="{L["t1"]}"/><path d="{L["Rt"] or "M0 0"}" fill="{ink}"/><path d="{L["Rd"]}" fill="{ink}" fill-rule="evenodd"/><path d="{L.get("Rh") or "M0 0"}" fill="none" stroke="{ink}" stroke-width="{L["t1"]*0.55}"/><path d="{L["R"] or "M0 0"}" fill="{ink}"/>'
            + (f'<g fill="{ink}">{L["Rx"]}</g>' if L.get("Rx") else '')
            + f'<g transform="translate({L.get("shift",0)},0)"><path d="{L["O"]}" fill="url(#{gid})" fill-rule="evenodd"/><path d="{L["N"]}" fill="url(#{gid})"/></g>')
LIGHT='<stop offset="0" stop-color="#5f5c58"/><stop offset=".55" stop-color="#a7a39d"/><stop offset="1" stop-color="#d3cfc8"/>'
DARK='<stop offset="0" stop-color="#e2ddd5"/><stop offset=".55" stop-color="#9d9993"/><stop offset="1" stop-color="#5a5753"/>'
VB='-6 20 822 240'
sets=[('Final · Thin + O',4.2,8.5,1.0,1.9,None),('Traced R · thin letters',4.2,8.5,1.0,1.9,'traced'),('Traced R · serif letters',4.2,8.5,1.0,1.9,'traced_serif'),('Elegant · all letters',4.2,8.5,1.0,1.9,'elegant_all'),('R · elegant',4.2,8.5,1.0,1.9,'elegant'),('Desk · horseshoe',4.2,8.5,1.0,1.9,'horseshoe'),('Desk · rounded',4.2,8.5,1.0,1.9,'round'),('Desk · table top',4.2,8.5,1.0,1.9,'top'),('Desk · cantilever',4.2,8.5,1.0,1.9,'stem'),('Thin',4.2,8.5,1.0,None,None),('Weighted base',4.2,8.5,1.9,None,None),('Old-style',4.2,8.5,1.5,None,None)]
tiles=''
for name,t1,t2,k,ko,dk in sets:
    L=letters(t1,t2,k,ko,dk); key=name.lower().replace(' · ','-').replace(' + ','-').replace(' ','-')
    a=svg(L,'#1b1a18',LIGHT,'g'+key+'l'); b=svg(L,'#EEE9E4',DARK,'g'+key+'d')
    open(f'aron-thin-{key}-light.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="796" height="240" viewBox="{VB}">{a}</svg>')
    open(f'aron-thin-{key}-dark.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="796" height="240" viewBox="{VB}"><rect x="0" y="20" width="796" height="240" fill="#0e0e0e"/>{b}</svg>')
    tiles+=f'<p class="cap">{name.upper()}</p><div class="row"><div class="tile" style="background:#fff"><svg viewBox="{VB}">{a}</svg></div><div class="tile" style="background:#0e0e0e"><svg viewBox="{VB}">{b}</svg></div></div>'
html=f'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ARON · Thin</title>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300&family=Noto+Sans+KR:wght@300&display=swap" rel="stylesheet">
<style>*{{box-sizing:border-box;margin:0}}body{{background:#f3f1ee;font-family:Jost,"Noto Sans KR",sans-serif;color:#1b1a18;padding:56px 5vw 80px}}h1{{font-weight:300;font-size:34px;letter-spacing:.06em}}p{{color:#6b645c;margin:10px 0 24px;font-size:14px}}.cap{{font-size:12px;letter-spacing:.2em;color:#8a8278;margin:26px 0 10px}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}.tile{{aspect-ratio:16/8;display:grid;place-items:center;padding:10% 14%}}.tile svg{{width:100%;height:auto}}@media(max-width:800px){{.row{{grid-template-columns:1fr}}}}</style></head><body>
<h1>ARON · Wordmark (Thin)</h1><p>A와 R은 위로 갈수록 무겁게(꼭짓점·윗가로획이 굵고 아래는 가늘게), O와 N은 아래로 무겁게 — 위와 아래가 서로 균형을 잡아요. O는 사선 강세(가라몬드식). 기존 로고 형태(가로획 없는 A, 깎인 R, O, N) 그대로, ON은 회색 그라데이션. 아래는 비교용 기존 Thin.</p>
{tiles}
</body></html>'''
open('thin.html','w').write(html)
