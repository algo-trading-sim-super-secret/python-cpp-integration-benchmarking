import numba 
from object_benchMarks import Candidate, BenchMarks, Test,temp_func


from os import system
import os
import time

import csv
import pandas

import warnings
warnings.filterwarnings('ignore')  

try:
    import cppyy 
    cppyy.include("BenchMarks.h")
    cppyy.load_library("benchmarks_libpb")
    cppyy_csvRead =cppyy.gbl.BenchMarks.csvRead

except Exception as ex:
    print(ex) 
    cppyy_csvRead = None

try:
    import benchmarks_pybind_libpb

    pybind_csvRead = benchmarks_pybind_libpb.BenchMarks.csvRead
except Exception as ex:
    print(ex)
    pybind_csvRead = None


def py_csvRead(folderPath):
    print("folderpath",folderPath)
    filePaths = [os.path.join(folderPath,fileName) for fileName in os.listdir(folderPath)]
    data = [] 
    data = [pandas.read_csv(filePath) for filePath in filePaths]

# @numba.jit(nopython=False)
# def py_csvRead_numba(folderPath):
#     filePaths = [os.path.join(folderPath,fileName) for fileName in os.listdir(folderPath)]
#
#     data = [] 
#     data = [pandas.read_csv(filePath) for filePath in filePaths]

def cpp_csvRead(folderPath):
    system('./cpp_csv_read')

candidates = [(cpp_csvRead, 'C++'), (py_csvRead, 'Python')]

if cppyy_csvRead is not None:
    candidates.append((cppyy_csvRead, 'cppyy_library'))

    # candidates.append( (cppyy_csvRead, 'cppyy_native'))
    # candidates.append((cppyy_inv_numba, 'cppyy+numba'))

# if py_csvRead_numba is not None:
#     candidates.append( (py_csvRead_numba, 'Numba'))
if pybind_csvRead is not None:
    candidates.append((pybind_csvRead, 'pybind'))


def format_candidate_list(values):
    return set([Candidate(value[1],value[0]) for value in values])

test_cases = Test(['folderPath'],{0:['satellite_data/']})
candidates = format_candidate_list(candidates)
# print(test_cases)
# print(candidates)
# =================================================================================
# CONDUCT TESTS
benchMarks = BenchMarks("csv Read",test=test_cases,candidates=candidates,save_candidate_data=False) 
print(benchMarks.results)
benchMarks.perform_all_tests()
benchMarks.format_test_results()
