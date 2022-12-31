import logging
import os

import cv2
from PIL import Image


class VisualsScaler:
    SCALED_visual_QUALITY = 95  # could also be less, anything above q > 95 pointless...

    def __init__(self, unscaled_visuals, use_already_scaled_visuals=False):

        self.unscaled_visuals = unscaled_visuals
        self.use_already_scaled_visuals = use_already_scaled_visuals

        self.scaled_visuals = [f.split(".")[0] + "_scaled." + f.split(".")[1] for f in self.unscaled_visuals]

    def run(self):
        if not self.use_already_scaled_visuals:
            self.__remove_already_scaled_visuals()
            width, height = self.__get_width_hight_to_scale()
            self.__scale_visuals(width, height)
        else:
            logging.info("No visuals will be scaled. Using already scaled visuals.")

        logging.debug(f"Number of scaled visuals: {len(self.scaled_visuals)}")
        return self.scaled_visuals

    def __remove_already_scaled_visuals(self):
        logging.info("Removing all already scaled visuals...")
        scaled_visuals_to_remove = [img for img in os.listdir(os.getcwd()) if img.endswith(".jpg") and "scaled" in img]
        for visual_to_remove in scaled_visuals_to_remove:
            os.remove(visual_to_remove)
            logging.debug(f"Removed {visual_to_remove}")

    def __get_width_hight_to_scale(self, scale_type="fixed"):
        if scale_type == "fixed":  # height 1920 px ; aspect ratio 9:16
            height_to_scale = 1920
            width_to_scale = int(height_to_scale * 9 / 16)
        elif scale_type == "fit2smallest":  # scale all visuals to visual with smallest height
            width_to_scale = 1e9
            height_to_scale = 1e9
            for visual in self.unscaled_visuals:
                frame = cv2.imread(visual) # ToDo: also handle scaling of videos
                height, width, layers = frame.shape
                if height < height_to_scale:
                    height_to_scale = height
                    width_to_scale = width
        else:
            raise NotImplementedError(f"Scale Type {scale_type} not supported!!")

        logging.debug(f"visuals will be scaled to width {width_to_scale} / height {height_to_scale}")
        return width_to_scale, height_to_scale

    # ToDo: could be a static method
    # ToDo: implement scaling of videos
    def __scale_visuals(self, width, height):
        logging.info("About to scale visuals...")
        for file_name, new_filename in zip(self.unscaled_visuals, self.scaled_visuals):
            image = Image.open( file_name)
            new_image = image.resize((width, height))
            new_image.save(new_filename, quality=self.SCALED_visual_QUALITY)
            logging.debug(f"Saved scaled image {new_filename}")
        logging.info("Finished scaling of visuals!")
        return new_filename
