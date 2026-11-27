import sys, numpy as np, cv2
W,H=1920,1080; fps=30
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
def interp(t,tbl): return float(np.interp(t,[a for a,b in tbl],[b for a,b in tbl]))
dropY=[(0,108),(1.467,108),(1.567,209),(1.667,473),(1.8,545)]
ripR=[(1.8,70),(2.0,170),(2.4,250),(2.7,380),(2.9,520),(3.4,590),(4.6,720),(6,900),(8,1100),(14,1300)]
i=0; inp=sys.stdin.buffer; out=sys.stdout.buffer
while True:
    b=inp.read(W*H*3)
    if len(b)<W*H*3: break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.float32)
    t=i/fps
    if t<1.8:
        cx,cy=955,interp(t,dropY); rx=ry=80; fe=110
    else:
        k=min(1,(t-1.8)/0.5); k=k*k*(3-2*k)
        cx=955; cy=545+25*k; r=interp(t,ripR); rx=r; ry=r*0.5; fe=90+0.45*r
    d=np.sqrt(((xx-cx)/rx)**2+((yy-cy)/ry)**2)  # 1 at edge
    dist=(d-1)*min(rx,ry)  # approx px outside edge
    m=np.clip(1-dist/fe,0,1); m=m*m*(3-2*m)
    bl=cv2.GaussianBlur(f,(0,0),15)
    o=f*m[...,None]+bl*(1-m[...,None])
    out.write(o.clip(0,255).astype(np.uint8).tobytes()); i+=1
