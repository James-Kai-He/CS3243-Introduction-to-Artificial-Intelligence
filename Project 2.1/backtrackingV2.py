from typing import Dict, List, Tuple, Callable, Optional


def solve_CSP(input_dict: Dict[str, Dict[str, List[int]]]) -> Optional[Dict[str, int]]:
    domains = input_dict["domains"]
    constraints = input_dict["constraints"]

    # Check constraints
    def is_consistent(var, value, assignment):
        for (var1, var2), constraint in constraints.items():
            if (
                var1 == var
                and var2 in assignment
                and not constraint(value, assignment[var2])
            ) or (
                var2 == var
                and var1 in assignment
                and not constraint(assignment[var1], value)
            ):
                return False
        return True

    # Select the next variable
    def select_unassigned_variable(assignment):
        return min(
            [v for v in domains if v not in assignment],
            key=lambda var: len(domains[var]),
        )

    # Forward checking
    def forward_check(var, value, assignment):
        removed = {}
        for (var1, var2), constraint in constraints.items():
            if var1 == var and var2 not in assignment:
                to_remove = [val for val in domains[var2] if not constraint(value, val)]
                if to_remove:
                    removed[var2] = to_remove
                    domains[var2] = [
                        val for val in domains[var2] if val not in to_remove
                    ]
                    if not domains[var2]:
                        return False, removed
            elif var2 == var and var1 not in assignment:
                to_remove = [val for val in domains[var1] if not constraint(val, value)]
                if to_remove:
                    removed[var1] = to_remove
                    domains[var1] = [
                        val for val in domains[var1] if val not in to_remove
                    ]
                    if not domains[var1]:
                        return False, removed
        return True, removed

    # Restore domains after forward checking
    def restore_domains(removed):
        for var, values in removed.items():
            domains[var].extend(values)

    # Backtracking search function
    def backtrack(assignment):
        if len(assignment) == len(domains):
            return assignment

        var = select_unassigned_variable(assignment)
        for value in domains[var]:
            if is_consistent(var, value, assignment):
                assignment[var] = value
                success, removed = forward_check(var, value, assignment)

                if success:
                    result = backtrack(assignment)
                    if result:
                        return result

                del assignment[var]
                restore_domains(removed)

        return None

    return backtrack({})
