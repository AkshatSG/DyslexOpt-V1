# DyslexOpt-V1

![Flowchart Diagram](https://github.com/AkshatSG/DyslexOpt-V1/blob/main/flowchart.png)

DyslexOpt is A Human-in-the-Loop Bayesian Optimization System for Enhancing Reading Fluency for Dyslexic Users

DyslexOpt-V1 uses basic text settings as the parameters to tune. In the future, the goal is to optimize the parameters of the bezier curves of the texts in an attempt to create much more detailed and personalized fonts.

Hence, google text formats were used to tune the text. 

The given code is very ambiguous. THe choice of which parameters to tune are up to the dyslexic reader/tester, and ought to be available where the test occurs (a simple google slide to a more robust lab application). 

reading_test.py already contains 30 sample reading texts generated using Mistral 7B. It is also where the reader will be tested for fluency, and comfort score will be inputted.

BO.py is the python file for the bayesian optimization based text config tuning framework. You are required to input the objective function value f(x) (described in the paper) during each of the iterations based on the state the tuner returns to you. This value is based on the result from reading_test.py (using reader fluency and feedback in a prudent manner).
