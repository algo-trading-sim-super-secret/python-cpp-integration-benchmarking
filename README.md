
This is a simple comparision between native C++ code, Native Python, Pybind11 with C++, cppyy with C++ library, cppyy implemented natively inside of the python file, and Numba

# Testing Methodology:
Each one of these methods are used called with varying test cases on computing the sum of a products of a matrix of dimensionality DxD by a vector of size D for N number trials.

# Compilation
C++:
`g++ -O3 -std=c++20 cpp_run.cpp BenchMarks.cpp -o cpp_run && ./cpp_run 10 10`

cppyy_library:
`g++ -O3 -Wall -shared -std=c++2b -fpic BenchMarks.cpp -o benchmarks_libpb.so`

cppyy_native:
Inside of `compare.py`, I needed to defined the function in C++ to be converted to Python bindings

Pybind:
`g++ -O3 -Wall -shared -std=c++2b -fpic $(python3 -m pybind11 --includes) BenchMarks_pybind.cpp BenchMarks.cpp -o benchmarks_pybind_libpb$(python3 -m pybind11 --extension-suffix)`

`g++ -O3 -Wall -shared -std=c++2b -fpic BenchMarks.cpp -o benchmarks_libpb.so`

Numba:
Decorate the python `py_inv` function with the njit decorator.
** Note that this will only work in select instances where the method is performing a computation; this will not work in general.

** Also note that cppyy supports Numba with the caveat that the python interpreter is pypy. The sample code of 
```python
import cppyy.numba_ext
@numba.jit(nopython=True)
def cppyy_inv_numba(n,dim):
    return cppyy.gbl.matrixComputation(n, dim)
```
will fail to load unless `__pypy__` is available. 


# Environment:
Ubuntu 22.04 
AMD Ryzen 7 5825U 

G++: `g++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0`
Python:
```
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

Note: you should run this set up on any machine you plan to benchmark on, as this is subjective to the system used and package versioning. 

# Caveats
* Using g++ for compilation of the libraries in C++, however cppyy native can use clang for optimization and thus could be the reason why the performance is different
* Perhaps the choice of tests are not indicative of actual performance for my use case, and there are other methods that better (ie data throughput, I/O reads, data scrapping, etc.)
* The tests are done sequentially and with time.time(), there are better methods and there is likely influence from concurent processes/threads. I try to make even it out by performing `time.sleep(1)` after each test, but that might not be sufficient.

# .gitignore of binaries
Run the following command:
`find . -executable -type f >>.gitignore`
