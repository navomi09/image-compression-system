import numpy as np
from collections import Counter, defaultdict
import heapq
def rle_encode(image):
    flat = image.flatten()
    encoded = []
    prev_pixel = flat[0]
    count = 1
    for pixel in flat[1:]:
        if pixel == prev_pixel:
            count += 1
        else:
            encoded.append((prev_pixel, count))
            prev_pixel = pixel
            count = 1
    encoded.append((prev_pixel, count))
    return encoded

class Node:
    def __init__(self, symbol=None, freq=None, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [Node(symbol=symbol, freq=freq) for symbol, freq in frequencies.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = Node(freq=node1.freq + node2.freq, left=node1, right=node2)
        heapq.heappush(heap, merged)
    return heap[0]

def generate_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node.symbol is not None:
        code_map[node.symbol] = prefix
    else:
        generate_codes(node.left, prefix + "0", code_map)
        generate_codes(node.right, prefix + "1", code_map)
    return code_map

def huffman_encode(image):
    flat = image.flatten()
    frequencies = Counter(flat)
    tree_root = build_huffman_tree(frequencies)
    code_map = generate_codes(tree_root)
    encoded_data = ''.join(code_map[pixel] for pixel in flat)
    return encoded_data, tree_root
