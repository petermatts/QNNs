import subprocess
import argparse
import os
import sys
from pathlib import Path
from pandas import read_csv

sys.path.append(str((Path.cwd() / ".." / "references").resolve()))
from Estimator import Estimator


def make_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    model_type_group = parser.add_mutually_exclusive_group()
    model_type_group.add_argument("--classical", type=bool, nargs='?', const=True, default=False, help="")
    model_type_group.add_argument("--quantum", type=bool, nargs='?', const=True, default=False, help="")

    main = parser.add_mutually_exclusive_group(required=True)
    main.add_argument("--name", type=str, help="")
    main.add_argument("--clean-all", type=bool, nargs='?', const=True, default=False, help="")
    
    parser.add_argument("--runs", type=int, default=100, help="")
    parser.add_argument("--clean", type=bool, nargs='?', const=True, default=False, help="")

    # estimator args
    parser.add_argument("--conf-pct", type=float, default=95, help="")
    parser.add_argument("--epsilon", type=float, default=0.01, help="")
    parser.add_argument("--relative", type=bool, default=True, help="")

    return parser.parse_args()


def build_matlab_str(args: argparse.Namespace) -> str:
    model = None
    if args.classical:
        if args.name == "linear":
            model = 1
        elif args.name == "nonlin":
            model = 2
        else:
            raise ValueError("Invalid model name or type")
    elif args.quantum:
        if args.name == "linear":
            model = 3
        elif args.name == "nonlin":
            model = 4
        else:
            raise ValueError("Invalid model name or type")
    else:
        raise ValueError("Unspecified model type")
    
    assert model is not None

    return f"hide=true;numruns={args.runs};model={model};driver;"


def check_clean(args) -> None:
    if args.clean:
        if args.classical:
            if args.name == "linear":
                if os.path.exists('classical/linear.csv'): os.remove('classical/linear.csv')
            elif args.name == "nonlin":
                if os.path.exists('classical/nonlin.csv'): os.remove('classical/nonlin.csv')
            else:
                raise ValueError("Invalid model name or type")
        elif args.quantum:
            if args.name == "linear":
                if os.path.exists('quantum/linear.csv'): os.remove('quantum/linear.csv')
            elif args.name == "nonlin":
                if os.path.exists('quantum/nonlin.csv'): os.remove('quantum/nonlin.csv')
            else:
                raise ValueError("Invalid model name or type")
        else:
            raise ValueError("Unspecified model type")
    elif args.clean_all:
        if os.path.exists('classical/linear.csv'): os.remove('classical/linear.csv')
        if os.path.exists('classical/nonlin.csv'): os.remove('classical/nonlin.csv')
        if os.path.exists('quantum/linear.csv'): os.remove('quantum/linear.csv')
        if os.path.exists('quantum/nonlin.csv'): os.remove('quantum/nonlin.csv')


def analyze(args):
    est = Estimator(args.conf_pct, args.epsilon, args.relative)

    data = None
    if args.classical:
        if args.name == "linear":
            data = read_csv("classical/linear.csv", header=None).to_numpy()
        elif args.name == "nonlin":
            data = read_csv("classical/nonlin.csv", header=None).to_numpy()
        else:
            raise ValueError("Invalid model name or type")
    elif args.quantum:
        if args.name == "linear":
            data = read_csv("quantum/linear.csv", header=None).to_numpy()
        elif args.name == "nonlin":
            data = read_csv("quantum/nonlin.csv", header=None).to_numpy()
        else:
            raise ValueError("Invalid model name or type")
    else:
        raise ValueError("Unspecified model type")
    
    assert data is not None

    for i in range(args.runs):
        est.add_val(data[i,0])

    print("Average accuracy is %f"%est.get_mean())
    print(est.get_ci(), end='\n\n')


if __name__ == "__main__":
    args = make_parser()

    if args.clean or args.clean_all:
        check_clean(args)
    else:
        cmd_str = build_matlab_str(args)
        subprocess.call(['matlab', '-batch', cmd_str])
        analyze(args)
