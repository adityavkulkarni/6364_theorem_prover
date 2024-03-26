import argparse
import time

OUTPUT = []
PROCESSED_KB = {}


def parse_kb_file(filepath):
    """
    Parses the kb.in file
    :param filepath:
    :return: a list of list representing clauses and clause that is to be checked
    """
    initial_kb = []
    with open(filepath, 'r') as f:
        for line in f:
            clause = []
            current_literal = ""
            for char in line:
                if char == ' ':
                    clause.append(current_literal.strip())
                    current_literal = ""
                else:
                    current_literal += char
            if current_literal:
                clause.append(current_literal.strip())
            initial_kb.append(clause)
    last_clause = initial_kb[-1]
    initial_kb = initial_kb[:-1]
    return initial_kb, last_clause


def theorem_prover(kb, clause_to_test):
    """
    Main method to derive a resolution proof
    :param kb: a list of clauses (initial KB)
    :param clause_to_test: clause to prove
    :return: None
    """
    # Create a cache set of unsorted set of clauses
    global PROCESSED_KB
    PROCESSED_KB = set(map(frozenset, kb))
    ind = len(kb) + 1
    # Initial kb
    for i, cl in enumerate(kb, start=1):
        print_stdout(f"{i}. {' '.join(cl)} {{}}")
    # Negation of literals of clause to prove, added to KB
    for c in negate_clause(clause_to_test):
        kb.append([c])
        print_stdout(f"{ind}. {c} {{}}")
        PROCESSED_KB.add(frozenset((c,)))
        ind += 1
    # Resolution proof begins
    for cli, clause1 in enumerate(kb, start=1):
        for clj, clause2 in enumerate(kb[:cli], start=1):
            # Resolve each pair of clause
            status, result = resolve(clause1, clause2)
            if status is False:
                # Contradiction
                print_stdout(f"{ind}. Contradiction {{{cli}, {clj}}}")
                print_stdout("Valid")
                return
            elif status and frozenset(result) not in PROCESSED_KB:
                # New resolved clause, that is not in cache
                PROCESSED_KB.add(frozenset(result))
                kb.append(result)
                print_stdout(f"{ind}. {' '.join(result)} {{{cli}, {clj}}}")
                ind += 1
    print_stdout('Fail')


def negate_clause(clause):
    """
    Method for negating a clause
    :param clause:
    :return:
    """
    n = []
    for literal in clause:
        n.append(f"~{literal}" if "~" not in literal else f"{literal[1]}")
    return n


def resolve(c1, c2):
    """
    Method for resolving two clauses from KB
    :param c1:
    :param c2:
    :return: 1. True if found, False if contradiction, else None
             2. Resolved clause if found
    """
    # Create resolved clause
    resolved = []
    for r1 in c1 + c2:
        if r1 not in resolved:
            resolved.append(r1)
    complete = resolved
    # Resolution begins
    for l1 in c1:
        for l2 in c2:
            if l1 == ('~' + l2) or l2 == ('~' + l1):
                # Remove negations
                resolved.remove(l1)
                resolved.remove(l2)
                if len(resolved) == 0:
                    # Empty resolution
                    return False, []
                elif any(r1 == ('~' + r2) or r2 == ('~' + r1) for r2 in resolved for r1 in resolved):
                    # Completely True resolution
                    return None, []
                else:
                    if set(resolved) in PROCESSED_KB:
                        # Resolved clause already in KB
                        return None, []
                    else:
                        # Proper resolution
                        return True, resolved
    if resolved == complete:
        # Unresolvable clauses
        return None, []


def print_stdout(txt):
    """
    Method to print the output in given format
    :param txt:
    :return:
    """
    global OUTPUT
    print(txt)
    OUTPUT.append(txt)


def test(path):
    """
    Method to test output
    :param path:
    :return:
    """
    print("[DEBUG]Execution time: {:.3f} seconds".format(time.time() - start_time))
    with open(path.replace("in", "out"), "r") as f:
        lines = [x.replace("\n", "") for x in f.readlines()]
    if len(lines) != len(OUTPUT):
        print("[DEBUG]Lists are not equal in length.")
        l_str = '\n'.join(lines)
        print(f"[DEBUG]Expected:\n{l_str}\n")
        l_str = '\n'.join(OUTPUT)
        print(f"[DEBUG]Actual:\n{l_str}\n")
    else:
        unequal_elements = [(elem1, elem2) for elem1, elem2 in zip(lines, OUTPUT) if elem1 != elem2]
        if not unequal_elements:
            print("[DEBUG]Lists are equal.")
        else:
            print("[DEBUG]Lists are not equal.")
            print("[DEBUG]Elements that are not equal:")
            for elem1, elem2 in unequal_elements:
                print(f"[DEBUG]{elem1} (Expected) != {elem2} (Actual)")


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("kb_file",
                        type=str,
                        help="Path to kb file")
    args = parser.parse_args()
    init_kb, ct = parse_kb_file(args.kb_file)
    theorem_prover(init_kb, ct)
    # test(args.kb_file)
