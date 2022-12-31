import logging
import os

import cv2
from PIL import Image
from moviepy import editor as mpe

from filename_helpers import is_image, is_video, get_lower_case_file_suffix


class VisualsScaler:
    SCALED_IMAGE_QUALITY = 95  # could also be less, anything above q > 95 pointless...

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
        scaled_visuals_to_remove = [vis for vis in os.listdir(os.getcwd())
                                    if (is_video(vis) or is_image(vis)) and "scaled" in vis]

        for visual_to_remove in scaled_visuals_to_remove:
            os.remove(visual_to_remove)
            logging.debug(f"Removed {visual_to_remove}")

    def __get_width_hight_to_scale(self, scale_type="fixed"):
        if scale_type == "fixed":  # height 1920 px ; aspect ratio 9:16
            height_to_scale = 200  # ToDo: set back to 1920
            width_to_scale = int(height_to_scale * 9 / 16)
        elif scale_type == "fit2smallest":  # scale all visuals to visual with smallest height
            width_to_scale = 1e9
            height_to_scale = 1e9
            for visual in self.unscaled_visuals:
                frame = cv2.imread(visual)  # ToDo: also handle scaling of videos
                height, width, layers = frame.shape
                if height < height_to_scale:
                    height_to_scale = height
                    width_to_scale = width
        else:
            raise NotImplementedError(f"Scale Type {scale_type} not supported!!")

        logging.debug(f"visuals will be scaled to width {width_to_scale} / height {height_to_scale}")
        return width_to_scale, height_to_scale

    # ToDo: could be a static method
    def __scale_visuals(self, width, height):
        logging.info("About to scale visuals...")
        for unscaled_visual, scaled_visual in zip(self.unscaled_visuals, self.scaled_visuals):
            if is_image(unscaled_visual):
                image = Image.open(unscaled_visual)
                new_image = image.resize((width, height))
                new_image.save(scaled_visual, quality=self.SCALED_IMAGE_QUALITY)
                logging.debug(f"Saved scaled image {scaled_visual}")
            elif is_video(unscaled_visual):
                # ToDo: only downsclaing works, so higher resolution images may make a problem --> throw exception
                clip = mpe.VideoFileClip(unscaled_visual)
                clip_resized = clip.resize(height=height,
                                           width=width)
                clip_resized.write_videofile(scaled_visual, codec='libx264')  # codec libx264 only for mp4 ?
                logging.debug(f"Saved scaled video {scaled_visual}")
            else:
                file_suffix = get_lower_case_file_suffix(unscaled_visual)
                raise IOError(f"Scaling not implemented for files of type '{file_suffix}'. "
                              f"File {unscaled_visual} cannot be scaled!")

            logging.info("Finished scaling of visuals!")
