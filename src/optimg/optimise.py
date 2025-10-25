# -*- coding: utf-8 -*-
"""optimisation utilities for optimg"""
__copyright__ = "Copyright (c) 2025 https://github.com/davidohnee"


import os
import logging

from PIL import Image, ImageOps

logger = logging.getLogger(__name__)


def _parse_format(format_ext: str) -> str:
    """format extension"""
    format_ext = format_ext.lower()
    if format_ext == "jpg":
        format_ext = "jpeg"
    return format_ext


def optimise_image(
    image_path: str,
    output_dir: str,
    *,
    format_ext: str = "webp",
    max_res: int | None = None,
    resize_mode: str | None = "c",
    lossless: bool = False,
    quality: int = 80,
) -> str:
    """
    Optimise an image and save it to the output directory.

    :param image_path: Path to the input image.
    :param output_dir: Directory to save the optimised image.
    :param format_ext: Output image format extension (default: "webp").
    :param max_res: Maximum resolution (px) for resizing (default: None).
    :param resize_mode: Resize mode - "f" for fit & crop, "c" for contain (default: "c").
    :param lossless: Use lossless compression (webp only) (default: False).
    :param quality: Output image quality (1-100) or compression level if lossless (1-100).
    :return: Path to the optimised image.
    """
    # Open an image
    image = Image.open(image_path)

    # Resize the image
    if resize_mode is not None and max_res is not None:
        fixed_image = ImageOps.exif_transpose(image)
        if resize_mode == "f":
            logger.debug("Resizing image %s with fit & crop to %d px", image_path, max_res)
            image = ImageOps.fit(fixed_image, (max_res, max_res))
        elif resize_mode == "c":
            logger.debug("Resizing image %s with contain to %d px", image_path, max_res)
            image = ImageOps.contain(fixed_image, (max_res, max_res))

    file_wo_ext = os.path.splitext(os.path.basename(image_path))[0]
    output = os.path.join(output_dir, file_wo_ext + "." + format_ext)

    # Save the image
    try:
        logger.debug(
            "Saving image %s as %s with format %s, quality %d, lossless %s",
            image_path,
            output,
            _parse_format(format_ext),
            quality,
            lossless,
        )
        image.save(
            output,
            _parse_format(format_ext),
            optimize=True,
            quality=quality,
            lossless=lossless,
        )
        return output
    except OSError as e:
        if "RGBA" in str(e):
            logger.debug("Converting RGBA to RGB for %s", image_path)
            # Convert RGBA to RGB if format does not support alpha channel
            image = image.convert("RGB")
            image.save(
                output,
                _parse_format(format_ext),
                optimize=True,
                quality=quality,
                lossless=lossless,
            )
            return output
        else:
            logger.error("Error saving image %s: %s", image_path, e)
            raise e
