from ase.io import iread, write
import random

def process_large_xyz(file_path, output_file_path, n=None, indices=None):
    """
    Efficiently process a large XYZ file to select and save snapshots.

    :param file_path: Path to the input XYZ file.
    :param output_file_path: Path to the output XYZ file.
    :param n: Number of snapshots to randomly select (use None if using indices).
    :param indices: Specific indices of snapshots to select (use None if using random selection).
    """
    # Determine total number of frames in the trajectory
    total_frames = sum(1 for _ in iread(file_path))

    # Decide which frames to keep
    if indices is not None:
        selected_indices = set(indices)
    elif n is not None:
        selected_indices = set(random.sample(range(total_frames), n))
    else:
        raise ValueError("Either n or indices must be provided.")

    # Process and write selected frames
    with open(output_file_path, 'w') as outfile:
        for i, atoms in enumerate(iread(file_path)):
            if i in selected_indices:
                write(outfile, atoms, format='xyz', append=True)

# Path to your input XYZ file
input_file_path = 'md.xyz'
# Path to your output XYZ file
output_file_path = 'selected_snapshots.xyz'

# Number of snapshots to randomly select (set to None if using indices)
n = 5
# Specific indices of snapshots to select (set to None if using random selection)
indices = None

# Process the large XYZ file
process_large_xyz(input_file_path, output_file_path, n=n, indices=indices)
