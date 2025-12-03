# Project 1.1 Public Test Cases Description

This README file describes the public test cases for project 1.1. These public test cases are designed to catch common errors in the project implementation. The public test cases are not comprehensive and passing all the public test cases does not guarantee a good grade. You are encouraged to design your own test cases to test your implementation and to reason about your implementation.

## Correctness Test Cases

All the correctness test cases are located in the `correctness` directory. The test case name is in one of the two formats:
    - `correctness_public_<test_case_type>_<test_case_number>_<size>.txt`, or;
    - `correctness_public_<test_case_type>_<size>.txt`
The test case types are one of: `dummy_correct`, `dummy_complete`, `ab_small`, `b_small`, `bt_small`. Test cases whose type is prefixed with `dummy` will use the second format, while the rest will use the first format.

You are encouraged to use the `dummy` test cases to help debug your initial implementation. These test cases are all small (size 9 x 9) and thus can easily be traced by hand. The `dummy_correct` test cases are designed to test for correctness i.e. correct path for DFS and optimal path for BFS and UCS. The `dummy_complete` test cases are designed to test for completeness i.e. paths are produced when possible, and no paths are produced when not possible.

The `ab_small`, `b_small`, and `bt_small` test cases are designed to test for correctness and completeness. They have been generated using different maze-generation algorithms, specifically: `Aldous-Broder`, `Backtracking`, and `Binary Tree`, with minor modifications. The different algorithms lead to different kinds of mazes; for example, the `Backtracking` algorithm tend to create mazes with low branching factors, whereas the `Binary Tree` algorithm has strong bias towards certain places in the maze. If your implementation passes all the `dummy` test cases, but fails on the `ab_small`, `b_small`, or `bt_small` test cases, then it is likely that your implementation is not general enough to handle all kinds of mazes. You may construct your own mazes based on the characteristics of the mazes that your implementation fails on to help debug your implementation. You may also look into the maze-generation algorithms to understand the differences between the mazes.

## Efficiency Test Cases

All the efficiency test cases are located in the `efficiency` directory. The test case name is in the format: `efficiency_public_<test_case_type>_<size>.txt`.

These test cases are scaled-up versions of the correctness test cases, made using the corresponding maze-generation algorithm. The largest test case has a size of 1101 x 1101.

## Hints

The following are some hints that may help you with the project. You may choose to ignore these hints, especially if you would like to not be "spoiled" by the hints.

1. Do NOT use the tree search implementation of the algorithms. The search space is too large (can you do a rough estimate of the search space size?) and the search will take too long to complete. You should use the graph search implementation of the algorithms.
2. Do NOT use recursion to implement DFS. There is a limit to the maximum recursion depth in Python. You should use an explicit stack to implement DFS.
3. Experiment between early and late goal test for the different algorithms. Which one is more efficient? Why?
4. Python-related:
   1. The `PriorityQueue` module has certain concurrency-related overheads. You may want to use the `heapq` module instead.
   2. For custom classes, you may or may need to implement the `__eq__`, `hash`, and `__lt__` methods. See the Python documentation for more details. In particular, the `__eq__` and `__hash__` methods will be useful for `set` membership testing, and the `__lt__` method will be useful for priority queue ordering.
5. Certain "optimisations" can be helpful, but should be reserved towards the end once you are certain that no other, more obvious optimisations can be made to your implementations. These "optimisations" include:
   1. Different data structures may lead to better performance even though they have the same or worse asymptotic complexity. For example, a `list` can be faster than a `set` for membership testing if the elements to be tested are in known locations in the `list`.
   2. Movement ordering can be important especially for algorithms with no optimal path guarantee
   3. For variables that are repeatedly accessed without modification, it can be faster to use global variables instead of passing them as parameters to functions.
   4. And many more...
