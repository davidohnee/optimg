# -*- coding: utf-8 -*-
"""optimg main"""
__copyright__ = "Copyright (c) 2025 https://github.com/davidohnee"

import os
import logging
import argparse
from tqdm import tqdm
from .optimise import optimise_image
from .dir import ensure_dir_exists, get_images_in_dir

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_args() -> argparse.Namespace:
    """get arguments"""
    parser = argparse.ArgumentParser(description="Optimise images")
    parser.add_argument("--input-dir", "-i", type=str, default="./", help="Input dir")
    parser.add_argument("--output-dir", "-o", type=str, default="./out/", help="Output dir")
    parser.add_argument(
        "--resize-mode",
        type=str,
        default=None,
        help="Type [f]it & crop or [c]ontain",
        choices=["f", "c", None],
    )
    parser.add_argument("--max-res", type=int, default=2560, help="Max resolution (px)")
    parser.add_argument("--format", "-f", type=str, default="webp", help="Output image format")
    parser.add_argument(
        "--quality",
        type=int,
        default=100,
        help="Output image quality (1-100) or compression level if lossless (1-100)",
    )
    parser.add_argument(
        "--lossless", action="store_true", help="Use lossless compression (webp only)"
    )
    return parser.parse_args()


def main() -> None:
    """main"""
    args = _get_args()

    input_dir: str = args.input_dir
    output_dir: str = args.output_dir

    ensure_dir_exists(output_dir)
    files = get_images_in_dir(input_dir)

    # max_res specified but resize_mode not specified
    if args.max_res is not None and args.resize_mode is None:
        args.resize_mode = "c"
        logger.info("Auto setting resize mode to 'c' (contain). Use --resize-mode to override.")

    if args.lossless and args.format.lower() != "webp":
        logger.warning("Lossless option is only supported for webp format. Ignoring --lossless.")

    for file in tqdm(files, desc="Optimising images"):
        optimise_image(
            os.path.join(input_dir, file),
            output_dir,
            format_ext=args.format,
            max_res=args.max_res,
            resize_mode=args.resize_mode,
            quality=args.quality,
            lossless=args.lossless,
        )


if __name__ == "__main__":
    main()
