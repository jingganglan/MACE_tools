"""

data_cp2mace.py: A script to combine positions and forces from XYZ files into an extended XYZ file.

Author: Jinggang Lan
Date: May 21, 2024

Usage:
    python cp2mace.py -p name_of_positions.xyz -f name_of_forces.xyz -cell a b c alpha beta gamma -stride 10

Arguments:
    -p, --positions  Name of the positions XYZ file (required)
    -f, --forces     Name of the forces XYZ file (required)
    -cell            Cell dimensions: a b c alpha beta gamma (required)
    -stride          Stride for selecting frames (default: 1)
"""


import argparse
from ase.io import read, write
from ase.units import Hartree, Bohr

def main():
    parser = argparse.ArgumentParser(description='Process positions and forces.')
    parser.add_argument('-p', '--positions', type=str, required=True, help='Name of the positions XYZ file')
    parser.add_argument('-f', '--forces', type=str, required=True, help='Name of the forces XYZ file')
    parser.add_argument('-cell', nargs=6, type=float, required=True, help='Cell dimensions: a b c alpha beta gamma')
    parser.add_argument('-stride', type=int, default=1, help='Stride for selecting frames (default: 1)')

    args = parser.parse_args()

    # Read positions and forces from XYZ files
    positions = read(args.positions, index=':')  # Reads all frames if multiple
    forces = read(args.forces, index=':')  # Make sure this matches the structure of positions
    box = args.cell

    # Check if the number of atoms and frames match in both files
    assert len(positions) == len(forces), "Number of frames in positions and forces does not match"
    for pos, force in zip(positions, forces):
        assert len(pos) == len(force), "Number of atoms in positions and forces does not match"

    # Combine positions and forces into one file
    output_positions = []
    for i, (pos, force) in enumerate(zip(positions, forces)):
        if i % args.stride == 0:  # Write only every nth step
            pos.set_pbc([True, True, True])  # Set periodic boundary conditions to True for all dimensions
            pos.set_cell(box)  # Set the cell dimensions
            pos.new_array('REF_forces', force.get_positions() * Hartree / Bohr)  # Replace get_positions() with the appropriate method if needed
            energy = pos.info['E']
            pos.info['REF_energy'] = energy * Hartree
            del pos.info['E']
            del pos.info['time']
            del pos.info['i']
            output_positions.append(pos)

    # Write to a new extended XYZ file
    write('combined.extxyz', output_positions, format='extxyz')

if __name__ == "__main__":
    main()
