"""Rebuild the Cooskie Ridge page from its existing data.json with the shared flipbook template and the LiDAR/TWI overlays."""
import json,re
h=open('site/index_prev.html').read()
d=json.load(open('site/data.json')); om=json.load(open('overlay_meta.json'))
i=h.find('<div class="notes">'); j=h.find('</div>\n</main>',i); notes=h[i+19:j]
lay=json.load(open('/home/claude/flip/layers_note.json')).replace('39 tops','38 tops').replace('2,664 in the drainage','257 in the watershed').replace('drainage, parcel and 3D views','watershed, parcel and 3D views')
k=notes.find('<h2>',10); notes=notes[:k]+lay.lstrip()+'  '+notes[k:] if k>0 else notes+lay
for f in d['frames']:
    f['year']=int(f['id'][:4]); f['bw']=f['year']<2005
note3d=re.search(r'id="note3d" hidden>(.*?)</p>',h,re.S).group(1)
for k,v in d['views'].items():
    v.update(om['views'].get(k,{}))
    if k=='d': v['note']=note3d
    for f in v['fires']: f['name']=f['name'] if f['name'].endswith('Fire') else f['name']
d['order']=['w','p','d']; d['slug']='cooskie'; d['rasters']=om['rasters']
d['labels']=dict(parcel='Parcel boundary, APN 104-122-019',shed='Wild Turkey Creek Watershed',tree='Legacy trees: LiDAR tops over 131 ft',rastnote='Canopy height and legacy trees are from 2018 USGS 3DEP LiDAR. Wetness index is computed from the 10 m elevation model.')
json.dump(d,open('site/data2.json','w'))
m=re.search(r'<h1>(.*?)</h1>\s*<p>(.*?)</p>',h,re.S)
t=open('/home/claude/flip/page.tpl').read()
out=t.replace('__DATA__',json.dumps(d)).replace('__TITLE__','Cooskie Ridge Aerial Flipbook').replace('__H1__',m.group(1)).replace('__SUB__',m.group(2)).replace('__NOTES__',notes)
open('site/index.html','w').write(out); print(len(out)//1000,'kB', 'layers note in' , 'Topographic Wetness' in notes)
