import os

def join_files(input_directory, output_file):
    with open(output_file, 'wb') as output:
        chunk_number = 0
        while True:
            input_file = os.path.join(input_directory, f'chunk_{chunk_number}.npy')
            if not os.path.exists(input_file):
                break
            with open(input_file, 'rb') as input_chunk:
                output.write(input_chunk.read())
            chunk_number += 1

output_file = 'glove-wiki-gigaword-300.vectors.npy'
join_files("split_gigaword", output_file)