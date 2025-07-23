import numba 
from object_benchMarks import Candidate, BenchMarks, temp_func

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

from os import system
import os
import time

import csv
import pandas
def py_csvRead(folderPath):
    filePaths = [os.path.join(folderPath,fileName) for fileName in os.listdir(folderPath)]
    data = [] 
    data = [pandas.read_csv(filePath) for filePath in filePaths]

# @numba.jit(nopython=False)
# def py_csvRead_numba(folderPath):
#     filePaths = [os.path.join(folderPath,fileName) for fileName in os.listdir(folderPath)]
#
#     data = [] 
#     data = [pandas.read_csv(filePath) for filePath in filePaths]
#
def cpp_csvRead(folderPath):
    system('./cpp_run {} {}'.format(10, 10))


candidates = [(cpp_csvRead, 'C++'), (py_csvRead, 'Python')]
# candidates = [(py_csvRead, 'Python')]

# if cppyy_csvRead is not None:
    # candidates.append((cppyy_csvRead, 'cppyy_library'))

    # candidates.append( (cppyy_csvRead, 'cppyy_native'))
    # candidates.append((cppyy_inv_numba, 'cppyy+numba'))

# if py_csvRead_numba is not None:
#     candidates.append( (py_csvRead_numba, 'Numba'))
# if pybind_csvRead is not None:
    # candidates.append((pybind_csvRead, 'pybind'))

def format_candidate_list(values):
    return set([Candidate(value[1],value[0]) for value in values])

def format_test_cases(names,values):
    return {jdx:{names[idx]:values[idx] for idx in range(len(names))} for jdx in range(len(values))}


candidates = format_candidate_list(candidates)
test_cases = format_test_cases(['folderPath'],['satellite_data/'])
print(test_cases)
# print(test_cases[0])
print(candidates)
print(py_csvRead(**test_cases[0]))
# assert False
# assert False
# =================================================================================
# CONDUCT TESTS
benchMarks = BenchMarks("csv Read",test_cases=test_cases,candidates=candidates,save_candidate_data=False) 
print(benchMarks.results)
benchMarks.perform_all_tests()
benchMarks.format_test_results()


# candidates = set([Candidate(f"{idx}",temp_func) for idx in range(3)])
# test_cases = {0:{'n':5,'value':"20"},1:{'n':200,'value':"1"}}
#
# print("PROPER FORMATTING\n\n")
# print(candidates)
# print(test_cases)
# benchMarks = BenchMarks("code_val", test_cases, candidates)
# benchMarks.perform_test(1,"2")
# benchMarks.format_test_results()
#
# benchMarks.perform_all_tests()
# benchMarks.format_test_results()
