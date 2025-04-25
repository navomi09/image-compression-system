import cv2
import schedule
import time
import threading
from collections import defaultdict
from image_capture import load_image, capture_image
from compression import rle_encode, huffman_encode
from decompression import rle_decode, huffman_decode

app_tasks = defaultdict(dict)

def sample_task():
    print(" Running scheduled image compression task...")
    return "Task Executed!"

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler, daemon=True).start()

def main():
    print("\n1. Run-Length Encoding (RLE)")
    print("2. Huffman Encoding")
    print("3. Schedule a Compression Task")
    choice = input("Select Option: ")

    if choice in ["1", "2"]:
        image_path = input("Enter image file path or press enter to capture: ")
        image = load_image(image_path) if image_path else load_image(capture_image())

        if choice == "1":
            compressed_data = rle_encode(image)
            print(" RLE Compressed Data:", compressed_data[:50])
        else:
            encoded_data, huffman_codes, root = huffman_encode(image)
            print(" Huffman Compressed Data:", encoded_data[:50])

    elif choice == "3":
        interval = int(input("Enter scheduling interval (seconds): "))
        task_id = len(app_tasks) + 1
        schedule.every(interval).seconds.do(sample_task)
        app_tasks[task_id] = {"status": "Scheduled", "interval": interval}
        print(f" Task {task_id} scheduled every {interval} seconds!")

if __name__ == "__main__":
    main()
