# Compiler settings
cxx= g++
cxx_flags = -Wall -g --std=c++2b
cxx_flags_optimized = $(cxx_flags) -O3
cxx_flags_optimized_library =  $(cxx_flags_optimized) --shared -fpic

# For pybind 
python_includes := $(shell python3 -m pybind11 --includes)
python_extension := $(shell python3 -m pybind11 --extension-suffix)


get_libraries: clean cpp_run_optimized cpp_library pybind 

cpp_run: cpp_run.cpp BenchMarks.cpp  
	$(cxx) $(cxx_flags) cpp_run.cpp BenchMarks.cpp -o cpp_run

cpp_run_optimized: cpp_run.cpp BenchMarks.cpp  
	$(cxx) $(cxx_flags_optimized_library) cpp_run.cpp BenchMarks.cpp -o cpp_run

cpp_library: BenchMarks.cpp  
	$(cxx) $(cxx_flags_optimized_library) BenchMarks.cpp -o benchmarks_libpb.so

pybind: BenchMarks_pybind.cpp
	$(cxx) $(cxx_flags_optimized_library) $(python_includes) BenchMarks_pybind.cpp BenchMarks.cpp -o benchmarks_pybind_libpb$(python_extension)


clean:
	rm -f benchmarks_pybind_libpb$(python_extension) cpp_run benchmarks_libpb.so
