import os

import cv2
from PIL import Image


class ImageScaler:
    QUALITY = 95  # could also be less, anything above q > 95 pointless...

    def __init__(self, unscaled_images, working_dir, images_are_already_scaled=False):

        self.working_dir = working_dir
        self.unscaled_images = unscaled_images
        self.images_are_already_scaled = images_are_already_scaled

        self.scaled_images = []

    def run(self):
        if not self.images_are_already_scaled:
            self.__remove_already_scaled_images()
        width, height = self.__get_width_hight_to_scale()
        for image in self.unscaled_images:
            scaled_image = self.__scale_image(image, width, height)
            self.scaled_images.append(scaled_image)

        return self.scaled_images

    def __remove_already_scaled_images(self):
        print("Removing all already scaled images...")
        scaled_images_to_remove = [img for img in os.listdir(self.working_dir) if
                                   img.endswith(".jpg") and "scaled" in img]
        for image_to_remove in scaled_images_to_remove:
            filepath = os.path.join(self.working_dir, image_to_remove)
            os.remove(filepath)
            print(f"Removed {filepath}")

    def __get_width_hight_to_scale(self, scale_type="fixed"):
        if scale_type == "fixed":  # height 1920 px ; aspect ratio 9:16
            min_height = 1920
            min_width = int(min_height * 9 / 16)
            return min_width, min_height

        if scale_type == "fit2smallest":  # scale all images to image with smallest height
            min_width = 1e9
            min_height = 1e9
            for image in self.unscaled_images:
                frame = cv2.imread(os.path.join(self.working_dir, image))
                height, width, layers = frame.shape
                if height < min_height:
                    min_height = height
                    min_width = width

            return min_width, min_height

        raise NotImplementedError(f"Scale Type {scale_type} not supported!!")

    # ToDo: could be a static method
    # ToDO both scales images and gives the filenames...
    def __scale_image(self, file_name, width, height):
        basename = file_name.split(".")[0]
        suffix = file_name.split(".")[1]
        new_filename = basename + "_scaled." + suffix

        if not self.images_are_already_scaled:
            image = Image.open(os.path.join(self.working_dir, file_name))
            new_image = image.resize((width, height))
            path_scaled_image = os.path.join(self.working_dir, new_filename)
            new_image.save(path_scaled_image, quality=self.QUALITY)
            print(f"Wrote scaled file {path_scaled_image}")

        return new_filename
