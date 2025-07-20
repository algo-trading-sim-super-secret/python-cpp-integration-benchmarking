class DefaultObject:
    def __init__(self):
        pass 
    def matrixComputation(n,dim):
        pass
try:
    # from robot_lib import Robot as Robot_cppyy
    # robot_cppyy = Robot_cppyy()
    # import cppyy 
    # cppyy.load_library("./librobot.so")
    # cppyy.include("robot.h")
    # robot_cppyy = cppyy.gbl.Robot()
    # pass 
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
    robot_cppyy = DefaultObject()
    robot_cppyy.matrixComputation = cppyy.gbl.matrixComputation
except Exception as ex:
    print(ex) 
    assert False
    robot_cppyy = None

try:
    # from robot_libpb import Robot as Robot_pybind
    import benchMarks_pybind_libpb
    robot_pybind = DefaultObject() 

    robot_pybind.matrixComputation = benchMarks_pybind_libpb.BenchMarks.matrixComputation
except:
    robot_pybind = None


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


from numba import njit
@njit
def py_inv_numba(n, dim):
    sum = 0
    for _ in range(n):
        A = randn(dim, dim)
        B = randn(dim)
        C = A*B
        sum += norm(C)
    return sum


def cpp_inv(n, dim):
    system('./cpp_run {} {}'.format(n, dim))

candidates = [(cpp_inv, 'C++'), (py_inv, 'Python'), (py_inv_numba, 'Numba')]
# candidates =  [(cpp_inv, 'C++'), (py_inv, 'Python')]
if robot_cppyy is not None:
    candidates.append((robot_cppyy.matrixComputation, 'cppyy'))
if robot_pybind is not None:
    candidates.append((robot_pybind.matrixComputation, 'pybind'))

def elapsed_time(n, dim):
    for fct, method in candidates:
        t0 = time.time()
        fct(n, dim)
        print('   {}\t-> {:.2f} ms'.format(method, 1000*(time.time() - t0)))


# TESTS
print("Results:")

tests = {0:[0,0], 1:[50,50], 2:[100,100], 3:[250,250], 4:[500,500]}
for (n, dim) in tests.values():
    print(f"============Test n={n} dim={dim}=============")
    elapsed_time(n, dim)
