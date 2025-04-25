import numpy as np
def rle_decode(compressed_data, image_shape=(256, 256)):
    """
    Decompresses RLE data.
    :param compressed_data: List of (pixel, count) tuples or [count1, value1, count2, value2...]
    :param image_shape: Tuple indicating final image shape.
    :return: Decoded image as a NumPy array.
    """
    decoded_pixels = []
    if isinstance(compressed_data[0], (list, tuple)) and len(compressed_data[0]) == 2:
        for pixel, count in compressed_data:
            decoded_pixels.extend([pixel] * count)
    else:
        i = 0
        while i < len(compressed_data):
            count = compressed_data[i]
            value = compressed_data[i + 1]
            decoded_pixels.extend([value] * count)
            i += 2

    return np.array(decoded_pixels, dtype=np.uint8).reshape(image_shape)

class Node:
    def __init__(self, symbol=None, left=None, right=None):
        self.symbol = symbol
        self.left = left
        self.right = right

def huffman_decode(encoded_data, tree_root, image_shape=(256, 256)):
    """
    Decompresses Huffman encoded data.
    :param encoded_data: A string of bits.
    :param tree_root: Root of the Huffman tree.
    :param image_shape: Tuple indicating final image shape.
    :return: Decoded image as a NumPy array.
    """
    decoded_pixels = []
    node = tree_root

    for bit in encoded_data:
        node = node.left if bit == '0' else node.right
        if node.symbol is not None:
            decoded_pixels.append(node.symbol)
            node = tree_root

    return np.array(decoded_pixels, dtype=np.uint8).reshape(image_shape)
