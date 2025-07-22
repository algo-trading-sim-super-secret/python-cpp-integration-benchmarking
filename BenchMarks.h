#pragma once
#include <eigen3/Eigen/Dense>
#include <iostream>
#include <chrono>
#include <string.h>

#include <fstream>
#include <sstream>
#include <filesystem>

class BenchMarks
{
public:
    static double matrixComputation(unsigned int n, unsigned int dim);
    static double csvRead(std::string folderPath);
};
