% check for important variables
if not(exist('model', 'var'))
    quit(1)
end

if not(exist('numruns', 'var'))
    quit(2)
end

%disable graphs
set(0, 'DefaultFigureVisible', 'off')

% initialize progress display
txt = sprintf("Progress %7.3f", 0);
fprintf(txt+"%%")

for i = 1:numruns
    % reset rng seed
    reset(RandStream.getGlobalStream, sum(100*clock)) %#ok<*CLOCK>
    
    % todo support other model types (dynamically)
    if model == 1
        cd classical
        linear;
        cd ..
    elseif model == 2
        cd classical
        nonlin;
        cd ..
    elseif model == 3
        cd quantum
        linear;
        cd ..
    elseif model == 4
        cd quantum
        nonlin;
        cd ..
    else
        quit(3)
    end
    
    fprintf(repmat('\b', 1, 20))
    txt = sprintf("Progress %7.3f", 100*(i/numruns));
    fprintf(txt+"%%")
    
    % important or else next run will used previously trained model
    clearvars -except model i numruns hide
end

fprintf("\n")
