#!/usr/bin/env python3

from pyDhd import *

done = False
dhdOpen()#pour ourir la communçcation usb
k1=1000
while(not done):
    ret, px,py,pz = dhdGetPosition()#ret pour dire c cbien passer , le reste les positions
    ret, vx, vy, vz = dhdGetLinearVelocity()#recup vitesses
    print (ret,px,py,pz)
    done=dhdGetButton(0)#pour savoir si l'utilisateur appuit sur les bouttons 0 button centrale
    #1 a droite ,2 a gauche
    dhdSetForce(-k1*px,0,0)#il va essayer de pousser 10 newr=ton selon l'axe x
#    print(done)
    
dhdClose()
