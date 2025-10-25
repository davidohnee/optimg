# Optimg - A Simple Image Optimization Tool

Optimg is a command-line tool designed to optimise images for web use. It supports resizing, format conversion, and quality adjustment to help reduce file sizes while maintaining visual fidelity.

## Getting Started

To install Optimg, you can use pip:

```bash
pip install optimg
```

## Usage

Without any arguments, the tool will use default settings to optimise images in the current directory and save them to an `out` folder.

```bash
optimg
```

You can customize the optimisation process using various command-line options:

```bash
optimg -i path/to/images -o path/to/output --resize-mode c --max-res 1920 --format webp --quality 80 --lossless
```

You can disable resizing by setting `--resize-mode` to `n` (none):

```bash
optimg --resize-mode n
```

For more details on the available options, run:

```bash
optimg --help
```

Note that the `--lossless` option is only applicable when the output format is set to `webp`.
The quality parameter will then control the compression level for lossless webp images, where 100 is the most compression.

## Usage with Docker

You can also run Optimg using Docker. First, build the Docker image:

```bash
docker run -v ./in:/in -v ./out:/out ghcr.io/davidohnee/optimg:main --resize-mode n
```

Or use Docker Compose:

```bash
curl https://raw.githubusercontent.com/davidohnee/optimg/main/docker-compose.yml -o docker-compose.yml
docker compose up
```
