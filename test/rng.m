samples = 5000; % number of samples to generate, must match value in rng_gof.py
nums = rand(samples,1);
writematrix(nums, "rng.csv");