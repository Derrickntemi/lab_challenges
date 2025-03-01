import struct


def read_bitmap_image(file_path, bytes_len=None):
    """Reads a file using binary mode"""
    read_bytes = bytearray()
    with open(file_path, "rb") as f:
        read_bytes = f.read()
    if bytes_len is None:
        return read_bytes
    else:
        return read_bytes[:bytes_len]


def parse_bmp_header(header):
    """Attempts to extract information from a BMP header. The header is typically the first 54 bytes of the bitmap image. The header contains metadata such as the file signature, the size and the image width & height metadata.
    If the header of the image is not encrypted, it will start with the file signature BM, which is in hex is 0x42 0x4D"""
    if header[:2] != b"BM":
        print("The header is encrypted!")
        return

    # headers store values in little-endian format hence why the < byte order is used
    file_size = struct.unpack("<I", header[2:6])[0]
    pixel_data_offset = struct.unpack("<I", header[10:14])[0]
    width = struct.unpack("<I", header[18:22])[0]
    height = struct.unpack("<I", header[22:26])[0]
    bit_depth = struct.unpack("<H", header[28:30])[0]
    compression_status = struct.unpack("<I", header[30:34])[0]

    print(f"File Size: {file_size} bytes")
    print(f"Pixel Data Offset: {pixel_data_offset} bytes")
    print(f"Image Width: {width} pixels")
    print(f"Image Height: {height} pixels")
    print(f"Bit Depth: {bit_depth} bits per pixel")
    print(f"Compression Type: {compression_status}")


if __name__ == "__main__":
    header = read_bitmap_image("", 54)
    parse_bmp_header(header)
