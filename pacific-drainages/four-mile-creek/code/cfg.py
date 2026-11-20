OX,OY=378000,4467500           # ref DEM origin (10 m, 1800 px)
VW=(383900,4455650,392900,4459700); RW=1.5     # watershed view, ~500 m buffer
VP=(386000,4457450,387320,4458770); RP=0.4     # parcel view, ~250 m buffer
VIEWS={'w':(VW,RW),'p':(VP,RP)}
def size(v,r): return int(round((v[2]-v[0])/r)),int(round((v[3]-v[1])/r))
VX=(381500,4453500,394500,4462000); RX=2.5     # wide backdrop for 3D and refinement
ALLV=dict(VIEWS); ALLV['x']=(VX,RX)
CEN=(388000.,4458000.)
BX=(380500,4450500,395500,4465500)
