import torch
from scipy.stats import chi2
import subprocess
from tqdm import tqdm
from pandas import read_csv
import sys
from pathlib import Path

sys.path.append(str((Path.cwd() / ".." / "references").resolve()))
from Estimator import Estimator

A = torch.tensor([
    [4529.4, 9044.9, 13568, 18091, 22615, 27892],
    [9044.9, 18097, 27139, 36187, 45234, 55789],
    [13568, 27139, 40721, 54281, 67852, 83685],
    [18091, 36187, 54281, 72414, 90470, 111580],
    [22615, 45234, 67852, 90470, 113262, 139476],
    [27892, 55789, 83685, 111580, 139476, 172860]
])

B = torch.tensor([1/6,5/24,11/120,19/720,29/5040,1/840])

"""
Translated code from Problem 7.8 in Law.

Note the J variable was adapted to be 0-indexed
"""
def runs_up(samples: torch.tensor) -> tuple[int,int,int,int,int,int]:
    runs = [0,0,0,0,0,0]

    J = 0
    A = samples[0]

    for i in range(1,samples.size()[0]):
        B = samples[i]
        if A >= B:
            J = min(J,5)
            runs[J] += 1
            J = 0
        else:
            J += 1
        A = B

    J = min(J,5)
    runs[J] += 1
        
    return tuple(runs)

def R(runs: tuple[int,int,int,int,int,int], n)->float:
    rs = torch.tensor(runs)
    mult = rs - n*B
    return (1/n)*torch.sum(A * torch.outer(mult,mult))

if __name__ == '__main__':
    runs = 5
    n = 5000 # number of samples
    conf = 0.95
    epsilon = 0.01
    relative = True
    score = float(chi2.isf(1-conf, 6))
    trial = True

    if runs == 1:
        print("Null Hypothesis: Number Generator is a valid uniform generator.\n")
        samples = torch.rand(n)
        rus = runs_up(samples)
        print("Runs:", rus)
        r_score = float(R(rus, n))
        print("R =", r_score)
        
        print("X^2 score =", score, "for df=6 and", conf, "confidence.\n")
        if r_score <= score:
            print("Accept Hypothesis: Number Generator is a valid uniform generator")
        else:
            print("Reject Hypothesis: Number Generator is not a valid uniform generator")

        # test case in book
        # n = 10
        # samples = torch.tensor((0.86,0.11,0.23,0.03,0.13,0.06,0.55,0.64,0.87,0.10))
        # print(runs_up(samples)) # (2,2,0,1,0,0)
        # print(R(runs_up(samples), n))
    else:
        est = Estimator(100*conf, epsilon=epsilon, relative=relative)
        est.reset()

        for run in tqdm(range(runs)):
            subprocess.call(['matlab', '-batch', '"reset(RandStream.getGlobalStream,sum(100*clock));rng"'])
            data = torch.tensor(read_csv("rng.csv").to_numpy())
            assert n == data.shape[0]
            rus = runs_up(data)
            r_score = float(R(rus, n))
            est.add_val(r_score)

        r_score = est.get_mean()
        print("Average Runs-Up score is %f"%r_score)
        print(est.get_ci(), end='\n\n')
        print("Null Hypothesis: Number Generator is a valid uniform generator.")
        print("X^2 score =", score, "for df=6 and", conf, "confidence.\n")
        if r_score <= score:
            print("Accept Hypothesis: Number Generator is a valid uniform generator!\n")
        else:
            print("Reject Hypothesis: Number Generator is not a valid uniform generator!\n")

        if trial:
            print(est.get_num_trials())
