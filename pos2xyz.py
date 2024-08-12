import sys
from ase.io import read, write
from ase.build import make_supercell

def convert_poscar_to_extxyz(input_file, output_file, supercell=(1, 1, 1)):
    # Load the POSCAR file
    atoms = read(input_file)

    # Create a supercell if specified
    atoms = atoms * supercell

    # Write to extxyz format
    write(output_file, atoms)

if __name__ == "__main__":
    if len(sys.argv) < 5 or len(sys.argv) > 11:
        print("Usage: python convert.py -i input_file -o output_file [-c a b c]")
        sys.exit(1)
    
    # Parse command-line arguments
    input_file = None
    output_file = None
    supercell = (1, 1, 1)

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '-i':
            input_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '-o':
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '-c':
            if i + 3 >= len(sys.argv):
                print("Error: Missing values for supercell dimensions")
                sys.exit(1)
            try:
                supercell = (int(sys.argv[i + 1]), int(sys.argv[i + 2]), int(sys.argv[i + 3]))
            except ValueError:
                print("Error: Supercell dimensions must be integers")
                sys.exit(1)
            i += 4
        else:
            print(f"Error: Unknown argument {sys.argv[i]}")
            sys.exit(1)

    if input_file is None or output_file is None:
        print("Error: Missing input or output file")
        sys.exit(1)

    # Convert POSCAR to extxyz with optional supercell
    convert_poscar_to_extxyz(input_file, output_file, supercell)
