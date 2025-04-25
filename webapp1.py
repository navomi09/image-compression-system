import streamlit as st
import cv2
import numpy as np
from compression import rle_encode, huffman_encode
from decompression import rle_decode, huffman_decode
from PIL import Image

st.set_page_config(page_title="Embedded Image Compression", layout="wide")
st.title("📷 Embedded Image Compression System")

if 'image' not in st.session_state:
    st.session_state.image = None
if 'compressed_rle' not in st.session_state:
    st.session_state.compressed_rle = None
if 'compressed_huffman' not in st.session_state:
    st.session_state.compressed_huffman = None
if 'decompressed_image' not in st.session_state:
    st.session_state.decompressed_image = None
st.header("🎥 Live Webcam Capture")
webcam_frame = st.camera_input("Capture from Webcam")

if webcam_frame is not None:
    image = Image.open(webcam_frame)
    st.session_state.image = np.array(image)
    st.image(st.session_state.image, caption="Captured Image", use_column_width=True)

st.header("📁 Upload an Image File")
uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.session_state.image = np.array(image)
    st.image(st.session_state.image, caption="Uploaded Image", use_column_width=True)

if st.button("🔄Retake or Upload Another"):
    st.session_state.image = None
    st.session_state.compressed_rle = None
    st.session_state.compressed_huffman = None
    st.session_state.decompressed_image = None
    st.experimental_rerun()

if st.session_state.image is not None:
    st.header("Compression")
    gray_image = cv2.cvtColor(st.session_state.image, cv2.COLOR_RGB2GRAY)
    

    rle_data = rle_encode(gray_image)

    encoded_data, tree_root = huffman_encode(gray_image)
    huffman_data = {
        "data": encoded_data,
        "tree": tree_root,
        "shape": gray_image.shape
    }

    st.session_state.compressed_rle = rle_data
    st.session_state.compressed_huffman = huffman_data

    st.subheader("RLE Compressed Data")
    with st.expander("View RLE Data"):
        st.text_area("RLE Data", value=str(rle_data), height=300)

    st.subheader("Huffman Compressed Data")
    with st.expander("View Huffman Data"):
        st.text_area("Huffman Encoded Bits", value=str(huffman_data["data"]), height=200)

    st.header("Decompression")

    rle_decoded = rle_decode(rle_data, image_shape=gray_image.shape)
    st.session_state.decompressed_image = rle_decoded

    st.subheader("Decompressed Image Preview")
    st.image(rle_decoded, caption="Decompressed Image (RLE)", use_column_width=True)
