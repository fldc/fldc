import cv2
import numpy as np
from PIL import Image

# ASCII characters from dark to light
ASCII_CHARS = "@#S%?*+;:,. "  

def remove_background(image_path):
    img = cv2.imread(image_path)
    mask = np.zeros(img.shape[:2], np.uint8)

    # Background and foreground models (for GrabCut)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    # Define a rectangle around the subject (manual guess)
    height, width = img.shape[:2]
    rect = (10, 10, width-10, height-10)  # Start x, Start y, Width, Height

    # Apply GrabCut
    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

    # Convert mask: 0 & 2 -> Background, 1 & 3 -> Foreground
    mask = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
    img = img * mask[:, :, np.newaxis]  # Apply mask to the image

    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for ASCII
    
def image_to_ascii_cv(image_path, width=36):
    # Load image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Resize while maintaining aspect ratio
    height = int(img.shape[0] * (width / img.shape[1]) * 0.55)  # Adjust aspect ratio for text spacing
    img = cv2.resize(img, (width, height))

    # Enhance contrast using histogram equalization
    img = cv2.equalizeHist(img)

    #img = cv2.bitwise_not(img)  # Invert colors

    # Optional: Apply edge detection for better detail
    #img = cv2.Canny(img, threshold1=100, threshold2=200)

    # Convert each pixel to an ASCII character
    ascii_str = "\n".join("".join(ASCII_CHARS[p // 25] for p in row) for row in img)

    return ascii_str

ascii_art = image_to_ascii_cv("portrait.jpg")
print(ascii_art)