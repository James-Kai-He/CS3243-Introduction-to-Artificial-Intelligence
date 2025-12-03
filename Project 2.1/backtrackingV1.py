from typing import Dict, List, Tuple, Callable, Optional


def solve_CSP(input_dict: Dict[str, Dict[str, List[int]]]) -> Optional[Dict[str, int]]:
    domains = input_dict["domains"]
    constraints = input_dict["constraints"]

    # Check constraints
    def is_consistent(var, value, assignment):
        for (var1, var2), constraint in constraints.items():
            if var1 == var and var2 in assignment:
                if not constraint(value, assignment[var2]):
                    return False
            elif var2 == var and var1 in assignment:
                if not constraint(assignment[var1], value):
                    return False
        return True

    # Select the next variable
    def select_unassigned_variable(assignment):
        unassigned_vars = [v for v in domains if v not in assignment]
        return min(unassigned_vars, key=lambda var: len(domains[var]))

    # Forward checking
    def forward_check(var, value, assignment):
        removed = {}
        for (var1, var2), constraint in constraints.items():
            if var1 == var and var2 not in assignment:
                for val in domains[var2][:]:
                    if not constraint(value, val):
                        domains[var2].remove(val)
                        removed.setdefault(var2, []).append(val)
                    if not domains[var2]:
                        return False, removed
            elif var2 == var and var1 not in assignment:
                for val in domains[var1][:]:
                    if not constraint(val, value):
                        domains[var1].remove(val)
                        removed.setdefault(var1, []).append(val)
                    if not domains[var1]:
                        return False, removed
        return True, removed

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
