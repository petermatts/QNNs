from scipy.stats import norm
from math import sqrt

class Estimator:
    """ Computes point estimates and confidence intervals """
    def __init__(self, conf_pct, epsilon, relative):
        self.epsilon = epsilon # precison of CI
        self.relative = relative # relative or absolute precision
        self.k = 0  # number of values processed so far
        self.sum = 0.0  # running sum of values
        self.v = 0.0  # running value of (k-1)*variance
        self.z = norm.ppf(0.5 + (conf_pct / 200))  # CI normal quantile
        self.conf_str = str(conf_pct) + "%"  # string of form "xx%" for xx% CI
        # self.values = list() # use for debugging

    def reset(self) -> None:
        self.k = 0
        self.sum = 0
        self.v = 0
        # self.values = list() # use for debugging

    def add_val(self, value) -> None:
        self.k += 1
        if self.k > 1:
            diff = self.sum - (self.k - 1) * value
            self.v += diff/self.k * diff/(self.k-1)
        self.sum += value
        # self.values.append(value) # use for debugging

    def get_var(self) -> float:
        return self.v/(self.k-1) if self.k > 1 else 0

    def get_mean(self) -> float:
        return self.sum/self.k if self.k > 1 else 0

    def get_ci(self) -> str:
        hw = self.z * sqrt(self.get_var()/self.k)
        point_est = self.get_mean()
        c_low = point_est - hw
        c_high = point_est + hw
        return "{0} Confidence Interval: [ {1:.4f}, {2:.4f} ]  (hw = {3:.4f})".format(self.conf_str, c_low, c_high, hw)

    def get_num_trials(self) -> str:
        var = self.get_var()
        if var == 0:
            return "UNAVAILABLE (Need at least 2 pilot reps)"
        if self.relative:
            width = self.get_mean() * self.epsilon
            retstr = "Est. # of reps for +/- {0:.2f}% accuracy: {1}"
            acc = 100 * self.epsilon
        else:
            width = self.epsilon
            retstr = "Est. # of reps for +/- {0:.4f} accuracy: {1}"
            acc = self.epsilon
        nreps = int(1+(var * self.z * self.z)/(width * width))

        return retstr.format(acc, nreps)