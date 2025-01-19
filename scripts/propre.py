# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
#!/usr/bin/env python3

from utils import*
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pyDhd import *


plt.close('all')

def ressort_simple(d,k):
    return -d*k

def mur_en_y(py,vy,pos=0.02):#experimentale
    cy=200
    if py >0.02:
        return Vecteur3d(0,-(py-pos)*500,0)
    else :
        #fy=cy*vy
        return Vecteur3d(0,0,0)
    
def mur(pos,m=Vecteur3d(0,0.02,0),n=Vecteur3d(0,1,0)):

    '''m point du plan , n vecteur normale au plan'''
    n=n.norm()
   
    a=n**pos
    b=n**m
    dist=(a-b)/n.mod()
    temp=-dist*float(exp(-90000*dist*dist))#derivee d'une gaussienne
    force=ressort_simple(d=temp,k=20000)
    force=n*force
  
    #print("temp=",temp)
    print ('position=',pos)
    print('force=',force)
    
    return force
    #return Vecteur3d(0,0,0)

    '''  
    #autre methode plus simple
    vec=m-pos
    temp=vec**n
    force=ressort_simple(d=-temp,k=1000)
    force=n*force
    if temp<0 :
        return force.x,force.y,force.z
    else :
        return 0,0,0
    
    '''

 
def cube(pos):
    L=0.06
    b=1000
    mur1=mur(pos,m=Vecteur3d(L/2,0,0),n=Vecteur3d(1,0,0))
    mur2=mur(pos,m=Vecteur3d(-L/2,0,0),n=Vecteur3d(1,0,0))#selonx
    
    mur1=mur1*float(1/(1+exp(-b*(pos.y - -L/2 ))))*float(1/(1+exp(b*(pos.y - +L/2))))#independant du point de definition du mur 
    mur2=mur2*float(1/(1+exp(-b*(pos.y - -L/2 ))))*float(1/(1+exp(b*(pos.y - +L/2)))) #troncer selon y

    mur1=mur1*float(1/(1+exp(-b*(pos.z - -L/2 ))))*float(1/(1+exp(b*(pos.z - +L/2))))#independant du point de definition du mur 
    mur2=mur2*float(1/(1+exp(-b*(pos.z - -L/2 ))))*float(1/(1+exp(b*(pos.z - +L/2)))) #troncer selon z


    mur3=mur(pos,m=Vecteur3d(0,L/2,0),n=Vecteur3d(0,1,0))
    mur4=mur(pos,m=Vecteur3d(0,-L/2,0),n=Vecteur3d(0,1,0))#selony
    
    mur3=mur3*float(1/(1+exp(-b*(pos.x - -L/2 ))))*float(1/(1+exp(b*(pos.x - +L/2))))#independant du point de definition du mur 
    mur4=mur4*float(1/(1+exp(-b*(pos.x - -L/2 ))))*float(1/(1+exp(b*(pos.x - +L/2)))) #troncer selon x

    mur3=mur3*float(1/(1+exp(-b*(pos.z - -L/2 ))))*float(1/(1+exp(b*(pos.z - +L/2))))#independant du point de definition du mur 
    mur4=mur4*float(1/(1+exp(-b*(pos.z - -L/2 ))))*float(1/(1+exp(b*(pos.z - +L/2)))) #troncer selon z

    mur5=mur(pos,m=Vecteur3d(0,0,L/2),n=Vecteur3d(0,0,1))
    mur6=mur(pos,m=Vecteur3d(0,0,-L/2),n=Vecteur3d(0,0,1))#selonz
    
    mur5=mur5*float(1/(1+exp(-b*(pos.y - -L/2 ))))*float(1/(1+exp(b*(pos.y - +L/2))))#independant du point de definition du mur 
    mur6=mur6*float(1/(1+exp(-b*(pos.y - -L/2 ))))*float(1/(1+exp(b*(pos.y - +L/2)))) #troncer selon y

    mur5=mur5*float(1/(1+exp(-b*(pos.x - -L/2 ))))*float(1/(1+exp(b*(pos.x - +L/2))))#independant du point de definition du mur 
    mur6=mur6*float(1/(1+exp(-b*(pos.x - -L/2 ))))*float(1/(1+exp(b*(pos.x - +L/2)))) #troncer selon x
    
    
    force=mur1+mur2+mur3+mur4+mur5+mur6
    force.x=min(max(force.x,-15),15)
    force.z=min(max(force.z,-15),15)
    force.y=min(max(force.y,-15),15)
    return force
    #return Vecteur3d(0,0,0)
    
    
    
def sphere(pos,center=Vecteur3d(0,0,0),rayon=0.04):
    
    vec=(pos-center)
    dist=vec.mod() -rayon
    temp=-dist*float(exp(-90000*dist*dist))#derivee d'une gaussienne
    force=ressort_simple(d=temp,k=20000)
    force=force*vec.norm()
    return force


def glissiere(pos,n=Vecteur3d(0,1,0),p=Vecteur3d(0,0,0)):
    #texture=sin
    f=300
    n=n.norm()
    vec=(pos-p)**n
    f_colle=(pos-p) -vec*n
    
    f_tan=-5*np.cos(f*pos**n)*n#pos.x - p.x*
    #f_tan=ressort_simple(f_tan, 1000)*n
    f_colle=ressort_simple(f_colle,k=1000)
    force=f_colle+f_tan
    return force 



def mur_texture(pos,m=Vecteur3d(0.0,-0.02,0),n=Vecteur3d(0,1,0)):

    f=500
    n=n.norm()
    #m=m+Vecteur3d(0,np.cos(f*pos.x),0)
   
    pos=pos+Vecteur3d(0,5*float(np.cos(f*pos.x)),0)
    a=n**pos
    b=n**m
    dist=(a-b)#/n.mod()
    
    temp=-dist*float(exp(-90000*dist*dist))#derivee d'une gaussienne
    force=ressort_simple(d=temp,k=20000)
    force=n*force
  
    #print("temp=",temp)
    #print ('distance au plan',dist)
    print('force=',force)
    
    return force
        
"""Initialisation"""


done = False

posy = []
fylist=[]

posx = []
fxlist=[]

posz = []
fzlist=[]

y_plot = [i * 0.001 for i in range(-22, 20)]  # a changer avec la position du mur theorique 
x_plot = [i * 0.001 for i in range(-22, 20)]
z_plot = [i * 0.001 for i in range(-22, 20)]
X_plot, Y_plot = np.meshgrid(x_plot, y_plot)
force_magz = []


fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-0.08, 0.08]) 
ax.set_ylim([-0.08, 0.08])
ax.set_xlabel("X Position (m)")
ax.set_ylabel("Y Position (m)")
ax.set_zlabel("Force Magnitude (N)")
scatter = ax.scatter([], [], [], color='blue',s=1)


dhdOpen()#pour ourir la communçcation usb

while(not done):

    '''Aquisition'''
    ret, px,py,pz = dhdGetPosition()#ret pour dire c cbien passer , le reste les positions
    ret, vx, vy, vz = dhdGetLinearVelocity()#recup vitesses
    
    done=dhdGetButton(0)
    position=Vecteur3d(px,py,pz)
    

    '''Question 1'''

    '''
    k=500
    fx,fy,fz=ressort_simple(position,k).lst()
    dhdSetForce(fx,fy,fz)

    ret,fx,fy,fz=dhdGetForce()
    posx = posx + [px]#pour tracer
    fxlist = fxlist + [fx]
    posx = posx + [px]#pour tracer
    posy = posy + [py]
    posz = posz + [pz]
    fxlist = fxlist + [fx]
    fylist = fylist + [fy]
    fzlist = fzlist + [fz]
    '''
   
    
    '''Question 2 '''

    '''
    #x,y,z=mur_en_y(py,vy).lst()    #experimentale
    fx,fy,fz=mur(position).lst()

    dhdSetForce(fx,fy,fz)
    

    ret,fx,fy,fz=dhdGetForce()

    posx = posx + [px]#pour tracer
    fxlist = fxlist + [fx]

    posy = posy + [py]#pour tracer
    fylist = fylist + [fy]#pour tracer
    
    posz = posz + [pz]#pour tracer
    fzlist = fzlist + [fz]

    force_magz.append(fx + fy)
    #ax.scatter(px, py, fx + fy, color="blue", s=10)
    





    '''


    '''Question Cube '''
    '''
    fx,fy,fz=cube(position).lst()
    
    dhdSetForce(fx,fy,fz)

    ret,fx,fy,fz=dhdGetForce()
    
    posx = posx + [px]#pour tracer
    fxlist = fxlist + [fx]

    posy = posy + [py]#pour tracer
    fylist = fylist + [fy]#pour tracer
    
    posz = posz + [pz]#pour tracer
    fzlist = fzlist + [fz]

    force_magz.append(fx + fy)
    
    #ax.scatter(px, py, fx + fy, color="blue", s=10)
    #plt.pause(0.00001)
    '''  
    
    '''Question Sphere '''
    
    #fx,fy,fz=sphere(position).lst()
    
    fx,fy,fz=mur_texture(position).lst()
    dhdSetForce(fx,fy,fz)

    ret,fx,fy,fz=dhdGetForce()
    
    posx = posx + [px]#pour tracer
    fxlist = fxlist + [fx]

    posy = posy + [py]#pour tracer
    fylist = fylist + [fy]#pour tracer
    
    posz = posz + [pz]#pour tracer
    fzlist = fzlist + [fz]

    force_magz.append(fx + fy)
    
    #ax.scatter(px, py, fx + fy, color="blue", s=10)
    #plt.pause(0.00001)
    
    
    '''Question Glissiere '''
    '''
    fx,fy,fz=glissiere(position).lst()
    
    dhdSetForce(fx,fy,fz)

    ret,fx,fy,fz=dhdGetForce()
    
    posx = posx + [px]#pour tracer
    fxlist = fxlist + [fx]

    posy = posy + [py]#pour tracer
    fylist = fylist + [fy]#pour tracer
    
    posz = posz + [pz]#pour tracer
    fzlist = fzlist + [fz]

    force_magz.append(fx + fy)
    
    #ax.scatter(px, py, fx + fy, color="blue", s=10)
    #plt.pause(0.00001)
    '''
    
    
    
    
    
    
dhdClose()


'''Tracer de la Question 1'''
'''

plt.figure(figsize=(8, 6))
plt.plot(posx, label="Position (x-component)", color="blue")  # No x-abscissa provided
plt.title("Position[n] (x-component) ")
plt.xlabel("sampeles")
plt.ylabel("Position (x-component)")
plt.grid(True)
plt.legend()
plt.show()

alpha=np.log(0.0322/0.0161)/(2*np.pi*1)
F=1/((-3789+4067)*10**-3)
omega=2*np.pi*F/(1-alpha**2)**0.5
m=k/omega**2
c=2*alpha*omega/m
print('mass=',m)
print('amortissement = ',c)
'''


'''Tracer de la Question 2'''
'''



scatter._offsets3d = (posx, posy, force_magz)
plt.show()

plt.figure(figsize=(8, 6))
plt.plot(posy,fylist, label="Force (y-component)", color="blue")#, marker="o"
plt.title("Force (y-component) vs Position (y)")
plt.xlabel("y Position (m)")
plt.ylabel("Force in y (N)")
plt.grid(True)
plt.legend()

plt.figure(figsize=(8, 6))
plt.plot(posx,fxlist, label="Force (x-component)", color="blue")#, marker="o"
plt.title("Force (x-component) vs Position (x)")
plt.xlabel("x Position (m)")
plt.ylabel("Force in x (N)")
plt.grid(True)
plt.legend()


plt.figure(figsize=(8, 6))
plt.plot(posz,fzlist, label="Force (z-component)", color="blue")#, marker="o"
plt.title("Force (z-component) vs Position (z)")
plt.xlabel("z Position (m)")
plt.ylabel("Force in z (N)")
plt.grid(True)
plt.legend()
plt.show()
'''


''' Tracer de la Question Cube'''

'''
scatter._offsets3d = (posx, posy, force_magz)
plt.show()
'''


''' Tracer de la Question sphere'''

scatter._offsets3d = (posx, posy, force_magz)
plt.show()