#pragma once
#include <eigen3/Eigen/Dense>
#include <iostream>
#include <chrono>

class BenchMarks
{
public:
    static double matrixComputation(unsigned int n, unsigned int dim);
};
