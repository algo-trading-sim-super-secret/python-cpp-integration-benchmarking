#include <pybind11/pybind11.h>
#include "BenchMarks.h"

namespace py = pybind11;

PYBIND11_MODULE(benchMarks_pybind_libpb, m) {
    py::class_<BenchMarks>(m, "BenchMarks")
        .def("matrixComputation", &BenchMarks::matrixComputation);
#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
