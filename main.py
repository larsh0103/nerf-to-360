import cv2
import numpy as np

def convert_to_equirectangular(img, fov_vertical, focal_length):
    height, width = img.shape[:2]
    eq_height = int(height * 360 / fov_vertical)
    eq_width = int(eq_height * 2)

    eq_img = np.zeros((eq_height, eq_width, 3), dtype=np.uint8)

    for v in range(eq_height):
        for u in range(eq_width):
            theta = 2 * np.pi * u / eq_width
            phi = np.pi * v / eq_height

            x = -np.sin(theta) * np.sin(phi)
            y = np.cos(phi)
            z = np.cos(theta) * np.sin(phi)

            x_img = -focal_length * x / z
            y_img = focal_length * y / z

            x_img = int(x_img + width / 2)
            y_img = int(y_img + height / 2)

            if 0 <= x_img < width and 0 <= y_img < height:
                eq_img[v, u] = img[y_img, x_img]

    return eq_img

def stitch_images(images):
    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    status, pano = stitcher.stitch(images)

    if status != cv2.Stitcher_OK:
        print("Error during stitching:", status)
        return None

    return pano

def main():
    # Assuming you have a list of filepaths to your images
    image_files = ['image1.jpg', 'image2.jpg', 'image3.jpg', ...]

    # Load images
    images = [cv2.imread(f) for f in image_files]

    # Convert images to equirectangular format
    fov_vertical = 180  # or 360
    focal_length = 500  # You may need to adjust this value
    equirectangular_images = [convert_to_equirectangular(img, fov_vertical, focal_length) for img in images]

    # Stitch images
    pano = stitch_images(equirectangular_images)

    if pano is not None:
        cv2.imwrite('panorama.jpg', pano)

if __name__ == "__main__":
    main()
