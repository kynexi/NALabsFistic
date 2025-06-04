from PIL import Image
import numpy as np

def load_image():
    path = "Lab1\\photo.jpg"
    try:
        img = np.array(Image.open(path))
        return img
    except Exception as e:
        print("Error loading image:", e)
        exit(1)

def rotation_img(img, angle):
    theta = np.radians(angle)
    cos = np.cos(theta)
    sin = np.sin(theta)
    rotation_matrix = np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
    height, width = img.shape[:2]
    new_width = int(np.round(height * np.abs(sin) + width * np.abs(cos)))
    new_height = int(np.round(width * np.abs(sin) + height * np.abs(cos)))

    cx, cy = width / 2, height / 2
    dx, dy = new_width / 2, new_height / 2
    center_matrix = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]])
    center_matrix_inv = np.array([[1, 0, -dx], [0, 1, -dy], [0, 0, 1]])

    affine_matrix = np.dot(np.dot(center_matrix, rotation_matrix), center_matrix_inv)
    rotated_img = np.zeros((new_height, new_width, 3), dtype=np.uint8)
    for y in range(new_height):
        for x in range(new_width):
            source_X, source_Y, _ = np.dot(affine_matrix, [x, y, 1]).astype(int)
            if 0 <= source_X < width and 0 <= source_Y < height:
                rotated_img[y, x, :] = img[source_Y, source_X, :]
    return rotated_img

def scale(img, scale_height, scale_width):
    original_height, original_width = img.shape[:2]
    scaled_image = np.zeros((scale_height, scale_width, img.shape[2]), dtype=np.uint8)

    for r in range(scale_height):
        for c in range(scale_width):
            scaled_r = int(original_height * r / scale_height)
            scaled_c = int(original_width * c / scale_width)
            scaled_image[r, c] = img[scaled_r, scaled_c]
            
    return scaled_image

def main():
    img = load_image()
    print("\nWhat would you like to do?")
    print("1 - Rotate")
    print("2 - Scale")
    print("3 - Rotate and Scale")
    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == "1":
        angle = int(input("Enter rotation angle (in degrees): "))
        rotated = rotation_img(img, angle)
        Image.fromarray(rotated).show()

    elif choice == "2":
        h = int(input("Enter new height (pixels): "))
        w = int(input("Enter new width (pixels): "))
        scaled = scale(img, h, w)
        Image.fromarray(scaled).show()

    elif choice == "3":
        angle = int(input("Enter rotation angle (in degrees): "))
        h = int(input("Enter new height (pixels): "))
        w = int(input("Enter new width (pixels): "))
        rotated = rotation_img(img, angle)
        scaled = scale(rotated, h, w)
        Image.fromarray(scaled).show()

    else:
        print("Invalid option. Exiting.")

if __name__ == "__main__":
    main()
