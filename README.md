
This is a simple comparision between native C++ code, Native Python, Pybind11 with C++, CPPYY with C++, and Numba

# Testing Methodology:
Each one of these methods are used called with varying test cases on computing the sum of a products of a matrix of dimensionality DxD by a vector of size D for N number trials.

C++:
`g++ -O3 -std=c++20 cpp_run.cpp BenchMarks.cpp -o cpp_run && ./cpp_run 10 10`

Pybind:
`g++ -O3 -Wall -shared -std=c++2b -fpic $(python3 -m pybind11 --includes) BenchMarks_pybind.cpp BenchMarks.cpp -o benchmarks_pybind_libpb$(python3 -m pybind11 --extension-suffix)`

CPPYY:
Inside of `compare.py`, I needed to defined the function in C++ to be converted to Python bindings

Numba:
Decorate the python `py_inv` function with the njit decorator.
** Note that this will only work in select instances where the method is performing a computation; this will not work in general.

# Environment:
G++: `g++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0`
Python:
```python
clang==20.1.5
cppyy==3.5.0
cppyy-backend==1.15.3
cppyy-cling==6.32.8
cpycppyy==1.13.0
invoke==2.2.0
llvmlite==0.44.0
numba==0.61.2
numpy==2.2.6
pybind11==3.0.0
scipy==1.16.0
```

# .gitignore of binaries
Run the following command:
`find . -executable -type f >>.gitignore`
