from ase.io import read, write
from ase.io import Trajectory
from tqdm import tqdm
for i in tqdm(Trajectory('md.traj')[:]):    
    write('md.xyz',i,append=True)
