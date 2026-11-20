import rasterio, numpy as np, json, geopandas as gpd, os, sys, datetime
from PIL import Image
from shapely.geometry import box
import r3d, cams
from cfg import *
F=json.load(open('frames.json'))
os.makedirs('site/frames',exist_ok=True)
NAMES={'w':'Drainage','p':'Parcel','a':'3D parcel','b':'3D drainage'}
force=set(sys.argv[1:])
def rgb(path):
    a=rasterio.open(path).read(); a=a[:3] if a.shape[0]>=3 else np.repeat(a[:1],3,0); return Image.fromarray(np.moveaxis(a,0,-1))
for f in F:
    fid=f['id']
    for k,(v,r) in VIEWS.items():
        out=f'site/frames/{k}_{fid}.jpg'
        if os.path.exists(out) and fid not in force: continue
        im=rgb(f"master/{f['file']}_{k}.tif"); W,H=im.size
        im.save(out,quality=84,optimize=True,progressive=True)
        im.resize((W//2,H//2),Image.LANCZOS).save(f'site/frames/{k}s_{fid}.jpg',quality=80,optimize=True,progressive=True)
    for k,c in cams.CAMS.items():
        out=f'site/frames/{k}_{fid}.jpg'
        if os.path.exists(out) and fid not in force: continue
        X,Y,D=c.ground_map(); im=Image.fromarray(r3d.render(f['file'],X,Y,D))
        im.save(out,quality=86,optimize=True,progressive=True); im.resize((1200,900),Image.LANCZOS).save(f'site/frames/{k}s_{fid}.jpg',quality=80,optimize=True,progressive=True)
    print(fid,flush=True)
parcel=gpd.read_file('parcel.geojson').to_crs(26910).geometry.iloc[0]
ws=gpd.read_file('watershed.geojson').geometry.iloc[0].simplify(6)
nhd=gpd.read_file('nhd_utm.geojson')
fg=gpd.read_file('fires.geojson').set_crs(26910,allow_override=True)
FCOL={(1956,'Pearson Lbr. Co.'):'#ff8a3d',(1952,'L. Sibley'):'#ff4d6d',(1952,'L.M. Shaw'):'#d98cff',(2008,'Iaqua'):'#8be28b',(2009,'Kneeland'):'#f2a6c8'}
def fmeta(f):
    dt=(datetime.datetime(1970,1,1)+datetime.timedelta(milliseconds=float(f.ALARM_DATE))).strftime('%B %-d, %Y')
    nm=f.FIRE_NAME.title().replace('L.m.','L.M.'); return dict(year=int(f.YEAR_),name=nm,date=dt,acres=round(float(f.GIS_ACRES)),color=FCOL.get((int(f.YEAR_),nm),'#c9c9c9'))
ov={}
wsb=ws.buffer(0)
for k,(v,r) in VIEWS.items():
    x0,y0,x1,y1=v; bb=box(*v); W,H=size(v,r)
    def path(g):
        out=[]
        for gg in getattr(g,'geoms',[g]):
            if gg.is_empty: continue
            if gg.geom_type=='Polygon':
                for ring in [gg.exterior]+list(gg.interiors): out.append('M'+' L'.join(f'{(x-x0)/r:.1f} {(y1-y)/r:.1f}' for x,y,*_ in ring.coords)+'Z')
            elif gg.geom_type in('LineString','LinearRing'): out.append('M'+' L'.join(f'{(x-x0)/r:.1f} {(y1-y)/r:.1f}' for x,y,*_ in gg.coords))
            elif hasattr(gg,'geoms'): out.append(path(gg))
        return ' '.join(out)
    st=' '.join(path(g.intersection(wsb).intersection(bb.buffer(50))) for g in nhd.geometry if g.intersects(wsb))
    fires=[]
    for _,f in fg.iterrows():
        g=f.geometry.buffer(0)
        if g.intersection(bb).area<2000: continue
        m=fmeta(f); m['d']=path(g.intersection(bb.buffer(30)).boundary if False else g); fires.append(m)
    fires.sort(key=lambda x:x['year'])
    ov[k]=dict(name=NAMES[k],w=W,h=H,res=r,parcel=path(parcel),watershed=path(ws),streams=st,fires=fires)
NOTE={'a':'This view looks northwest at the parcel from a point about 1.9 km to the southeast and roughly 1,000 m above it. Grey terrain has no photo coverage for that year.',
      'b':'This view looks southwest up the drainage from above the Mad River, which crosses the bottom of the frame. The parcel is in the lower right part of the drainage. Grey terrain has no photo coverage for that year.'}
for k,c in cams.CAMS.items():
    X,Y,D=c.ground_map(); fires=[]
    for _,f in fg.iterrows():
        d=c.path3d(f.geometry.buffer(0).boundary,D)
        if len(d)<40: continue
        m=fmeta(f); m['d']=d; fires.append(m)
    fires.sort(key=lambda x:x['year'])
    st=' '.join(c.path3d(g.intersection(wsb),D) for g in nhd.geometry if g.intersects(wsb))
    ov[k]=dict(name=NAMES[k],w=r3d.W,h=r3d.H,res=None,parcel=c.path3d(parcel,D),watershed=c.path3d(ws,D),streams=st,fires=fires,note=NOTE[k])
data=dict(frames=[dict(id=f['id'],label=f['label'],year=f['year'],date=f['date'],source=f['source'],res=f['res'],note=f.get('note',''),bw=f.get('bw',False)) for f in F],views=ov,order=['w','p','a','b'])
json.dump(data,open('site/data.json','w'))
tpl=open('page.tpl').read(); N=json.load(open('notes.json'))
html=tpl.replace('__DATA__',json.dumps(data)).replace('__H1__',N['h1']).replace('__SUB__',N['sub']).replace('__NOTES__',N['notes'])
open('site/index.html','w').write(html)
tot=sum(os.path.getsize('site/frames/'+f) for f in os.listdir('site/frames')); print('files',len(os.listdir('site/frames')),'MB',round(tot/1e6,1),'html kB',len(html)//1000)
