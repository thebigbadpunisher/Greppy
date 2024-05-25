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
    git clone https://github.com/thebigbadpunisher/greppy.git
    ```
2. Navigate to the project directory:
    ```sh
    cd greppy
    ```
3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```
4. Give executable permissions:
    ```sh
    chmod +x greppy.py
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
```

## Examples:

### Extracting Parameters: 

#### From a File
To extract parameters from a list of URLs stored in a file (`urls.txt`):
```python
./greppy.py -u urls.txt -p
```

#### From Standard Input
To extract parameters from a list of URLs provided through standard input:
```python
cat urls.txt | ./greppy.py -u- -p
```

### Extracting Directories: 

#### From a File
To extract directories from a list of URLs stored in a file (`urls.txt`):
```python
./greppy.py -u urls.txt -d
```

#### From Standard Input
To extract directories from a list of URLs provided through standard input:
```python
cat urls.txt | ./greppy.py -u- -d
```

### Extracting Parameters and Directories with Detailed Information: 

#### From a File
To extract both parameters and directories from a list of URLs stored in a file (`urls.txt`) and include detailed information:
```python
./greppy.py -u urls.txt -p -d --info
```

#### From Standard Input
To extract both parameters and directories from a list of URLs provided through standard input and include detailed information:
```python
cat urls.txt | ./greppy.py -u- -p -d --info
```

### Writing Output to a File: 

#### Extracting Parameters and Saving to `output.txt`
To extract parameters and save the results to `output.txt`:
```python
./greppy.py -u urls.txt -p -o output.txt
```

#### Extracting Directories and Saving to `directories.txt`
To extract directories and save the results to `directories.txt`:
```python
./greppy.py -u urls.txt -d -o directories.txt
```

#### Extracting Parameters and Directories with Detailed Information and Saving to `output.txt`
To extract both parameters and directories, include detailed information, and save the results to `output.txt`:
```python
./greppy.py -u urls.txt -pd --info -o output.txt
```

#### Writing Output to Separate Files Using -O
To extract parameters and directories and write them to separate files (parameters.txt and directories.txt):
```python
./greppy.py -u urls.txt -p -d -O
```
