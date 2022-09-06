import numpy as np 
import matplotlib.pyplot as plt

import streamlit as st 
import yaml 

st.set_page_config(layout="wide")
st.title('Planetary System Map Generator')
hfont = {'fontname':'Arial Narrow','fontweight':'bold'}
tfont = {'fontname':'Impact'}


test_str = """\
name: Farudan System
planets:
  Farudan:
    dist: 40
    size: 2 
    orbitals:
      - Farudan Station
      - Gia (M)
  Aliasi:
    dist: 60
    size: 6
  Mari: 
    dist: 20
    size: 1
  Halicon:
    dist: 85
    size: 4.5
    orbitals:
      - Deselctron Mining Station

asteroid_belts:
  Altar Belt:
    dist: 71
    width: 1.1
    density: high"""


planets = {
    'Farudan': {'dist':40,'size':2,'orbitals':['Farudan Station','Gia (M)']},
    'Aliasi': {'dist':60,'size':6},
    'Mari': {'dist':20,'size':1},
    'Halicon': {'dist':85,'size':4.5,'orbitals':['Deselctron Mining Station']}
}

asteroid_belts = {'Altar Belt':{'dist':71,'width':1.1,'density':'high'}}


#conf = yaml.safe_load(test_str)
#planets = conf['planets']
#asteroid_belts = conf['asteroid_belts']

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
            fitt = np.polyfit([-25,0,25],[belt['dist']-curve_amount*belt['width'],belt['dist']+curve_amount*belt['width'],belt['dist']-curve_amount*belt['width']],2)
            pvals = np.polyval(fitt,np.linspace(-25,25,nast))
            ypositions = np.linspace(-25,25,nast)
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


with st.sidebar.form("my_form"):
    st.write('To set up a planetary system, enter the relevant parameters below. The tool uses the YAML format. An example system is provided --- you need toplevel defintions for name (of the system), planets, and asteroid belts. Within those, you can further specify parameters, as shown.')
    st.write('The spacing/indents are a little hard to see here, so you might try typing up your inputs in another file and pasting.')
    user_input = st.text_area("Enter YML form Configuration Here", value=test_str,height=660)
    submitted = st.form_submit_button("Submit")

if submitted:
    config = yaml.safe_load(user_input)
    sys_name = config['name']
    planets = config['planets']
    asteroid_belts = config['asteroid_belts']
    fn = sys_name + '.png'
    fig, ax = make_system(sys_name,planets,asteroid_belts=asteroid_belts,style='light')
    fig.savefig(fn)
    st.pyplot(fig,dpi=300)
    

    with open(fn, "rb") as file:
        btn = st.download_button(
             label="Download image",
             data=file,
             file_name=fn,
             mime="image/png"
           )


