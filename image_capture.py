import cv2

def load_image(file_path):
    """Loads an image from a given file path in color"""
    image = cv2.imread(file_path, cv2.IMREAD_COLOR) 
    return image

def capture_image():
    """Captures an image from the webcam in color"""
    cap = cv2.VideoCapture(0)  
    ret, frame = cap.read()  

    if ret:
        cv2.imwrite("captured_image.jpg", frame)  
        cap.release()
        cv2.destroyAllWindows()
        return "captured_image.jpg"  
    else:
        cap.release()
        cv2.destroyAllWindows()
        return None  # Return None if no image captured
