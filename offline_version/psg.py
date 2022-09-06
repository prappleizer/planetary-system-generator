import numpy as np 
import matplotlib.pyplot as plt
from pathlib import Path
import yaml 
import argparse


parser = argparse.ArgumentParser(description='Generate a Planetary System')
parser.add_argument('config_file',help='path to yml config file')
parser.add_argument("--output", help="output file name to save (by default, will by planet system name)",default=None)
parser.add_argument("--extension", help="extension for save (png or pdf); default: png.",type=str,default='png')
parser.add_argument("--style",type=str,default='light',help="style for output, either dark or light. default: light.")
args = parser.parse_args()

config_file =  args.config_file




hfont = {'fontname':'Arial Narrow','fontweight':'bold'}
tfont = {'fontname':'Impact'}




conf = yaml.safe_load(Path(config_file).read_text())
sys_name = conf['name']
planets = conf['planets']
asteroid_belts = conf['asteroid_belts']
style = args.style

def make_system(sys_name,planets,asteroid_belts=None,style='dark'):
    fig, ax = plt.subplots(figsize=(14,7.5),constrained_layout=True)
    
    ax.set_aspect('equal')
    if style == 'dark':
        fig.patch.set_facecolor('#030112')
        ax.set_facecolor('#030112')
        planetcolor='w'
    else:
        planetcolor='k'
    
    ax.set_ylim(-25,25)
    ax.set_xlim(0,110)
    ax.text(0.99,0.99,sys_name,va='bottom',ha='right',transform=ax.transAxes,fontsize=45,**tfont,color=planetcolor)
    ax.axis('off')

    
    ax.axhline(0,lw=3,color='gray',alpha=0.5,zorder=-1)

        

        
    circle1 = plt.Circle((-20, 0), 30, color=planetcolor)

    ax.add_patch(circle1)

    for p in planets.keys():
        pl = planets[p]
        if 'orbitals' in pl.keys():
            offset = pl['size'] + 0.5*((len(pl['orbitals'])-1)*pl['size'])
        else:
            offset=1
        ax.text(pl['dist'],pl['size']+offset,p,ha='center',va='bottom',fontsize=14,color=planetcolor,**hfont)
        c = plt.Circle((pl['dist'],0),pl['size'],color=planetcolor)
        ax.add_patch(c)
        if 'orbitals' in pl.keys():
            lc1 = pl['size'] + 0.5*((len(pl['orbitals']))*pl['size'])
            lc2 = 6
            
            lc = lc1 + lc2
            ax.plot([pl['dist'],pl['dist']],[0,-lc],lw=3,color='gray',alpha=0.5,zorder=-1)
            for i,n in enumerate(pl['orbitals']):
                ii = i+1
                r = pl['size'] + 0.5*((i+1)*pl['size'])
                circ = plt.Circle((pl['dist'],0),r,edgecolor=planetcolor,facecolor='None',lw=1.0)
                ax.add_patch(circ)
                c = plt.Circle((pl['dist'],-(lc2/len(pl['orbitals']))*ii-lc1),0.5,color=planetcolor)
                ax.add_patch(c)
                
                ax.text(pl['dist']+1,-(lc2/len(pl['orbitals']))*ii-lc1,n,fontsize=12,color=planetcolor,va='center')

    if asteroid_belts is not None:
        for belts in asteroid_belts.keys():
            belt = asteroid_belts[belts]
            if belt['density']=='low':
                nast = 50
            elif belt['density'] == 'medium':
                nast = 75
            elif belt['density'] == 'high':
                nast = 100
            elif belt['density'] == 'very high':
                nast = 170
            curve_amount = belt['width']
            fitt = np.polyfit([-30,0,30],[belt['dist']-curve_amount*belt['width'],belt['dist']+curve_amount*belt['width'],belt['dist']-curve_amount*belt['width']],2)
            pvals = np.polyval(fitt,np.linspace(-30,30,nast))
            ypositions = np.linspace(-30,30,nast)
            xpositions = pvals
            width_spread = np.random.normal(loc=0,scale=belt['width'],size=xpositions.shape)
            final_x = xpositions+width_spread
            height_spread = np.random.normal(loc=0,scale=2,size=ypositions.shape)
            final_y = ypositions+height_spread 
            
            
            
            size_spread = np.random.normal(loc=4,scale=5,size=final_y.shape)
            for i in range(len(final_y)):
                ax.plot(final_x[i],final_y[i],'o',ms=size_spread[i],color='gray')
            ax.text(belt['dist']+1.5,-24.5,belts,fontsize=15,color='gray')

        


    return fig, ax



if args.output is not None:
    fn = args.output + '.' + args.extension
else:
    fn = sys_name.replace(' ','_') + '.' + args.extension
fig, ax = make_system(sys_name,planets,asteroid_belts=asteroid_belts,style=style)


fig.savefig(fn,facecolor=fig.get_facecolor(), edgecolor='none')



