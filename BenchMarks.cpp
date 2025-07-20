#include "BenchMarks.h"
using namespace Eigen;
using namespace std::chrono;

double BenchMarks::matrixComputation(unsigned int n, unsigned int dim)
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
    /*auto end = high_resolution_clock::now();*/
    /*auto duration = duration_cast<milliseconds>(end - start).count();*/
    /*std::cout << "Total time: " << duration << " ms\n";*/
    /*std::cout << "Average per run: " << static_cast<double>(duration) / n << " ms\n";*/
    /*std::cout << "Final norm sum: " << sum << "\n";*/
    /*return sum;*/
}

