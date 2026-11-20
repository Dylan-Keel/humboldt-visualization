"""Build 1 m ground, surface and canopy height rasters for a UTM 10N box from USGS 3DEP LiDAR (COPC tiles on Planetary Computer)."""
import sys, os, json, time, numpy as np, requests, laspy, rasterio
from rasterio.transform import from_origin
from pyproj import Transformer, CRS
import pystac_client, planetary_computer as pc
def run(name,box,res=1.0):
    x0,y0,x1,y1=box; W=int((x1-x0)/res); H=int((y1-y0)/res)
    dsm=np.full((H,W),-9999,np.float32); gnd=np.full((H,W),9999,np.float32)
    t=Transformer.from_crs(26910,4326,always_xy=True); lo=t.transform(x0,y0); hi=t.transform(x1,y1)
    c=pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1",modifier=pc.sign_inplace)
    its=list(c.search(collections=['3dep-lidar-copc'],bbox=[lo[0]-0.002,lo[1]-0.002,hi[0]+0.002,hi[1]+0.002],max_items=500).items())
    its=[i for i in its if 'Wildfires_B4_2018' in i.id] or its
    done=set(json.load(open(f'{name}_done.json'))) if os.path.exists(f'{name}_done.json') else set()
    if done: dsm=np.load(f'{name}_dsm.npy'); gnd=np.load(f'{name}_gnd.npy')
    print(name,len(its),'tiles',flush=True)
    for n,it in enumerate(its):
        if it.id in done: continue
        fn=f'/tmp/{name}_tile.copc.laz'
        for k in range(4):
            try:
                href=pc.sign(it.assets['data'].href)
                with requests.get(href,stream=True,timeout=600) as r, open(fn,'wb') as f:
                    for ch in r.iter_content(1<<22): f.write(ch)
                las=laspy.read(fn); break
            except Exception as e: print('retry',it.id,str(e)[:80],flush=True); time.sleep(5); las=None
        if las is None: print('FAILED',it.id,flush=True); continue
        crs=las.header.parse_crs(); 
        try: horiz=crs.sub_crs_list[0] if crs.is_compound else crs
        except Exception: horiz=crs
        tr=Transformer.from_crs(horiz,26910,always_xy=True)
        X,Y=tr.transform(np.asarray(las.x),np.asarray(las.y)); Z=np.asarray(las.z,dtype=np.float32)
        try:
            uf=crs.axis_info[-1].unit_conversion_factor if len(crs.axis_info)>2 else 1.0
        except Exception: uf=1.0
        if abs(uf-1)>1e-6: Z=Z*uf
        cl=np.asarray(las.classification)
        ci=((X-x0)/res).astype(np.int64); ri=((y1-Y)/res).astype(np.int64)
        ok=(ci>=0)&(ci<W)&(ri>=0)&(ri<H)&(cl!=7)&(cl!=18)
        if ok.sum()==0: done.add(it.id); print(n,it.id,'outside',flush=True); continue
        idx=ri[ok]*W+ci[ok]; z=Z[ok]; g=cl[ok]==2
        np.maximum.at(dsm.ravel(),idx,z); np.minimum.at(gnd.ravel(),idx[g],z[g])
        done.add(it.id)
        if n%4==0: np.save(f'{name}_dsm.npy',dsm); np.save(f'{name}_gnd.npy',gnd); json.dump(sorted(done),open(f'{name}_done.json','w'))
        print(n,it.id,'pts',int(ok.sum()),'ground',int(g.sum()),'z %.0f-%.0f'%(z.min(),z.max()),'unit',uf,flush=True)
    np.save(f'{name}_dsm.npy',dsm); np.save(f'{name}_gnd.npy',gnd); json.dump(sorted(done),open(f'{name}_done.json','w'))
    # fill ground gaps, build canopy height
    from scipy import ndimage as ndi
    has=gnd<9000; cov=dsm>-9000
    ind=ndi.distance_transform_edt(~has,return_distances=False,return_indices=True); dtm=gnd[tuple(ind)]
    dtm=ndi.uniform_filter(dtm,5)*(~has)+dtm*has          # soften interpolated cells only
    chm=np.where(cov,dsm-dtm,0); chm[chm<0]=0
    med=ndi.median_filter(chm,3); spike=(chm-med)>8; chm[spike]=med[spike]      # drop single-return spikes (birds, noise)
    chm[~cov]=np.nan
    for nm,a in (('dtm',np.where(ndi.binary_dilation(cov,iterations=3),dtm,np.nan)),('chm',chm)):
        with rasterio.open(f'{name}_{nm}.tif','w',driver='GTiff',width=W,height=H,count=1,dtype='float32',crs='EPSG:26910',transform=from_origin(x0,y1,res,res),compress='deflate',nodata=np.nan) as d: d.write(a.astype(np.float32),1)
    print(name,'done coverage %.3f'%cov.mean(),'chm p50 %.1f p99 %.1f max %.1f'%tuple(np.nanpercentile(chm,[50,99,100])),flush=True)
if __name__=='__main__':
    S={'fourmile':(383900,4455650,392900,4459700),'cooskie':(392000,4456700,394400,4459400),'fox':(424200,4500150,428100,4503900)}
    for s in sys.argv[1:]: run(s,S[s])
