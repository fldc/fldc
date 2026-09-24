import sys

import cv2

# ASCII characters from dark to light
ASCII_CHARS = "@#S%?*+;:,. "


def image_to_ascii_cv(image_path: str, width: int = 36) -> str:
    # Load image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Resize while maintaining aspect ratio
    height = int(img.shape[0] * (width / img.shape[1]) * 0.55)  # Adjust aspect ratio for text spacing
    img = cv2.resize(img, (width, height))

    # Enhance contrast using histogram equalization
    img = cv2.equalizeHist(img)

    # Convert each pixel to an ASCII character
    # Map 256 pixel values (0-255) to ASCII_CHARS indices (0-11)
    # Use min() to ensure we never exceed the array bounds
    ascii_str = "\n".join(
        "".join(ASCII_CHARS[min(p * len(ASCII_CHARS) // 256, len(ASCII_CHARS) - 1)] for p in row)
        for row in img
    )

    return ascii_str


if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else "portrait.jpg"
    print(image_to_ascii_cv(image_path))