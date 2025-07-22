#include "BenchMarks.h"

using namespace Eigen;
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
        C.noalias() = A * B;
        sum += C.norm();
    }

    return sum;
}

double BenchMarks::csvRead(std::string folderPath)
{
    // Load all file names
    std::vector<std::string> fileNames;
    try {
        for (const auto& entry : std::filesystem::directory_iterator(folderPath))
            fileNames.push_back(entry.path().filename().string());
    } 
    catch (const std::filesystem::filesystem_error& e) {
        std::cerr << "Filesystem error: " << e.what() << '\n';
    }

    for (auto& fileName : fileNames){
        std::ifstream file(folderPath+fileName);
        if (!file.is_open()) {
            std::cerr << "Failed to open file: " << folderPath+fileName << "\n";
            return 1;
        }

        std::string line;
        std::vector<std::vector<std::string>> data;

        while (std::getline(file, line)) {
            std::stringstream ss(line);
            std::string cell;
            std::vector<std::string> row;

            while (std::getline(ss, cell, ',')) {
                row.push_back(cell);
            }

            data.push_back(row);
        }

        /*// Print parsed data*/
        /*for (const auto& row : data) {*/
        /*    for (const auto& cell : row) {*/
        /*        std::cout << cell << " ";*/
        /*    }*/
        /*    std::cout << "\n";*/
        /*}*/

        file.close();
    }
    return 0;
}
