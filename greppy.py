#!/usr/bin/python3
import argparse
from urllib.parse import urlparse, parse_qs
import re
import aiohttp
import asyncio
import sys
from bs4 import BeautifulSoup

# ASCII Art
ASCII_ART = """
 ▄▄ • ▄▄▄  ▄▄▄ . ▄▄▄· ▄▄▄· ▄· ▄▌
▐█ ▀ ▪▀▄ █·▀▄.▀·▐█ ▄█▐█ ▄█▐█▪██▌
▄█ ▀█▄▐▀▀▄ ▐▀▀▪▄ ██▀· ██▀·▐█▌▐█▪
▐█▄▪▐█▐█•█▌▐█▄▄▌▐█▪·•▐█▪·• ▐█▀·.
·▀▀▀▀ .▀  ▀ ▀▀▀ .▀   .▀     ▀ •
                       -@nischalxd
"""

def extract_parameters(urls):
    parameters = set()
    for url in urls:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        parameters.update(query_params.keys())
    return parameters

def extract_paths(urls):
    paths = set()
    for url in urls:
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split('/') if part]
        paths.update(path_parts)
    return paths

async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                return None
    except Exception:
        return None

def extract_js_variables(html_content):
    js_variables = re.findall(r'(?:var|let|const)\s+([\w$]+)\s*=?\s*(?::\s*\[\]|\{\}|=\s*(?:(?:(["\']).*?\2)|(?:[^;,]+)))?;', html_content)
    return [name for name, _ in js_variables]

def extract_input_names(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    input_tags = soup.find_all('input', {'name': True})
    return [tag['name'] for tag in input_tags]

async def process_url(session, url, unique_input_names, unique_js_variables):
    html_content = await fetch_url(session, url)
    if html_content:
        input_names = extract_input_names(html_content)
        js_variables = extract_js_variables(html_content)
        unique_input_names.update(input_names)
        unique_js_variables.update(js_variables)

async def extract_parameters_from_html(urls):
    unique_input_names = set()
    unique_js_variables = set()
    async with aiohttp.ClientSession() as session:
        tasks = [process_url(session, url.strip(), unique_input_names, unique_js_variables) for url in urls]
        await asyncio.gather(*tasks)
    return unique_input_names, unique_js_variables

def main(urls_file, output_file=None, parameters=False, directories=False, output_dir=False, info=False):
    print(ASCII_ART)  # Print ASCII art
    if urls_file == '-':
        urls = [line.strip() for line in sys.stdin if line.strip()]
    else:
        with open(urls_file, 'r') as infile:
            urls = [line.strip() for line in infile if line.strip()]

    param_items = set()
    path_items = set()
    input_names = set()
    js_variables = set()

    if parameters:
        param_items = extract_parameters(urls)
        additional_input_names, additional_js_variables = asyncio.run(extract_parameters_from_html(urls))
        input_names.update(additional_input_names)
        js_variables.update(additional_js_variables)

    if directories:
        path_items = extract_paths(urls)

    if output_file:
        with open(output_file, 'w') as outfile:
            if info:
                if parameters:
                    for item in sorted(param_items):
                        outfile.write(f"{item} [\033[95mparameter\033[0m]\n")
                    for item in sorted(input_names):
                        outfile.write(f"{item} [\033[92minput\033[0m]\n")
                    for item in sorted(js_variables):
                        outfile.write(f"{item} [\033[93mjs_variable\033[0m]\n")
                if directories:
                    for item in sorted(path_items):
                        outfile.write(f"{item} [\033[94mdirectory\033[0m]\n")
            else:
                if parameters:
                    for item in sorted(param_items):
                        outfile.write(f"{item}\n")
                    for item in sorted(input_names):
                        outfile.write(f"{item}\n")
                    for item in sorted(js_variables):
                        outfile.write(f"{item}\n")
                if directories:
                    for item in sorted(path_items):
                        outfile.write(f"{item}\n")
    elif output_dir:
        if parameters:
            with open("parameters.txt", 'w') as outfile:
                if info:
                    for item in sorted(param_items):
                        outfile.write(f"{item} [\033[95mparameter\033[0m]\n")
                    for item in sorted(input_names):
                        outfile.write(f"{item} [\033[92minput\033[0m]\n")
                    for item in sorted(js_variables):
                        outfile.write(f"{item} [\033[93mjs_variable\033[0m]\n")
                else:
                    for item in sorted(param_items):
                        outfile.write(f"{item}\n")
                    for item in sorted(input_names):
                        outfile.write(f"{item}\n")
                    for item in sorted(js_variables):
                        outfile.write(f"{item}\n")
        if directories:
            with open("directories.txt", 'w') as outfile:
                if info:
                    for item in sorted(path_items):
                        outfile.write(f"{item} [\033[94mdirectory\033[0m]\n")
                else:
                    for item in sorted(path_items):
                        outfile.write(f"{item}\n")
    else:
        if info:
            if parameters:
                for item in sorted(param_items):
                    print(f"{item} [\033[95mparameter\033[0m]")
                for item in sorted(input_names):
                    print(f"{item} [\033[92minput\033[0m]")
                for item in sorted(js_variables):
                    print(f"{item} [\033[93mjs_variable\033[0m]")
            if directories:
                for item in sorted(path_items):
                    print(f"{item} [\033[94mdirectory\033[0m]")
        else:
            if parameters:
                for item in sorted(param_items):
                    print(item)
                for item in sorted(input_names):
                    print(item)
                for item in sorted(js_variables):
                    print(item)
            if directories:
                for item in sorted(path_items):
                    print(item)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract URL parameters or paths from a list of URLs.')
    parser.add_argument('-u', '--urls', required=True, help='Path to the input file containing URLs, or "-" to read from stdin.')
    parser.add_argument('-p', '--parameters', action='store_true', help='Flag to indicate parameter discovery mode.')
    parser.add_argument('-d', '--directories', action='store_true', help='Flag to indicate directory discovery mode.')
    parser.add_argument('-o', '--output', help='Path to the output file for extracted items.')
    parser.add_argument('-O', '--Output', action='store_true', help='Flag to indicate output directory mode.')
    parser.add_argument('--info', action='store_true', help='Flag to include detailed information in the output.')

    args = parser.parse_args()

    if args.parameters or args.directories:
        main(args.urls, args.output, args.parameters, args.directories, args.Output, args.info)
    else:
        print("Error: Please specify either --parameters or --directories.")
