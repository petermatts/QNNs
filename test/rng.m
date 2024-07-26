% make sure that the samples variable exists
if not(exist('samples', 'var'))
    quit(1)
end

if not(exist('runs', 'var'))
    quit(2)
end

nums = rand(1, samples);
writematrix(nums, "rng.csv");

for r = 1:runs
    % not really necessary but still good to do
    reset(RandStream.getGlobalStream,sum(100*clock)) %#ok<*CLOCK>
    nums = rand(1, samples+1);
    writematrix(nums, "rng.csv", 'WriteMode', 'append');
end
