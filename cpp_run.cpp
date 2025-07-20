#include "BenchMarks.h"

#include <cstdlib>  // for std::atoi

int main(int argc, char* argv[])
{
    // Default parameters
    unsigned int n = std::atoi(argv[1]);// = 1000;
    unsigned int dim = std::atoi(argv[2]); // = 100;

    /*if (argc >= 2) n = std::atoi(argv[1]);*/
    /*if (argc >= 3) dim = std::atoi(argv[2]);*/

    /*std::cout << "Running matrix benchmark with n = " << n << ", dim = " << dim << std::endl;*/
    BenchMarks::matrixComputation(n, dim);
    /*std::cout << BenchMarks::matrixComputation(n, dim) << std::endl;*/

    return 0;
}
