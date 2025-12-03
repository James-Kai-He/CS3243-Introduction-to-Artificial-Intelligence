# Project 1.2 Public Test Cases Description

This README file describes the public test cases for the project. These public test cases are designed to catch common errors in the project implementation. Many of the information from project 1.1 still applies; you are encouraged to read the project 1.1 public test cases description before reading this.

## Correctness Test Cases

All the correctness test cases are located in the `correctness` directory. The test case name is in one of the two formats:
    - `correctness_public_<test_case_type>_<test_case_number>_<size>.txt`, or;
    - `correctness_public_<test_case_type>_<size>.txt`
The test case types are one of: `dummy_correct`, `dummy_creeps`, `dummy_no_creeps`, `ab_small`, `b_small`, `bt_small`. Test cases whose type is prefixed with `dummy` will use the second format, while the rest will use the first format.

You are encouraged to use the `dummy` test cases to help debug your initial implementation. These test cases are all small (size 9 x 9) and thus can easily be traced by hand. The `dummy_correct` test cases are designed to test for correctness i.e. correct path for DFS and optimal path for BFS and UCS.

The `dummy_simple` test cases have no skills and no creeps in the maze. These test cases are designed to test whether you have ported the necessary code from your project 1.1 implementation to your project 1.2 implementation correctly.

The `dummy_no_creeps` test cases have skills but no creeps in the maze. These test cases are designed to test whether you have implemented `FLASH` and `NUKE` skills correctly.

The `dummy_creeps` test cases have both skills and creeps in the maze. These test cases are designed to test for the optimality of your search algorithm.

The `ab_small`, `b_small`, and `bt_small` test cases are designed to test for correctness and completeness. You may refer to the project 1.1 public test cases description for more information on how these test cases are generated.

### Examples

To aid in your understanding of the test cases better, we use some of the public test cases as examples in this section. The optimal action sequences will be revealed, along with the reason why they are optimal.

1. `correctness_public_dummy_no_creeps_0.json`
   This is a correctness test case with type `dummy_no_creeps`. Hence, there are no creeps in the maze. The test case number is 0. You are allowed to use FLASH 3 times and NUKE 0 time. The maze size is 9 x 9.

    [[-1. -1. -1. -1. -1. -1. -1. -1. -1.]
     [-1.  0.  0.  0. -1.  0.  0.  0. -1.]
     [-1.  0. -1. -1. -1.  0. -1. -1. -1.]
     [-1.  0. -1.  0.  0.  0.  0.  0. -1.]
     [-1.  0. -1.  0. -1.  0. -1.  0. -1.]
     [-1.  0.  0.  0.  0.  0. -1.  0. -1.]
     [-1.  0. -1. -1. -1. -1. -1.  0. -1.]
     [-1.  0. -1.  0.  0.  0.  0.  0. -1.]
     [-1. -1. -1. -1. -1. -1. -1. -1. -1.]]
    Figure 1: Maze visualisation, where -1 indicates obstacle and 0 indicates empty space.

    The agent starts at (7, 3) and goals are [(1, 3)]. The best action sequence is 4 x RIGHT, 4 x UP, 4 x LEFT, 2 x DOWN, 2 x LEFT, 4 x UP, 2 x RIGHT. Note how the action sequence brings us to the goal. This action sequence has a cost of (4 + 4 + 4 + 2 + 2 + 4 + 2) *4 MP = 88 MP.

    [[You may skip this part if you are not interested in proving the optimality of the above action sequence.]]
    Claim: No other action sequences that have a lower cost.
    Proof: By inspection, we can see that if no skills are allowed, the proposed action sequence is optimal. We are left to show that the use of skills cannot further lower the cost. For NUKE, this is trivial, since there are no creeps in the maze. For FLASH, note that the skill FLASH costs 10 + 2n, where n is the number of steps taken. On the other hand, standard movements cost 4n. Thus, FLASH only makes sense when 10 + 2n < 4n i.e. n > 5. Since in the proposed action sequence, no particular direction is taken more than 5 times, it is not possible to use FLASH to reduce the cost of the action sequence.

2. `correctness_public_dummy_no_creeps_8.json`
    The starting position is (5, 7) and one of the goal is (5, 7). Hence, taking no action is optimal i.e. return an empty action sequence.

3. `correctness_public_dummy_creeps_4.json`
    This is a correctness test case with type `dummy_creeps`. Hence, there are creeps in the maze. The test case number is 4. You are allowed to use FLASH 2 times and NUKE 1 time. The maze size is 9 x 9.
    [[-1. -1. -1. -1. -1. -1. -1. -1. -1.]
     [-1. 27. 53. 83. -1.  0. -1.  0. -1.]
     [-1.  0. -1. -1. -1. 40. -1.  0. -1.]
     [-1. 56.  0.  0. 41.  0. 83. 96. -1.]
     [-1. -1. -1. 55. -1. -1. -1. 89. -1.]
     [-1. 95.  0.  0. -1.  0.  0. 26. -1.]
     [-1. 14. -1. -1. -1.  0. -1. -1. -1.]
     [-1. 59. -1. 74.  0. 60. 11. 59. -1.]
     [-1. -1. -1. -1. -1. -1. -1. -1. -1.]]
     Figure 2: Maze visualisation, where -1 indicates obstacle, 0 indicates empty space, and the numbers indicate the number of creeps.

    The agent starts at (1, 3) and the goals are [(7, 3)]. The proposed action sequence is NUKE, LEFT, LEFT, DOWN, DOWN, FLASH, RIGHT, DOWN, DOWN, LEFT, LEFT, DOWN, DOWN, LEFT, LEFT. Note that this action sequence brings the agent to the goal. The cost of this sequence is 120, with the following breakdown:
    - NUKE: 50 [Creep costs is zeroed for all cells within 10 Manhattan Distance of (1, 3)]
    - LEFT, LEFT, DOWN, DOWN: 4 x 4 = 16
    - FLASH: 10
    - RIGHT: 6 x 2 = 12 [2 instead of 4 due to previous casting of FLASH]
    - DOWN, DOWN, LEFT, LEFT, DOWN, DOWN, LEFT, LEFT: 8 x 4 = 32

    Note that since the maze is 9 x 9, the initial cast of NUKE removes all creeps from the maze. Thus, no creep costs are incurred for the rest of the action sequence. This is not true for larger mazes.

    [[You may skip this part if you are not interested in proving the optimality of the above action sequence.]]
    Claim: No other action sequences that have a lower cost.
    "Proof": Remove all skills from the action sequence appropriately. By inspection, this is the only action sequence that brings the agent to the goal. We are thus left with adding skill usage to further lower the cost. The use of NUKE at the start of the action sequence will strictly improve all solutions that does not use NUKE, as there are no action sequence that can avoid at most 50 creeps to reach one of the goal. Since NUKE removes creeps at the cost of 50 MP, then the use of NUKE has to improve the cost. As for the use of FLASH, it is easy to show that doing 6 x RIGHT would have cost 6 x 4 = 32. On the other hand, FLASH -> RIGHT only costs 22 in total. Thus, the proposed action sequence is optimal.

## Efficiency Test Cases

All the efficiency test cases are located in the `efficiency` directory. The test case name is in the format: `efficiency_public_<test_case_type>_<size>.txt`.

These test cases test for the efficiency of your implementation under a large search space regime. Note that this does not mean the mazes are large; the smallest test case has size 25 x 25.

If you are unable to pass the test cases with suffix `_small`, it is likely that there are better ways to model the skills in your implementation. You may want to revisit your implementation and see if there are any obvious optimisations that you have missed.

If you are unable to pass the test cases with suffix `_medium`, it is likely that there are better ways to implement to your overall search algorithm. You may want to revisit your implementation and see if there are any obvious optimisations that you have missed.

## Hints

All the hints from project 1.1 still applies; you are encouraged to read the project 1.1 public test cases description before reading this.

1. The most basic approach is to model the agent to have 6 actions: `UP`, `DOWN`, `LEFT`, `RIGHT`, `FLASH`, and `NUKE`. This approach is simple to implement. However, there are other ways of modelling the agent. What are they? What are the pros and cons of each approach? [This does not mean that you cannot use the basic approach.]

2. What are other information other than the agent's position that you need to track? What does it mean for a state to be "visited" in this project?

3. Recall that an admissible heuristic is needed for A\* graph search V2, whereas a consistent heuristic is needed for A\* graph search V3. What heuristics can you think of for this project? Are they admissible or consistent?
   1. A heuristic need not be something complicated
   2. Since the heuristic `h` is added to the path cost `g`, and the cost `g` has a certain semantics attached to it (distance in this case), it is likely that the heuristic `h` has a similar semantics.
