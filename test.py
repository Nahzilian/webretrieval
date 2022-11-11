import argparse
import gzip
import os
import itertools

from typing import BinaryIO, Iterator

CHUNK_SIZE = 4096  # bytes


def megabytes_to_bytes(megabytes: int) -> int:
    return megabytes * 1024 * 1024


def chunk_sizes(total_bytes: int, chunk_size: int) -> Iterator[int]:
    for _ in range(total_bytes // chunk_size):
        yield chunk_size

    if remaining_bytes := total_bytes % chunk_size:
        yield remaining_bytes


class FileSplitter:
    input_file_path: str
    output_directory: str
    output_file_base_name: str
    split_size: int  # size of each partition, in MB

    def __init__(
        self, input_file_path: str, output_directory: str, split_size: int
    ) -> None:
        self.input_file_path = input_file_path
        self.output_directory = output_directory
        name = os.path.basename(input_file_path)
        name_without_file_extension = os.path.splitext(name)[0]
        self.output_file_base_name = name_without_file_extension
        self.split_size = split_size

    def get_new_file(self, file_number: int) -> BinaryIO:
        new_file_name = f"{self.output_file_base_name}.{file_number}"
        new_file_path = os.path.join(self.output_directory, new_file_name)
        return open(new_file_path, "wb")

    def split(self) -> None:
        bytes_per_file = megabytes_to_bytes(self.split_size)
        os.makedirs(self.output_directory, exist_ok=True)

        with gzip.open(self.input_file_path, mode="rb") as in_file:
            for file_number in itertools.count(start=1, step=1):
                with self.get_new_file(file_number) as out_file:
                    for chunk_size in chunk_sizes(bytes_per_file, CHUNK_SIZE):
                        chunk = in_file.read(chunk_size)
                        # chunk == "" means we finished reading the input file
                        if not chunk:
                            return
                        out_file.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read a gzip-compressed file "
        "and split its uncompressed contents into separate files."
    )
    parser.add_argument(
        "file_name", help="a gzip-compressed file, e.g. foo.gz"
    )
    parser.add_argument(
        "--size",
        type=int,
        default=500,
        help="desired size of each partition, in MB",
    )
    args = parser.parse_args()

    output_directory = os.path.join(os.getcwd(), "pychunks")
    splitter = FileSplitter(args.file_name, output_directory, args.size)
    splitter.split()
