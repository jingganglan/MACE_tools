import os
import argparse
from ase.io import read, write
import numpy as np

def read_xyz(filename):
    return read(filename, format='xyz')

def read_energy(ref_out_file):
    energy = None
    with open(ref_out_file, 'r') as file:
        for line in file:
            if 'ENERGY| Total FORCE_EVAL ( QS ) energy [a.u.]:' in line:
                energy = float(line.split()[-1])
                break
    if energy is None:
        raise ValueError("Energy not found in the ref.out file.")
    return energy

def read_lattice(ref_inp_file):
    lattice = None
    with open(ref_inp_file, 'r') as file:
        for line in file:
            if 'ABC' in line:
                print(f"Found lattice line: {line.strip()}")  # Debug statement
                lattice = list(map(float, line.split()[1:]))
                break
    if lattice is None:
        print(f"Contents of {ref_inp_file}:")  # Debug statement
        with open(ref_inp_file, 'r') as file:
            print(file.read())  # Debug statement
        raise ValueError("Lattice parameters not found in the ref.inp file.")
    return lattice

def write_extxyz(atoms, energy, output_file):
    atoms.info['energy'] = energy
    write(output_file, atoms, format='extxyz')

def main():
    parser = argparse.ArgumentParser(description='Process some atomic data.')
    parser.add_argument('-i', '--input', required=True, help='Input XYZ file')
    parser.add_argument('-o', '--output', required=True, help='Output EXTXYZ file')
    parser.add_argument('-cp2k_in', default='ref.inp', help='Input CP2K file (default: ref.inp)')
    parser.add_argument('-cp2k_out', default='ref.out', help='Output CP2K file (default: ref.out)')

    args = parser.parse_args()

    xyz_file = args.input
    ref_out_file = args.cp2k_out
    ref_inp_file = args.cp2k_in
    output_file = args.output

    # Read XYZ file
    atoms = read_xyz(xyz_file)

    # Read energy from ref.out
    energy_au = read_energy(ref_out_file)
    energy_ev = energy_au * 27.2114  # Convert energy from a.u. to eV

    # Read lattice parameters from ref.inp
    lattice = read_lattice(ref_inp_file)
    atoms.set_cell(lattice)
    atoms.set_pbc(True)  # Set periodic boundary conditions to True

    # Assign zero forces to each atom
    forces = np.zeros((len(atoms), 3))
    atoms.arrays['REF_forces'] = forces

    # Write to extxyz format
    write_extxyz(atoms, energy_ev, output_file)

    print(f"XYZ data written to {output_file} with energy {energy_ev:.6f} eV, lattice {lattice}, and PBC set to True")

if __name__ == "__main__":
    main()
