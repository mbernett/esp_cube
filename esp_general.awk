#! /usr/bin/awk -f
BEGIN{
bohr=0.529177249;

x0=-10; y0=-10; z0=-10;

xmin=x0*bohr; ymin=y0*bohr; zmin=z0*bohr;
xmax=-xmin; ymax=-ymin; zmax=-zmin;

Nx=Ny=Nz=10;
xinc=(xmax-xmin)/(Nx-1); yinc=(ymax-ymin)/(Ny-1); zinc=(zmax-zmin)/(Nz-1);

i=0;
}

{
 if ($1=="ATOM") {
  charge[i]=$9;
  x[i]=$6;
  y[i]=$7;
  z[i]=$8;
  i++
 }
}

END{
print " Opt job potenital=scf"
print " Electrostatic potential from Total SCF Density"
printf "%5i%11.5f%12.5f%12.5f\n", i,xmin/bohr,ymin/bohr,zmin/bohr;
printf "%5i%11.5f%12.5f%12.5f\n", Nx,xinc/bohr,0,0;
printf "%5i%11.5f%12.5f%12.5f\n", Ny,0,yinc/bohr,0;
printf "%5i%11.5f%12.5f%12.5f\n", Nz,0,0,zinc/bohr;
for (ii=0;ii<i;ii++) {
 printf "%5i%11.5f%12.5f%12.5f%12.5f\n", 0,0,x[ii]/bohr,y[ii]/bohr,z[ii]/bohr;
}

for(nx=0;nx<Nx;nx++){
 xprobe=xmin+nx*xinc;
 for(ny=0;ny<Ny;ny++){
  yprobe=ymin+ny*yinc;
  for(nz=0;nz<Nz;nz++){
   E[nz]=0
   for(j=0;j<i;j++){
   zprobe=zmin+nz*zinc;
   E[nz]=E[nz]+((charge[j])/sqrt(((xprobe-x[j])**2)+((yprobe-y[j])**2)+((zprobe-z[j])**2)))
   }
  }
  for(k=0;k<Nz;k++) {
   #la prima condizione k%6 da zero solo per multipli interi di 6
   #la seconda impone di andare a capo per l'ultimo valore di z
   #entrambe vanno soddisfatte
   if (((k+1)%6==0)||(k==(Nz-1))) {
   printf "%13.5e\n", E[k];
   } else {
   printf "%13.5e", E[k];
   }
  }
 }
}
}
