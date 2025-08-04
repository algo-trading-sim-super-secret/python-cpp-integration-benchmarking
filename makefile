# Compiler settings
cxx= g++
cxx_flags = -Wall -g --std=c++2b
cxx_flags_optimized = $(cxx_flags) -O3
cxx_flags_optimized_library =  $(cxx_flags_optimized) --shared -fpic

# For pybind 
python_includes := $(shell python3 -m pybind11 --includes)
python_extension := $(shell python3 -m pybind11 --extension-suffix)


get_libraries: clean cpp_matrix_computation_optimized cpp_csv_read_optimized cpp_library pybind 

cpp_matrix_computation_optimized: cpp_matrix_computation.cpp BenchMarks.cpp  
	$(cxx) $(cxx_flags_optimized) cpp_matrix_computation.cpp BenchMarks.cpp -o cpp_matrix_computation

cpp_csv_read_optimized: cpp_csv_read.cpp BenchMarks.cpp  
	$(cxx) $(cxx_flags_optimized) cpp_csv_read.cpp BenchMarks.cpp -o cpp_csv_read

cpp_library: BenchMarks.cpp  
	$(cxx) $(cxx_flags_optimized_library) BenchMarks.cpp -o benchmarks_libpb.so

pybind: BenchMarks_pybind.cpp
	$(cxx) $(cxx_flags_optimized_library) $(python_includes) BenchMarks_pybind.cpp BenchMarks.cpp -o benchmarks_pybind_libpb$(python_extension)


clean:
	rm -f benchmarks_pybind_libpb$(python_extension) cpp_run benchmarks_libpb.so cpp_matrix_computation cpp_csv_read 


# C++:
# `g++ -O3 -std=c++2b cpp_run.cpp BenchMarks.cpp -o cpp_run && ./cpp_run 10 10`

# cppyy_library:
# `g++ -O3 -Wall -shared -std=c++2b -fpic BenchMarks.cpp -o benchmarks_libpb.so`

# cppyy_native:
# Inside of `compare.py`, I needed to defined the function in C++ to be converted to Python bindings

# Pybind:
# `g++ -O3 -Wall -shared -std=c++2b -fpic $(python3 -m pybind11 --includes) BenchMarks_pybind.cpp BenchMarks.cpp -o benchmarks_pybind_libpb$(python3 -m pybind11 --extension-suffix)`

