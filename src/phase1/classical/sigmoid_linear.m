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
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

numSamples = 200;
[X,Y] = generateData(numSamples);
classNames = ["Blue", "Yellow"];

figure()
gscatter(X(:,1), X(:,2), Y,"by")
title("Train (Sigmoid Linear Classical)")
if not(exist('hide', 'var'))
    saveas(gcf, "../../../images/classical_sigmoid_linear_data.png");
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

inputSize = size(X,2);
numClasses = numel(classNames);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

layers = [featureInputLayer(inputSize,Normalization="none")
    % fullyConnectedLayer(5) % performance is best with another layer here
    sigmoidLayer()
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

if not(exist('hide','var'))
    currentfig = findall(groot, 'Tag', 'NNET_CNN_TRAININGPLOT_UIFIGURE');
    F = getframe(currentfig(1,1));
    imwrite(F.cdata, '../../../images/classical_sigmoid_linear_prog.png');
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[XTest,trueLabels] = generateData(numSamples);
predictedLabels = classify(net,XTest);

figure()
gscatter(XTest(:,1),XTest(:,2),predictedLabels,"by")
title("Test (Sigmoid Linear Classical)")
if not(exist('hide', 'var'))
    saveas(gcf, "../../../images/classical_sigmoid_linear_test.png")
end

figure()
confusionchart(trueLabels,predictedLabels)
title("Confusion Matrix (Sigmoid Linear Classical)")
if not(exist('hide', 'var'))
    saveas(gcf, "../../../images/classical_sigmoid_linear_conf.png")
end

format long
accuracy = sum(predictedLabels==trueLabels,'all')/numel(predictedLabels);
writematrix(accuracy, "sigmoid_linear.csv", "WriteMode", "append")
