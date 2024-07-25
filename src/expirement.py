import subprocess
import argparse
from tqdm import tqdm
import os


def make_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    model_type_group = parser.add_mutually_exclusive_group(required=True)
    model_type_group.add_argument("--classical", type=bool, nargs='?', const=True, default=False, help="")
    model_type_group.add_argument("--quantum", type=bool, nargs='?', const=True, default=False, help="")

    parser.add_argument("--name", type=str, required=True, help="")
    parser.add_argument("--runs", type=int, default=100, help="")
    parser.add_argument("--clean", type=bool, nargs='?', const=True, default=False, help="")

    return parser.parse_args()


if __name__ == "__main__":
    args = make_parser()
    BASE_CMD_STR = "reset(RandStream.getGlobalStream,sum(100*clock));" \
                   "set(0, 'DefaultFigureVisible', 'off');hide=true;"
    
    script = ";" # todo

    subprocess.call(['matlab', '-batch', BASE_CMD_STR+script])
