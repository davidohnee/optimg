# -*- coding: utf-8 -*-
"""directory utilities for optimg"""
__copyright__ = "Copyright (c) 2025 https://github.com/davidohnee"

import os
import re


def get_images_in_dir(input_dir: str) -> list[str]:
    """get images in dir"""
    files = os.listdir(input_dir)
    matching_files = [
        file
        for file in files
        if re.match(r".*\.(jpg|jpeg|png|gif|bmp|tiff|tif|webp)$", file, re.IGNORECASE)
    ]
    return matching_files


def ensure_dir_exists(dir_path: str) -> None:
    """ensure directory exists"""
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
