function [X,Y] = generateData(numSamples)
X = zeros(numSamples,2);
labels = strings(numSamples,1);
for i = 1:numSamples
    x1 = rand;
    x2 = rand;
    X(i,:) = [x1 x2];
    if (x1 > x2)
        labels(i) = "Blue";
    else
        labels(i) = "Yellow";
    end
end
Y = categorical(labels);

figure()
gscatter(X(:,1), X(:,2), Y,"by")
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

numSamples = 200;
[X,Y] = generateData(numSamples);
classNames = ["Blue", "Yellow"];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

inputSize = size(X,2);
numClasses = numel(classNames);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

layers = [featureInputLayer(inputSize,Normalization="none")
    fullyConnectedLayer(numClasses)
    softmaxLayer
    classificationLayer];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if exist('hide', 'var')
    options = trainingOptions("sgdm", ...
        MiniBatchSize=20, ...
        InitialLearnRate=0.1, ...
        Momentum=0.9, ...
        ExecutionEnvironment="cpu", ...
        Verbose=false);
else
    options = trainingOptions("sgdm", ...
        MiniBatchSize=20, ...
        InitialLearnRate=0.1, ...
        Momentum=0.9, ...
        ExecutionEnvironment="cpu", ...
        Plots="training-progress", ...
        Verbose=false);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

net = trainNetwork(X,Y,layers,options);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[XTest,trueLabels] = generateData(numSamples);
predictedLabels = classify(net,XTest);

gscatter(XTest(:,1),XTest(:,2),predictedLabels,"by")
figure()
confusionchart(trueLabels,predictedLabels)

format long
accuracy = sum(predictedLabels==trueLabels,'all')/numel(predictedLabels);
writematrix(accuracy, "linear.csv", "WriteMode", "append")
