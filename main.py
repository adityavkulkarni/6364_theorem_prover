"""
https://github.com/nomaanakhan/Theorem-Prover-for-Clause-Logic
https://github.com/codeCollision4/resolution_solver
"""
import argparse
import time
from multiprocessing import Pool

OUTPUT = []


def parse_kb_file(filepath):
    initial_kb = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
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


def negate_clause(clause):
    n = []
    for literal in clause:
        n.append(f"~{literal}" if "~" not in literal else f"{literal[1]}")
    return n


def theorem_prover(kb, clause_to_test):
    negated_clause = negate_clause(clause_to_test)
    ind = len(kb) + 1
    existing_clauses = set(map(tuple, kb))

    for i, cl in enumerate(kb, start=1):
        print_stdout(f"{i}. {' '.join(cl)} {{}}")

    for c in negated_clause:
        kb.append([c])
        print_stdout(f"{ind}. {c} {{}}")
        existing_clauses.add((c,))
        ind += 1

    for cli, clause1 in enumerate(kb, start=1):
        for clj, clause2 in enumerate(kb[:cli], start=1):
            result = resolve(clause1, clause2, existing_clauses)
            if result is False:
                print_stdout(f"{ind}. Contradiction {{{cli}, {clj}}}")
                print_stdout("Valid")
                return
            elif result is not True and tuple(result) not in existing_clauses:
                existing_clauses.add(tuple(result))
                kb.append(result)
                print_stdout(f"{ind}. {' '.join(result)} {{{cli}, {clj}}}")
                ind += 1
    print_stdout('Not Valid')


def resolve(c1, c2, clauses):
    resolved2 = c1 + c2
    hashmap = {}
    for r1 in resolved2:
        if r1 not in hashmap.keys():
            hashmap[r1] = 0

    resolved = list(hashmap.keys())
    ors = list(hashmap.keys())
    for l1 in c1:
        for l2 in c2:
            if is_contradiction(l1, l2):
                resolved.remove(l1)
                resolved.remove(l2)
                if len(resolved) == 0:
                    return False
                elif impTrue(resolved):
                    return True
                else:
                    if any(map(lambda cl: not Diff(resolved, cl), clauses)):
                        return True
                    return resolved
    if resolved == ors:
        return True


def is_contradiction(l1, l2):
    if l1 == ('~' + l2) or l2 == ('~' + l1):
        return True
    else:
        return False


def impTrue(resolved):
    seen = set()
    for i, r1 in enumerate(resolved):
        for r2 in resolved[i + 1:]:
            if (r1, r2) in seen or (r2, r1) in seen:
                continue
            if is_contradiction(r1, r2):
                return True
            seen.add((r1, r2))
    return False



def Diff(li1, li2):
    set1 = set(li1)
    set2 = set(li2)
    return list(set1.symmetric_difference(set2))


def print_stdout(txt):
    global OUTPUT
    print(txt)
    OUTPUT.append(txt)


def test(path):
    print("Execution time: {:.3f} seconds".format(time.time() - start_time))
    with open(path.replace("in", "out"), "r") as f:
        lines = [x.replace("\n", "") for x in f.readlines()]
    if len(lines) != len(OUTPUT):
        print("Lists are not equal in length.")
        l_str = '\n'.join(lines)
        print(f"Expected:\n{l_str}\n")
        l_str = '\n'.join(OUTPUT)
        print(f"Actual:\n{l_str}\n")
    else:
        unequal_elements = [(elem1, elem2) for elem1, elem2 in zip(lines, OUTPUT) if elem1 != elem2]
        if not unequal_elements:
            print("Lists are equal.")
        else:
            print("Lists are not equal.")
            print("Elements that are not equal:")
            for elem1, elem2 in unequal_elements:
                print(f"{elem1} (Expected) != {elem2} (Actual)")


if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("kb_file",
                        type=str,
                        help="Path to kb file")
    args = parser.parse_args()
    init_kb, ct = parse_kb_file(args.kb_file)
    theorem_prover(init_kb, ct)
    test(args.kb_file)
