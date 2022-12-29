import logging
import os

import cv2
from PIL import Image


class ImageScaler:
    SCALED_IMAGE_QUALITY = 95  # could also be less, anything above q > 95 pointless...

    def __init__(self, unscaled_images, working_dir, use_already_scaled_images=False):

        self.working_dir = working_dir
        self.unscaled_images = unscaled_images
        self.use_already_scaled_images = use_already_scaled_images

        self.scaled_images = [f.split(".")[0] + "_scaled." + f.split(".")[1] for f in self.unscaled_images]

    def run(self):
        if not self.use_already_scaled_images:
            self.__remove_already_scaled_images()
            width, height = self.__get_width_hight_to_scale()
            self.__scale_images(width, height)

        logging.debug(f"Number of scaled images: {len(self.scaled_images)}")
        return self.scaled_images

    def __remove_already_scaled_images(self):
        logging.info("Removing all already scaled images...")
        scaled_images_to_remove = [img for img in os.listdir(self.working_dir) if
                                   img.endswith(".jpg") and "scaled" in img]
        for image_to_remove in scaled_images_to_remove:
            filepath = os.path.join(self.working_dir, image_to_remove)
            os.remove(filepath)
            logging.debug(f"Removed {filepath}")

    def __get_width_hight_to_scale(self, scale_type="fixed"):
        if scale_type == "fixed":  # height 1920 px ; aspect ratio 9:16
            height_to_scale = 1920
            width_to_scale = int(height_to_scale * 9 / 16)
        elif scale_type == "fit2smallest":  # scale all images to image with smallest height
            width_to_scale = 1e9
            height_to_scale = 1e9
            for image in self.unscaled_images:
                frame = cv2.imread(os.path.join(self.working_dir, image))
                height, width, layers = frame.shape
                if height < height_to_scale:
                    height_to_scale = height
                    width_to_scale = width
        else:
            raise NotImplementedError(f"Scale Type {scale_type} not supported!!")

        logging.debug(f"Images will be scaled to width {width_to_scale} / height {height_to_scale}")
        return width_to_scale, height_to_scale

    # ToDo: could be a static method
    def __scale_images(self, width, height):
        logging.info("About to scale images...")
        for file_name, new_filename in zip(self.unscaled_images, self.scaled_images):
            image = Image.open(os.path.join(self.working_dir, file_name))
            new_image = image.resize((width, height))
            path_scaled_image = os.path.join(self.working_dir, new_filename)
            new_image.save(path_scaled_image, quality=self.SCALED_IMAGE_QUALITY)
            logging.debug(f"Saved scaled image {path_scaled_image}")
        logging.info("Finished scaling of images!")
        return new_filename
