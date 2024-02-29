#!/usr/bin/env python3
import subprocess
import shlex
import re
import json
from typing import List, Tuple

import click

DEP_PATTERN = re.compile(r'Inst (\S+) \((\S+).+\)')


def list_deps(package: str) -> List[Tuple[str, str]]:
    proc = subprocess.Popen(['docker', 'run', '--rm', 'ubuntu:20.04', 'sh', '-c', f'apt update && apt install --dry-run -y {package}'], stdout=subprocess.PIPE)
    deps = []
    for line in proc.stdout:
        print(line.decode(),end='')
        match = DEP_PATTERN.match(line.decode())
        if match is not None:
            deps.append(match.groups())
    proc.wait()
    return deps


@click.command()
@click.argument("package", required=True)
def main(package):
    deps = list_deps(package)
    with open(f'{package}_deps.json', 'w') as out:
        json.dump(deps, out)
                

if __name__ == "__main__":
    main()
