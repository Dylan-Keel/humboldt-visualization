import numpy as np, cv2, rasterio, json, re, os, sys, requests, time
from PIL import Image
from cfg import OX,OY,BX
dem=rasterio.open('ref/dem10.tif').read(1)
def hillshade(az,alt):
    gy,gx=np.gradient(dem,10.0); a=np.radians(az); e=np.radians(alt)
    nx=-gx; ny=gy; nn=np.sqrt(nx*nx+ny*ny+1)
    return np.clip((nx*np.sin(a)*np.cos(e)+ny*np.cos(a)*np.cos(e)+np.sin(e))/nn,0,1).astype(np.float32)
hp=lambda a,s:cv2.GaussianBlur(a,(0,0),0.8)-cv2.GaussianBlur(a,(0,0),s)
import os
REFSEL=os.environ.get('REFSEL','')
SCALES=(7.2,8.4,9.8,11.4,13.2,15.3,18.0)
def crop(path):
    a=np.asarray(Image.open(path).convert('L')); h,w=a.shape; return a[int(h*.08):int(h*.92),int(w*.08):int(w*.92)]
_C={}
def coarse_refs(g):
    if g not in _C:
        def w2(a,res):
            c=a[int((OY-BX[3])/res):int((OY-BX[1])/res),int((BX[0]-OX)/res):int((BX[2]-OX)/res)]
            return cv2.resize(c,(int((BX[2]-BX[0])/g),int((BX[3]-BX[1])/g)),interpolation=cv2.INTER_AREA)
        s=300.0/g
        _C[g]=[(nm,hp(w2(hillshade(az,45),10)*255,s)) for nm,az in (('hs150',150),('hs215',215))]
        im=np.asarray(Image.open('ref/naip2005_5m.jpg').convert('L')).astype(np.float32)
        _C[g].append(('img05',hp(cv2.resize(im,(int((BX[2]-BX[0])/g),int((BX[3]-BX[1])/g)),interpolation=cv2.INTER_AREA),s)))
    return _C[g]
def locate(a,g=50.0,scales=SCALES,drs=(-6,6)):
    a=a.astype(np.float32); out=[]; s=300.0/g
    for mpp in scales:
        t=cv2.resize(cv2.GaussianBlur(a,(0,0),max(0.5,g/mpp/2.5)),None,fx=mpp/g,fy=mpp/g,interpolation=cv2.INTER_AREA)
        if min(t.shape)<28: continue
        for base in (0,90,180,270):
            tb=np.ascontiguousarray(np.rot90(t,base//90))
            for dr in drs:
                hh,ww=tb.shape; M=cv2.getRotationMatrix2D((ww/2,hh/2),dr,1.0)
                tr=hp(cv2.warpAffine(tb,M,(ww,hh),borderMode=cv2.BORDER_REFLECT),s); m=int(min(hh,ww)*0.1); tr=tr[m:-m,m:-m]
                for nm,R in [c for c in coarse_refs(g) if REFSEL in c[0]]:
                    if tr.shape[0]>=R.shape[0] or tr.shape[1]>=R.shape[1]: continue
                    res=cv2.matchTemplate(R,tr,cv2.TM_CCOEFF_NORMED); _,mx,_,lc=cv2.minMaxLoc(res)
                    z=(mx-res.mean())/(res.std()+1e-6)
                    out.append((float(z),float(mx),nm,mpp,base+dr,BX[0]+(lc[0]+tr.shape[1]/2)*g,BX[3]-(lc[1]+tr.shape[0]/2)*g))
    out.sort(reverse=True); zs=np.array([o[0] for o in out])
    return out[0],float(zs[0]-np.median(zs))
S=requests.Session(); S.headers['User-Agent']='Mozilla/5.0'
def preview(aid):
    fn=f'hc/pv/{aid}.jpg'
    if not os.path.exists(fn):
        for k in range(3):
            try:
                b=S.get(f'https://digitalcommons.humboldt.edu/hcapc_aerial/{aid}/preview.jpg',timeout=40).content
                if b[:2]==b'\xff\xd8': open(fn,'wb').write(b); break
            except Exception as e: time.sleep(1)
        else: return None
    return fn if os.path.exists(fn) else None
def catalog():
    out=[]; seen=set()
    for l in open('hc/oai.jsonl'):
        r=json.loads(l)
        if not r['title'] or not r['identifier']: continue
        m=re.search(r'article/(\d+)/',r['identifier'][0])
        if m and m.group(1) not in seen: seen.add(m.group(1)); out.append((r['title'][0],(r['date'][0][:10] if r['date'] else ''),m.group(1)))
    return out
def work(c):
    t,d,aid=c
    try:
        fn=preview(aid)
        if not fn: return None
        b,z=locate(crop(fn))
        return dict(title=t,date=d,aid=aid,z=round(b[0],2),ncc=round(b[1],3),ref=b[2],mpp=b[3],rot=b[4],x=round(b[5]),y=round(b[6]),dz=round(z,2))
    except Exception as e: return None
if __name__=='__main__':
    from multiprocessing import Pool
    step=int(sys.argv[1]); off=int(sys.argv[2]); outf=sys.argv[3]; pat=sys.argv[4] if len(sys.argv)>4 else '.'
    key=lambda c:[int(x) if x.isdigit() else x for x in re.split(r'(\d+)',c[0])]
    cat=sorted([c for c in catalog() if re.match(pat,c[0])],key=key)[off::step]
    done=set(json.loads(l)['aid'] for l in open(outf)) if os.path.exists(outf) else set()
    cat=[c for c in cat if c[2] not in done]; print(len(cat),'frames',flush=True)
    cv2.setNumThreads(1); coarse_refs(50.0)
    with Pool(6) as p, open(outf,'a') as f:
        for i,r in enumerate(p.imap_unordered(work,cat,chunksize=4)):
            if r: f.write(json.dumps(r)+'\n'); f.flush()
            if i%500==0: print(i,flush=True)
