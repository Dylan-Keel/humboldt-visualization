OX,OY=418000,4512000           # ref DEM origin (10 m, 1800 px)
VW=(424200,4500150,428100,4503900); RW=1.0     # drainage view
VP=(426450,4502800,427200,4503550); RP=0.3     # parcel view
VIEWS={'w':(VW,RW),'p':(VP,RP)}
def size(v,r): return int(round((v[2]-v[0])/r)),int(round((v[3]-v[1])/r))
VX=(422000,4498000,430500,4506500); RX=2.5     # wide backdrop for 3D
ALLV=dict(VIEWS); ALLV['x']=(VX,RX)
