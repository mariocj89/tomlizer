import pathlib
from typing import Optional

import coloredlogs
import toml

from . import setup_py
from .cli import parse_args


def _convert(
    *, input_file: pathlib.Path, existing_config: Optional[dict] = None
) -> dict:
    result = {}
    if existing_config:
        result.update(existing_config)

    if input_file.name == "setup.py":
        data = setup_py.transformer.extract(input_file)
        # TODO: Merge with existing data
        result.update(data)

    return result


def main(argv):
    args = parse_args(argv)
    coloredlogs.install(level="INFO", fmt="%(message)s")
    output_file = pathlib.Path("pyproject.toml")

    existing_config = None
    if output_file.exists():
        existing_config = toml.loads(output_file.read_text())

    result = _convert(
        input_file=args.input_file,
        existing_config=existing_config,
    )
    output = toml.dumps(result)
    output_file.write_text(output)
