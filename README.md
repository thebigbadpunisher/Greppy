# Greppy

Greppy is a Python tool for extracting URL parameters and paths from a list of URLs. It can also perform advanced parameter discovery by scraping HTML input tag names and JavaScript variable names from the URLs. The extracted information can be used for fuzzing and security testing.

## Features

- Extract URL query parameters.
- Extract URL paths.
- Scrape and extract HTML input tag names.
- Scrape and extract JavaScript variable names.
- Highlight extracted information with details when using the `--info` flag.
- Supports reading URLs from a file or from standard input (stdin) for use in pipelines.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/greppy.git
    ```
2. Navigate to the project directory:
    ```sh
    cd greppy
    ```
3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

```sh
usage: greppy.py [-h] -u URLS [-p] [-d] [-o OUTPUT] [-O] [--info]

Extract URL parameters or paths from a list of URLs.

optional arguments:
  -h, --help            show this help message and exit
  -u URLS, --urls URLS  Path to the input file containing URLs, or "-" to read from stdin.
  -p, --parameters      Flag to indicate parameter discovery mode.
  -d, --directories     Flag to indicate directory discovery mode.
  -o OUTPUT, --output OUTPUT
                        Path to the output file for extracted items.
  -O, --Output          Flag to indicate output directory mode.
  --info                Flag to include detailed information in the output.
