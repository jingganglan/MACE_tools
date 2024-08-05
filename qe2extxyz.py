import argparse
from ase.io import read, write

def convert_qe_to_extxyz(input_file, output_file):
    # Read the Quantum ESPRESSO output file
    atoms = read(input_file, format='espresso-out')

    # Write to an extxyz file
    write(output_file, atoms, format='extxyz')

    print(f"Conversion complete: {input_file} -> {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert Quantum ESPRESSO output to extxyz format.")
    parser.add_argument('-i', '--input', required=True, help='Path to the Quantum ESPRESSO output file')
    parser.add_argument('-o', '--output', required=True, help='Path to the output extxyz file')

    args = parser.parse_args()

    convert_qe_to_extxyz(args.input, args.output)

if __name__ == "__main__":
    main()
