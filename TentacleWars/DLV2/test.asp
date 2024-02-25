% Define facts
%int1(5).
%int2(10).

% Define a rule
sum(Result) :- int1(X), int2(Y), Result = X + Y.
