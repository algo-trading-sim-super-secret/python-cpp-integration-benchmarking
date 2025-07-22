import numba 
try:
    import cppyy 

    cppyy.include("eigen3/Eigen/Dense")
    cppyy.cppdef(
        """
    using namespace Eigen;
    double matrixComputation(unsigned int n, unsigned int dim)
    {
        double sum = 0;
        MatrixXd A;
        VectorXd B;
        MatrixXd C;

        A.resize(dim,dim);
        B.resize(dim);
        /*auto start = high_resolution_clock::now();*/
        for (unsigned int i = 0; i < n; ++i) {
            /*A = MatrixXd::Random(dim,dim);*/
            A.setRandom();
            B.setRandom();
            /*B = VectorXd::Random(dim);*/
            C.noalias() = A * B;
            sum += C.norm();
        }

        return sum;
    }
        """
    )
    cppyy_native_matrixComputation = cppyy.gbl.matrixComputation

    cppyy.include("BenchMarks.h")
    cppyy.load_library("benchmarks_libpb")
    cppyy_matrixComputation =cppyy.gbl.BenchMarks.matrixComputation 

except Exception as ex:
    print(ex) 
    robot_cppyy = None

try:
    # from robot_libpb import Robot as Robot_pybind
    import benchMarks_pybind_libpb

    pybind_matrixComputation = benchMarks_pybind_libpb.BenchMarks.matrixComputation
except:
    pybind_matrixComputation = None

from numpy.linalg import solve, norm
from numpy.random import randn

from os import system
import time

def py_inv(n, dim):
    sum = 0
    for _ in range(n):
        A = randn(dim, dim)
        B = randn(dim)
        C = A*B
        sum += norm(C)
    return sum


@numba.jit(nopython=True)
def py_inv_numba(n, dim):
    sum = 0
    for _ in range(n):
        A = randn(dim, dim)
        B = randn(dim)
        C = A*B
        sum += norm(C)
    return sum

## Doesn't work because not using pypy interpreter
# import cppyy.numba_ext
# @numba.jit(nopython=True)
# def cppyy_inv_numba(n,dim):
#     return cppyy.gbl.matrixComputation(n, dim)


def cpp_inv(n, dim):
    system('./cpp_run {} {}'.format(n, dim))

candidates = [(cpp_inv, 'C++'), (py_inv, 'Python'), (py_inv_numba, 'Numba')]

if cppyy_matrixComputation is not None:
    candidates.append((cppyy_matrixComputation, 'cppyy_library'))
    candidates.append( (cppyy_native_matrixComputation, 'cppyy_native'))
    # candidates.append((cppyy_inv_numba, 'cppyy+numba'))

if pybind_matrixComputation is not None:
    candidates.append((pybind_matrixComputation, 'pybind'))


# find the longest length name for formatting output 
test_name_length = 0
for (_,test_name) in candidates:
    test_name_length = max(test_name_length,len(test_name))


def elapsed_time(n, dim):
    for fct, method in candidates:
        time.sleep(1)
        t0 = time.time()
        fct(n, dim)
        print(f'{method:<{test_name_length}}\t-> {1000*(time.time() - t0):.2f} ms' )

# =================================================================================
# CONDUCT TESTS
if __name__ == "__main__":
    print("Results:")
    # tests = {0:[0,0]}
    tests = {0:[0,0], 1:[50,50], 2:[100,100], 3:[250,250], 4:[500,500]}
    for (n, dim) in tests.values():
        print(f"============Test n={n} dim={dim}=============")
        elapsed_time(n, dim)
