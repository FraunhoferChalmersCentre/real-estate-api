from pathlib import Path
import argparse
import logging
import subprocess
import re

def run_portman(input_file: str, output_file: str, *args):
    cmd = ['portman', '-l', input_file, '-o', output_file] + list(args)
    logging.debug(f"Portman command: {cmd}")
    resp = subprocess.run(cmd, check=True)
    logging.debug(f"Portman return code: {resp.returncode}")

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("api", type=str, help="path to the source OpenAPI-spec")
    parser.add_argument("-o", "--output", type=str, help="output path of the genereated postman test collection")
    parser.add_argument("-c", "--conf-portman", type=str, help="path to a portman config that overrides the default")
    parser.add_argument("--loglevel", choices=["DEBUG", "INFO", "ERROR"], default="INFO")

    return parser.parse_known_args()

def post_process(output: Path) -> int:
    """
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

    if output is None:
        output_name = input.stem + '.json'
        output = Path.cwd() / output_name
    else:
        output = Path(args.output)

    if Path(args.conf_portman).is_file():
        extra_args = ['-c', args.conf_portman] + extra_args

    run_portman(str(input), str(output), *extra_args)
    logging.info(f"Postman test suite geterated")
    n_subs = post_process(output)
    logging.info(f"Made {n_subs} substitutions in the generated Postman collection")

    logging.info(f"Postman collection written to {output}")

if __name__ == "__main__":
    main()