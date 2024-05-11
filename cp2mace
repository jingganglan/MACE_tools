import ase
from ase.io import read, write
from ase.units import Hartree, Bohr


# Read positions and forces from XYZ files
positions = read('positions.xyz', index=':')  # Reads all frames if multiple
forces = read('forces.xyz', index=':')  # Make sure this matches the structure of positions
box = [17,17,47,90,90,90]

# Check if the number of atoms and frames match in both files
assert len(positions) == len(forces), "Number of frames in positions and forces does not match"
for pos, force in zip(positions, forces):
    assert len(pos) == len(force), "Number of atoms in positions and forces does not match"

# Combine positions and forces into one file
output_positions = []
for i, (pos, force) in enumerate(zip(positions, forces)):
    if i % 1 == 0:  # Write only every 10th step
        pos.set_pbc([True, True, True])  # Set periodic boundary conditions to True for all dimensions
        pos.set_cell(box)  # Set the cell dimensions
        pos.new_array('REF_forces', force.get_positions()*Hartree/Bohr)  # Replace get_positions() with the appropriate method if needed
        energy = pos.info['E'] 
        pos.info['REF_energy'] = energy*Hartree
        del pos.info['E']
        del pos.info['time']
        del pos.info['i']
        output_positions.append(pos)


# Write to a new extended XYZ file
write('combined.extxyz', output_positions , format='extxyz')
