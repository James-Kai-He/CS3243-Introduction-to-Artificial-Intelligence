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
                subset_above, subset_below = above_target[i], below_target[j]

                for x in subset_above[0]:
                    for y in subset_below[0]:
                        sum_diff = y - x
                        new_above_sum = subset_above[1] + sum_diff
                        new_below_sum = subset_below[1] - sum_diff

                        new_fitness = (
                            current_fitness
                            - (subset_above[1] - target_sum) ** 2
                            - (subset_below[1] - target_sum) ** 2
                            + (new_above_sum - target_sum) ** 2
                            + (new_below_sum - target_sum) ** 2
                        )

                        if new_fitness < current_fitness:
                            subset_above[0].remove(x)
                            subset_above[0].append(y)
                            subset_below[0].remove(y)
                            subset_below[0].append(x)
                            subset_above[1], subset_below[1] = (
                                new_above_sum,
                                new_below_sum,
                            )

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
