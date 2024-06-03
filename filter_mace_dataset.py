"""
filter_dataset.py: A script to filter frames from an XYZ file based on energy and force thresholds, and save the filtered frames to an extended XYZ file.

Author: Jinggang Lan
Date: June 3, 2024

Usage:
    python filter_dataset.py -i input_file.xyz -o output_file.extxyz [-e energy_threshold] [-f force_threshold]

Arguments:
    -i, --input              Input XYZ file path (required)
    -o, --output             Output XYZ file path (required)
    -e, --energy_threshold   Energy threshold (default: 0.5)
    -f, --force_threshold    Force threshold (default: 1)
"""


from ase.io import read, write
import numpy as np
import argparse

def read_xyz_with_threshold(file_path, energy_threshold, force_threshold):
    # Read the XYZ file
    frames = read(file_path, index=':')

    filtered_frames = []

    for frame in frames:
        REF_energy = frame.info.get('REF_energy')
        energy = frame.info.get('energy')
        REF_forces = frame.arrays.get('REF_forces')
        forces = frame.arrays.get('forces')
        
        # Calculate the energy error
        energy_error = abs(REF_energy - energy)
        
        # Calculate the forces difference
        forces_difference = np.linalg.norm(REF_forces - forces, axis=1).max()
        
        # Check if both the energy error and forces difference are within the thresholds
        if energy_error < energy_threshold and forces_difference < force_threshold:
            # Optionally remove the additional info
            del frame.info['energy']
            del frame.arrays['forces']
            filtered_frames.append(frame)
            
    return filtered_frames

def remove_energy_and_forces(frames):
    for frame in frames:
        # Remove 'energy' and 'forces' from info and arrays
        frame.info.pop('energy', None)
        frame.info.pop('free_energy', None)
        frame.info.pop('stress', None)
        frame.arrays.pop('forces', None)
        frame.set_array('forces', None)
        frame.set_calculator('None')
    return frames

def main():
    parser = argparse.ArgumentParser(description='Filter XYZ file based on energy and force thresholds.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input XYZ file path')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output XYZ file path')
    parser.add_argument('-e', '--energy_threshold', type=float, required=True, help='Energy threshold')
    parser.add_argument('-f', '--force_threshold', type=float, required=True, help='Force threshold')

    args = parser.parse_args()

    # Get the filtered frames
    filtered_frames = read_xyz_with_threshold(args.input, args.energy_threshold, args.force_threshold)

    # Save the filtered frames to a new .extxyz file
    write(args.output, remove_energy_and_forces(filtered_frames), format='extxyz')

    print(f"Filtered frames have been saved to {args.output}")

if __name__ == '__main__':
    main()
