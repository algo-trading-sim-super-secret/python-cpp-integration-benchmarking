# from typing import str



""" 
Miniture class of Candidate, a function/system to test. Noting speed, memory usage, and return data.
* Should be hashable, have equality, and can be checked quickly


BenchMarksData:
* Collection all tests and functions ran for a given benchmark. 
* Should just be a single class 
* Should have a collection of test ran, the Candidate ran, and the Candidates' results

* Has 4 fields: name, test, candidates, save_candidate_data
** Later should include saving the data in a .csv file or smth, or maybe even printing

"""
from dataclasses import dataclass

import time

def temp_func(n:int,value:str):
    return n*value 

@dataclass(init=True, repr=True, eq=False, order=False, unsafe_hash=False, frozen=False,
           match_args=True, kw_only=False, slots=False, weakref_slot=False)
class Candidate:
    name:str
    func: callable
    time_result:float = -1.0 
    mem_result:float = -1.0
    data:any = None

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, obj:any):
        return isinstance(obj,Candidate) and self.name == obj.name

class Test(dict):
    """A dictionary, with the added parameters stating the format"""
    def __init__(self, format: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = format
    def __repr__(self):
        return f"Test(format={self.format!r}, data={dict(self)!r})"

    def repr_case(self,key):
        assert key in dict(self), f"ValueError: {key} not in Test"
        values = self[key]
        return "[" + ", ".join(f"{fmt}={val}" for fmt, val in zip(self.format, values)) + "]"

class BenchMarks:
    # def __init__(self,name:str, save_candidate_data:bool = False):
    #     self.name = name
    #     self.test = set()
    #     self.candidates = set()
    #     self.save_candidate_data = save_candidate_data 

#     # def add_candidate_name(self,candidate_name:str):
#     #     if candidate_name in self.bench_data:
#     #         raise f"Warning. {candidate_name} exists within the set of candidates already"
#     #     self.add_candidate.add(candidate_name)
#     #
#     #     for test in self.bench_data.keys():
#     #         self.bench_data[test][candidate_name] = None 
#

    def __init__(self, name:str,test:Test, candidates:set[Candidate], save_candidate_data:bool=False):
        self.name = name
        self.test = test

        if type(candidates)==type(set()):
            self.candidates = {candidate.name:candidate for candidate in candidates}
        else:
            self.candidates = candidates 

        self.save_candidate_data = save_candidate_data
        self.results = {test_case_id:{candidate_name: Candidate(candidate_name,self.candidates[candidate_name].func) for candidate_name in self.candidates} for test_case_id in test.keys()}

        assert sum( len(self.results[test_case]) for test_case in self.results.keys()) == len(self.candidates)*len(self.test)



    def perform_test(self,test_case_id:int,candidate_name:str=None, candidate:Candidate=None):
        
        # ensure that candidate and test exist

        # only want to be provided one, and make sure that one is satisfied
        assert candidate_name or candidate and not (candidate_name and candidate), "Only note candidate_name xor candidate" 
        if candidate and candidate not in self.candidates:
            raise f"{candidate.name} does not exist within the set of candidates to test"
        
        if candidate_name and candidate_name not in self.candidates:
            raise f"{candidate_name} does not exist within the set of candidates to test"
        
        if test_case_id not in self.test:
            raise f"{test_case_id} does not exist within the set of test"

        candidate_identifier = candidate_name if candidate_name else candidate.name

        # run test (NOTE: need to add memory timing)
        ## Will have to note differences when running on GPU (need to add torch.cuda.synchronize())
        test_case = self.test[test_case_id]
        candidate_to_test = self.results[test_case_id][candidate_identifier]

        # print(candidate_to_test)

        start_time = time.perf_counter()
        return_data = candidate_to_test.func(*test_case)
        end_time = time.perf_counter()

        # Update results
        candidate_to_test.time_result = end_time - start_time
        candidate_to_test.mem_result = -1.0 #[][] need to figure it out 
        candidate_to_test.data = return_data if self.save_candidate_data else None 

    
    def perform_all_tests(self):
        for test_case_id in self.test.keys():
            for candidate_name in self.results[test_case_id]:
                self.perform_test(test_case_id,candidate_name=candidate_name)


    def format_test_results(self):

        print(f"================== {self.name.upper()} ==================")
 
        candidate_longest_name = 0
        for candidate_name in self.candidates:
             candidate_longest_name = max(candidate_longest_name,len(candidate_name))

        for test_case_id in self.test.keys():
            print(f"============= Test:{self.test.repr_case(test_case_id)} =============")
            for candidate_name in self.results[test_case_id]:
            
                print(f'{candidate_name:<{candidate_longest_name}}\t-> {1000*(self.results[test_case_id][candidate_name].time_result):.2f} ms')

            print()

        


if __name__=='__main__':
    
    
    ## ==================================================
    ## Temporary validation of Candidate objects
    # can1 = Candidate("1",temp_func)
    # can2 = Candidate("1",temp_func)
    # print(can1)
    # print(can1.__class__)python unpack list
    # print(type(can1))
    # print(can1==can2)
    ## ==================================================
    candidates = set([Candidate(f"{idx}",temp_func) for idx in range(3)])
    test = Test(["n","str"],{0:[5,'20'],1:[200,'1']})

    benchMarks = BenchMarks("code_val", test, candidates)
    # benchMarks.perform_test(Test([1,"2"]))
    # benchMarks.format_test_results()

    benchMarks.perform_all_tests()
    benchMarks.format_test_results()
