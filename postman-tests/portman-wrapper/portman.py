from contextlib import contextmanager
from pathlib import Path
import argparse
import logging
import os
import subprocess
import re

def run_portman(input_file: str, output_file: str, *args):
    cmd = ['portman', '-l', input_file, '-o', output_file] + list(args)
    logging.debug(f"run_portman command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("api", type=str, help="path to the source OpenAPI-spec")
    parser.add_argument("-o", "--output", type=str, help="output path of the genereated postman test collection")
    parser.add_argument("-c", "--conf-portman", type=str, help="path to a portman config that overrides the default")
    parser.add_argument("--loglevel", choices=["DEBUG", "INFO", "ERROR"], default="INFO")

    return parser.parse_known_args()

@contextmanager
def cwd(path):
    """ Temporarily change directory
    """
    oldpwd=Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)

def validate_api(api_file: str):
    cmd = ['swagger-cli', 'validate', api_file]
    logging.debug(f"validate_api command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def bundle_api(api_file: str, output: Path):
    output_type = str(output.suffix[1:])
    cmd = ['swagger-cli', 'bundle',  api_file, '-r', '-t', output_type , '-o', str(output)]
    logging.debug(f"bundle_api command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def pre_process(api: Path) -> Path:
    output_path = Path.cwd() / 'api_bundled.yaml'
    with cwd(api.parent):
        validate_api(api.name)
        bundle_api(api.name, output_path)
    return output_path

def post_process(output: Path) -> int:
    """
    Portman (or rather, openapi-to-portman) injects unwanted 'maxItems' properties
    into array schemas. We remove those by matching a regular expression.
    """
    contents = output.read_text()
    processed_contents, n_subs = re.subn(',?\\\\"maxItems\\\\":[0-9]+', '', contents)
    output.write_text(processed_contents)
    return n_subs


def main():
    args, extra_args = parse_args()

    logging.basicConfig(level=args.loglevel)
    logging.debug(f"{args=}; {extra_args=}")
    input = Path(args.api)
    output = args.output

    if not input.is_file():
        raise FileNotFoundError(f'{input} is not a file')
    logging.info(f"API file: {input}")

    if output is None:
        output_name = input.stem + '.json'
        output = Path.cwd() / output_name
    else:
        output = Path(args.output)

    if Path(args.conf_portman).is_file():
        extra_args = ['-c', args.conf_portman] + extra_args

    bundled_input = pre_process(input)
    run_portman(str(bundled_input), str(output), *extra_args)
    logging.info(f"Postman test suite geterated")
    n_subs = post_process(output)
    logging.info(f"Made {n_subs} substitutions in the generated Postman collection")

    logging.info(f"Postman collection written to {output}")

if __name__ == "__main__":
    main()