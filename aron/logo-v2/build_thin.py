import math, sys
T,B=40,240; H=B-T
def P(pts): return 'M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in pts)+' Z'
def stroke(xt,xb,wt,wb):
    # a straight stroke from top centre xt to bottom centre xb, width wt at the top and wb at the bottom (horizontal widths)
    return [(xt-wt/2,T),(xt+wt/2,T),(xb+wb/2,B),(xb-wb/2,B)]
def letters(t1,t2,k):
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
    # O: old-style diagonal stress — thick at lower-left and upper-right, thin at upper-left and lower-right
    cx,cy,rx,ry=496,140,96,100
    th=math.radians(-24); a=rx-t2*k*0.95; b=ry-t1*1.1
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
            f'<path d="{L["A"]}" fill="{ink}"/><path d="{L["Rs"]}" fill="none" stroke="{ink}" stroke-width="{L["t1"]}"/><path d="{L["Rt"]}" fill="{ink}"/><path d="{L["R"]}" fill="{ink}"/>'
            f'<path d="{L["O"]}" fill="url(#{gid})" fill-rule="evenodd"/><path d="{L["N"]}" fill="url(#{gid})"/>')
LIGHT='<stop offset="0" stop-color="#5f5c58"/><stop offset=".55" stop-color="#a7a39d"/><stop offset="1" stop-color="#d3cfc8"/>'
DARK='<stop offset="0" stop-color="#e2ddd5"/><stop offset=".55" stop-color="#9d9993"/><stop offset="1" stop-color="#5a5753"/>'
VB='0 20 796 240'
sets=[('Old-style',4.2,8.5,1.5),('Weighted base',4.2,8.5,1.9),('Thin',4.2,8.5,1.0)]
tiles=''
for name,t1,t2,k in sets:
    L=letters(t1,t2,k); key=name.lower().replace(' ','-')
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
