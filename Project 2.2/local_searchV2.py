import random
import itertools


def calculate_fitness(subsets, target_sum):
    return sum((subset[1] - target_sum) ** 2 for subset in subsets)


def search(input_dict):
    count = input_dict["count"]
    size = input_dict["size"]
    values = sorted(input_dict["values"], reverse=True)
    total_sum = sum(values)
    target_sum = total_sum // count

    def initialize_random_partition():
        random.shuffle(values)
        subsets = [
            [values[i * size : (i + 1) * size], sum(values[i * size : (i + 1) * size])]
            for i in range(count)
        ]
        return subsets

    best_solution = None
    best_fitness = float("inf")

    while best_fitness > 0:
        subsets = initialize_random_partition()
        current_fitness = calculate_fitness(subsets, target_sum)
        improving = True

        while improving:
            improving = False
            above_target = [s for s in subsets if s[1] > target_sum]
            below_target = [s for s in subsets if s[1] < target_sum]

            found_better = False
            for i, j in itertools.product(
                range(len(above_target)), range(len(below_target))
            ):
                for x in range(size):
                    for y in range(size):
                        value_above, value_below = (
                            above_target[i][0][x],
                            below_target[j][0][y],
                        )
                        sum_diff = value_below - value_above
                        new_above_sum = above_target[i][1] + sum_diff
                        new_below_sum = below_target[j][1] - sum_diff
                        new_fitness = (
                            current_fitness
                            - (above_target[i][1] - target_sum) ** 2
                            - (below_target[j][1] - target_sum) ** 2
                        )
                        new_fitness += (new_above_sum - target_sum) ** 2 + (
                            new_below_sum - target_sum
                        ) ** 2

                        if new_fitness < current_fitness:
                            above_target[i][0][x], below_target[j][0][y] = (
                                value_below,
                                value_above,
                            )
                            above_target[i][1] = new_above_sum
                            below_target[j][1] = new_below_sum
                            current_fitness = new_fitness
                            improving = True
                            found_better = True
                            break
                    if found_better:
                        break
                if found_better:
                    break

            if current_fitness < best_fitness:
                best_fitness = current_fitness
                best_solution = [[val for val in subset[0]] for subset in subsets]

    return best_solution
