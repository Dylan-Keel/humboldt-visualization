import numpy as np, cv2, json, sys, os, rasterio
from rasterio.transform import from_origin
import geo
from cfg import *
def mosaic(tag,frames,views=None,suffix='',ocf=None,primary=None):
    """frames: list of (scanpath, posefile). writes master/{tag}_{k}.tif for each view"""
    views=views or VIEWS; scans=[]
    for path,pf in frames:
        z=dict(np.load(pf,allow_pickle=True)); cf=z['cf'].tolist() if z['cf'].ndim else float(z['cf'])
        if ocf is not None:
            from PIL import Image
            Wf,Hf=Image.open(path).size; c0=(cf,)*4 if isinstance(cf,(int,float)) else cf
            K=z['K'].copy(); K[0,2]+=(c0[0]-ocf)*Wf; K[1,2]+=(c0[1]-ocf)*Hf; z['K']=K; cf=ocf
        z['pri']=0 if (primary and any(p in path for p in primary)) else 1
        scans.append((geo.load(path,cf),z))
    cov={}
    for k,(v,r) in views.items():
        W,H=size(v,r)
        X,Y=np.meshgrid(v[0]+(np.arange(W,dtype=np.float32)+.5)*r, v[3]-(np.arange(H,dtype=np.float32)+.5)*r)
        best=np.full((H,W),1e12,np.float32); out=np.zeros((H,W),np.float32); L=[]
        for a,z in scans:
            o=geo.ortho(a,z['K'],z['d'],z['rv'],z['tv'],v,r).astype(np.float32)
            e=max(3,int(40/r))|1
            vv=cv2.erode((o>0).astype(np.uint8),np.ones((e,e),np.uint8)).astype(bool)
            if vv.sum()<1000: continue
            d2=(X-float(z['cam'][0]))**2+(Y-float(z['cam'][1]))**2+z['pri']*1e9; L.append([o,vv,d2])
        if not L: cov[k]=0; continue
        L.sort(key=lambda l:-l[1].sum()); ro,rv_=L[0][0],L[0][1]
        for i,(o,vv,d2) in enumerate(L):
            ov=vv&rv_
            if i>0 and ov.sum()>20000:
                a_,b_=o[ov].std(),ro[ov].std(); o[:]=(o-o[ov].mean())*(b_/max(a_,1e-3))+ro[ov].mean()
            m=vv&(d2<best); out[m]=o[m]; best[m]=d2[m]
        out=np.clip(out,1,255).astype(np.uint8); out[best>=1e11]=0; cov[k]=float((best<1e11).mean())
        with rasterio.open(f'master/{tag}_{k}{suffix}.tif','w',driver='GTiff',width=W,height=H,count=1,dtype='uint8',crs='EPSG:26910',transform=from_origin(v[0],v[3],r,r),compress='deflate') as ds: ds.write(out,1)
        cv2.imwrite(f'master/{tag}_{k}_th.jpg',cv2.resize(out,(W//4,H//4),interpolation=cv2.INTER_AREA))
    print(tag,'coverage',cov,flush=True); return cov
if __name__=='__main__':
    J=json.load(open(sys.argv[1]))
    for tag in sys.argv[2:]: mosaic(tag,[tuple(x) for x in J[tag]])
