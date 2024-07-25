# QNNs

This repo houses an expirement idea I had to learn both linear and nonlinear data using Quantum Neural Networks (QNNs).

The idea came from [this](https://www.mathworks.com/help/matlab/math/solve-xor-problem-using-quantum-neural-network.html) reference when I noticed that the QNN implemented was able to learn nonlinear data (XOR data) without the need for a nonlinearity like Relu or tanh, etc... This got me wondering, could a QNN be trained to learn linear data as well ustilizing the same model structure?

## Code

- Reference code for estimating statistics with confidence intervals for model performances
- Evaluation of the MATLAB random number generator using the Runs-Up method.
- MATLAB NN and QNN models over (simplistic) linear and nonlinear datasets
- Driver code for running models mulitple times and gathering statistics on performance.

- Room for future improvement (see below)

## Notes

### Observations

TBD

### Future Work and Improvements to Expirement

See **Next Steps/Ideas** below.

## Next Steps/Ideas

### Code

The parameterized quantum circuit (PQC) defined in the MATLAB expirement is hard coded. This includes the function for computing the gradient values for the backpropagation algorithm. This means that when changing the circuit to tune/design a model, this function will need to be rewritten to match the new PQC. This does not scale with larger models, or even models that require a different/specialized quantum circuit.

Thus a framework is needed to compute the gradients analytically/algorithmically/automatically. At first I looked into [TensorFlow](https://www.tensorflow.org/quantum/tutorials/gradients), but even their API requires a hardcoded/custom defined function for each ciruit design.

Then I found [PennyLane.ai](https://pennylane.ai/). Their API looks fairly easy to use AND intergrates with TensorFlow and the PyTorch APIs neatly, by wrapping a PQC into a Layer defined within those APIs. Allowing the existing Autograd engines to work. **Moving forward this will be how progress in this project proceeds based on the initial matlab expirements.**

Furthermore, PennyLane also allows for the potential (through plug-ins) to run on real Quantum Devices. See their site for more details.

### Research Papers

- [An Introduction To Quantum Machine Learning for Engineers](https://arxiv.org/pdf/2205.09510)
- [Provable Advantage of Parameterized Quantum Circuit in Function Approximation](https://arxiv.org/pdf/2310.07528)
- [Characterizing randomness in parameterized quantum circuits through expressibility and average entanglement](https://arxiv.org/pdf/2405.02265)

### Useful Links

- [Synergistic pretraining of parametrized quantum circuits via tensor networks](https://www.nature.com/articles/s41467-023-43908-6)
- [Medium: Quantum Neural Networks](https://medium.com/mit-6-s089-intro-to-quantum-computing/quantum-neural-networks-7b5bc469d984)
- [TensorFlow Quantum: Calculate Gradients](https://www.tensorflow.org/quantum/tutorials/gradients)
