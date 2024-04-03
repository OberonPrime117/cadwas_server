import os

def split_file(input_file, output_directory, chunk_size):
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    with open(input_file, 'rb') as f:
        chunk_number = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            output_file = os.path.join(output_directory, f'chunk_{chunk_number}.npy')
            with open(output_file, 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk_number += 1

# Example usage
input_file = 'glove-wiki-gigaword-300.vectors.npy'
output_directory = 'split_gigaword'
chunk_size = 1024 * 1024  # 1 MB
split_file(input_file, output_directory, chunk_size)
