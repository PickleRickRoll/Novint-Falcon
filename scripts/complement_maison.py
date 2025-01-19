import numpy as np
from utils import *
import matplotlib.pyplot as plt


def ressort_simple(d,k):
    return -d*k



def mur(pos, m=Vecteur3d(0.0, 0.02, 0), n=Vecteur3d(0, 1, 0)):
    """
    Cette fonction calcule la force exercée par un mur virtuel modélisé par un plan, 
    en fonction de la position donnée et des caractéristiques du plan.

    Inputs:
    - pos (Vecteur3d): Position actuelle de l'interface ou de l'objet (en coordonnées 3D).
    - m (Vecteur3d): Un point appartenant au plan du mur (par défaut : Vecteur3d(0.0, -0.02, 0)).
    - n (Vecteur3d): Le vecteur normal au plan du mur (par défaut : Vecteur3d(0, 1, 0)).

    Outputs:
    - force (Vecteur3d): La force calculée selon la distance au plan et les propriétés d'un ressort (en N).
    """
    n = n.norm()
    a = n ** pos
    b = n ** m
    dist = a - b
    temp = -dist * float(exp(-90000 * dist * dist))  # Dérivée d'une gaussienne
    force = ressort_simple(d=temp, k=20000)
    force = n * force
    return force




def cube(pos):
    """
    Cette fonction calcule la force exercée par un cube virtuel en fonction de la position donnée,
    en utilisant plusieurs plans (murs) modélisés comme des ressorts.

    Inputs:
    - pos (Vecteur3d): Position actuelle de l'interface ou de l'objet (en coordonnées 3D).

    Outputs:
    - force (Vecteur3d): La force totale exercée par le cube, résultant de l'interaction avec les six murs (en N).
    """
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

    #print(force.x)
    #peut generer des erreur si ancienne version de numpy
    force.x=np.minimum(np.maximum(force.x,-15),15)
    force.z=minimum(maximum(force.z,-15),15)
    force.y=minimum(maximum(force.y,-15),15)
    return force




def sphere(pos,center=Vecteur3d(0.00001,0.0000001,0.00001),rayon=0.04):
    
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
    
    #f_tan=-10*np.cos(f*pos**n)*n
    f_tan=ressort_simple(np.cos(f*pos**n)*n,k=10)
    f_colle=ressort_simple(f_colle,k=1000)
    force=f_colle+f_tan
    return force 

def mur_texture(pos,m=Vecteur3d(0.0,-0.02,0),n=Vecteur3d(0,1,0)):

    f=100
    n=n.norm()
    a=n**pos
    b=n**m
    dist=(a-b)#/n.mod()
    
    temp=-dist*float(exp(-90000*dist*dist))#derivee d'une gaussienne
    force=ressort_simple(d=temp,k=20000)
    force=n*force

    t=Vecteur3d(1,1,1)*n.norm()
    
    ftan=ressort_simple(np.cos(f*pos**t)*t,k=10)#pas besoin de s'inquieter au signe
    np.cos(f*pos**t)*t
    force=force + ftan
    
    return force


def cylindre(pos,c=Vecteur3d(0.000001,0.00000001,0.0000001),n=Vecteur3d(0,1,0),r=0.02,L=0.08):


    #incompleted
    forcen= sphere(pos,center=-0.5*L*n+Vecteur3d(0.00001,0.00001,0.00001),rayon=r) + sphere(pos,center=0.5*L*n+Vecteur3d(0.00001,0.00001,0.00001),rayon=r)

    n=n.norm()
    v=(pos-c)**n
    t=((pos-c) - v*n).norm()
    
    center=r*(t) + v*n #pos - 
    forcet=mur(pos,center,t)

    return  forcen + forcet


def char_calculator(period,raideur,x0,xi,i):

    """
    Cette fonction calcule la masse apparente du système et son amortissement.

    Inputs:
    - period (float): La période du système (en secondes).
    - raideur (float): La raideur du ressort (en N/m).
    - x0 (float): La position initiale (en cm).
    - xi (float): La position finale (en cm).
    - i (int): nombre d'ossillation.

    Outputs:
    - m (float): La masse apparente du système (en kg).
    - c (float): L'amortissement du système (en Ns/m).
    """

    alpha=np.log(x0/xi)/(2*np.pi*i)
    F=1/period
    omega=2*np.pi*F/(1-alpha**2)**0.5
    m=raideur/omega**2
    c=2*alpha*omega/m
    print('mass=',m)
    print('amortissement = ',c)

def vis2d(x_axis,y_axis,xlabel,ylabel,title,label):

    plt.figure(figsize=(8, 6))
    plt.plot(x_axis, y_axis, label=label, color="blue")#, marker="o"
    plt.axhline(0, color='black', linewidth=0.8, linestyle="--")
    plt.axvline(0, color='black', linewidth=0.8, linestyle="--")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()

def vis3d(X,Y,Z,title,xlabel,ylabel,zlabel):

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    #ax.quiver(X, Y, 0, forces_x, forces_y, 0, length=0.001, color='blue', normalize=False)  # 3D quiver plot for force vectors
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    plt.show()


def vis3d2(cloud_points,title,xlabel,ylabel,zlabel):
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(cloud_points[:, 0], cloud_points[:, 1], cloud_points[:, 2], c='b', s=1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    plt.show()

if __name__=='__main__':

    plt.close('all')
    
    ########Question 1###########
    '''
    #axe x
    period=0.283
    raideur=500
    x0=0.0812
    xi=8.8*10**-3
    i=2
    char_calculator(period,raideur,x0,xi,i)
    

    #axe y 
    period=0.151
    raideur=500
    x0=0.033
    xi=0.022
    i=3
    char_calculator(period,raideur,x0,xi,i)
    
    #axe z
    period=0.15
    raideur=500
    x0=0.0192
    xi=9.6*10**-3
    i=5
    char_calculator(period,raideur,x0,xi,i)
    '''

    ################# Question 2  mur #################################################
    '''   
    # Define the range for y positions
    y_positions = [i * 0.001 for i in range(-80, 80)]  # Values from -0.008 to 0.01 in steps of 0.0001
    x_positions = [i * 0.001 for i in range(-80, 80)]
    z_positions = [i * 0.001 for i in range(-80, 80)]
    X, Y = np.meshgrid(x_positions, y_positions)
    forces_mag = np.zeros((len(x_positions), len(y_positions)))
    cloud_point=[]
    forces_y = []
    forces_x=[]
    forces_z=[]


    for i,y in enumerate(y_positions):

        for l,x in enumerate(x_positions):
            
            for j,z in enumerate(z_positions):
                pos = Vecteur3d(x, y, z)
                force = mur(pos)  # Call the mur function
                force_mag=(force.x**2 + force.y**2 + force.z**2)**0.5 
                if force_mag > 15 :
                    cloud_point.append((x, y, z))

            #forces_mag[l][i] = np.sqrt(force.x**2 + force.y**2)
            forces_mag[i][l] = force.x + force.y

        forces_y.append(force.y) 
        forces_x.append(force.x)
        forces_z.append(force.z)
    
    cloud_point = np.array(cloud_point)

    vis2d(y_positions,forces_y,"y Position (m)","Force in y (N)","Force (y-component) vs Position (y)","Force (y-component)")
    vis3d(X,Y,forces_mag,"Force Components vs Position","X Position (m)","Y Position (m)","Force (N)")
    #vis3d2(cloud_point,"points where force mag > 10","X Position (m)","Y Position (m)","Z Position (m)")
    '''
    
    ################### Question tous objets ########################
    #'''
    y_positions = [i * 0.005 for i in range(-16, 16)]  # Values from -0.008 to 0.01 in steps of 0.0001
    x_positions = [i * 0.005 for i in range(-16, 16)]
    z_positions = [i * 0.005 for i in range(-16, 16)]
    X, Y = np.meshgrid(x_positions, y_positions)
    forces_mag = np.zeros((len(x_positions), len(y_positions)))
    cloud_point=[]

    for i,y in enumerate(y_positions):

        for l,x in enumerate(x_positions):
    
            for j,z in enumerate(z_positions):
                pos = Vecteur3d(x, y, z)     #fixer z ici pour visualiser l'espace x ,y a z fixe
                force=cube(pos)
                #force=sphere(pos)
                #force=glissiere(pos)
                #force=mur_texture(pos)
                #force=cylindre(pos)
                force_mag=(force.x**2 + force.y**2 + force.z**2)**0.5 
                if force_mag < 5:   #>7
                    cloud_point.append((x, y, z))

            if (abs(y)>0.03 or  abs(x)>0.03) or 1: #la pour les singularitees , a ca depend de l'origine des spheres //// abs(y)>0.03 or  abs(x)>0.03 ///// ((y**2 +x**2)>=0.0395**2) or
                forces_mag[i][l] = force.x + force.y
            else :
                forces_mag[i][l] = 0

    cloud_point = np.array(cloud_point)



    vis3d(X,Y,forces_mag,"Force Components vs Position","X Position (m)","Y Position (m)","Force (N)")
    vis3d2(cloud_point,"points where force mag > 7","X Position (m)","Y Position (m)","Z Position (m)")



    #'''
            