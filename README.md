<!-- This document is auto-generated with generatereadme.py. Please do not edit this file directory and instad edit the script file. -->

# terriajs-scripts

Scripts for working with [terriajs](https://github.com/TerriaJS/terriajs) catalog files.

## Installing

```
python3 -m pip install git+https://github.com/ykiu/terriajs-scripts.git
```

## Usage

### `tjs share decode [-h] [--username USERNAME] [--password PASSWORD]`

```
Decodes a share URL into JSON. Reads from stdin and writes to stdout. 

example:
  $ echo https://pss-terria.com/#share=s-RBfZnezRe4XWXspi | tjs share decode
  {"initSources": {...}}

options:
  -h, --help           show this help message and exit
  --username USERNAME  Baisc authentication username
  --password PASSWORD  Baisc authentication password
```

### `tjs share encode [-h] [--base-url BASE_URL]`

```
Encodes a catalog item/init source/share data into a URL. Reads from stdin and writes to stdout.

example:
  $ cat item.json
  {"type": "3d-tiles", "name": "test", "url": "https://example.com/tileset.json"}
  $ cat item.json | tjs share encode --base-url=https://pss-terria.com
  https://pss-terria.com#start=%7B%22initSources%22%3A%5B%7B%22stratum%22%3A%...

options:
  -h, --help           show this help message and exit
  --base-url BASE_URL  The URL onto which to attach the share fragment. e.g. https://pss-
                       terria.com
```

### `tjs gzip [-h] source destination`

```
Gzipping directory contents.

example:
  $ tjs gzip path/to/source/directory path/to/destination/directory

positional arguments:
  source       The source directory.
  destination  The destination directory.

options:
  -h, --help   show this help message and exit
```

## Development

Running the command without building & installing:

```
python3 -m terriajsscripts.main
```

