import numba 
try:
    import cppyy 
    # cppyy.include("eigen3/Eigen/Dense")
    # cppyy.include("iostream")
    # cppyy.include("chrono")
    # cppyy.include("string.h")
    # cppyy.include("fstream")
    # cppyy.include("sstream")
    # cppyy.include("filesystem")
    # cppyy.include("BenchMarks.h")
    #
    #
    # cppyy.cppdef(
    #     """
    # double BenchMarks::csvRead(std::string folderPath)
    # {
    #     std::vector<std::string> fileNames;
    #     try {
    #         for (const auto& entry : std::filesystem::directory_iterator(folderPath))
    #             fileNames.push_back(entry.path().filename().string());
    #     } 
    #     catch (const std::filesystem::filesystem_error& e) {
    #         std::cerr << \\\"Filesystem error: \\\" << e.what() << \\\"\\\\n\\\";
    #     }
    #
    #     for (auto& fileName : fileNames){
    #         std::ifstream file(folderPath+fileName);
    #         if (!file.is_open()) {
    #             std::cerr << \"Failed to open file: \" << folderPath+fileName << \"\\n\";
    #             return 1;
    #         }
    #
    #         std::string line;
    #         std::vector<std::vector<std::string>> data;
    #
    #         while (std::getline(file, line)) {
    #             std::stringstream ss(line);
    #             std::string cell;
    #             std::vector<std::string> row;
    #
    #             while (std::getline(ss, cell, ',')) {
    #                 row.push_back(cell);
    #             }
    #
    #             data.push_back(row);
    #         }
    #
    #         file.close();
    #     }
    #     return 0;
    # }
    #     """
    # )
    #
    # cppyy_native_matrixComputation = cppyy.gbl.BenchMarks.matrixComputation

    cppyy.include("BenchMarks.h")
    cppyy.load_library("benchmarks_libpb")
    cppyy_csvRead =cppyy.gbl.BenchMarks.csvRead

except Exception as ex:
    print(ex) 
    cppyy_csvRead = None

try:
    # from robot_libpb import Robot as Robot_pybind
    import benchmarks_pybind_libpb

    pybind_csvRead = benchmarks_pybind_libpb.BenchMarks.csvRead
except Exception as ex:
    print(ex)
    pybind_csvRead = None

from os import system
import os
import time

import csv
import pandas
def py_csvRead(folderPath):
    filePaths = [os.path.join(folderPath,fileName) for fileName in os.listdir(folderPath)]
    
    data = [] 
    data = [pandas.read_csv(filePath) for filePath in filePaths]

@numba.jit(nopython=False)
def py_csvRead_numba(folderPath):
    filePaths = [os.path.join(folderPath,fileName) for fileName in os.listdir(folderPath)]

    data = [] 
    data = [pandas.read_csv(filePath) for filePath in filePaths]


def cpp_csvRead(n=10, dim=10):
    system('./cpp_run {} {}'.format(n, dim))

candidates = [(cpp_csvRead, 'C++'), (py_csvRead, 'Python')]

if cppyy_csvRead is not None:
    candidates.append((cppyy_csvRead, 'cppyy_library'))

    # candidates.append( (cppyy_csvRead, 'cppyy_native'))
    # candidates.append((cppyy_inv_numba, 'cppyy+numba'))

# if py_csvRead_numba is not None:
#     candidates.append( (py_csvRead_numba, 'Numba'))
if pybind_csvRead is not None:
    candidates.append((pybind_csvRead, 'pybind'))


# find the longest length name for formatting output 
test_name_length = 0
for (_,test_name) in candidates:
    test_name_length = max(test_name_length,len(test_name))


def elapsed_time(folderPath):
    for fct, method in candidates:
        time.sleep(1)
        t0 = time.time()
        fct(folderPath)
        print(f'{method:<{test_name_length}}\t-> {1000*(time.time() - t0):.2f} ms' )

# =================================================================================
# CONDUCT TESTS
if __name__ == "__main__":
    print("Results:")
    tests = {0:'satellite_data/'}
    for (n,folderPath) in tests.items():
        print(f"============Test n={n} folderPath={folderPath}=============")
        elapsed_time(folderPath)
