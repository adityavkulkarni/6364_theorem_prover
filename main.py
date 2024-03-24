import argparse
import time

OUTPUT = []
PROCESSED_KB = {}


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


def theorem_prover(kb, clause_to_test):
    global PROCESSED_KB
    negated_clause = negate_clause(clause_to_test)
    ind = len(kb) + 1
    PROCESSED_KB = set(map(frozenset, kb))
    for i, cl in enumerate(kb, start=1):
        print_stdout(f"{i}. {' '.join(cl)} {{}}")
    for c in negated_clause:
        kb.append([c])
        print_stdout(f"{ind}. {c} {{}}")
        PROCESSED_KB.add(frozenset((c, )))
        ind += 1
    for cli, clause1 in enumerate(kb, start=1):
        for clj, clause2 in enumerate(kb[:cli], start=1):
            result = resolve(clause1, clause2)
            if result is False:
                print_stdout(f"{ind}. Contradiction {{{cli}, {clj}}}")
                print_stdout("Valid")
                return
            elif result is not True and frozenset(result) not in PROCESSED_KB:
                PROCESSED_KB.add(frozenset(result))
                kb.append(result)
                print_stdout(f"{ind}. {' '.join(result)} {{{cli}, {clj}}}")
                ind += 1
    print_stdout('Not Valid')


def negate_clause(clause):
    n = []
    for literal in clause:
        n.append(f"~{literal}" if "~" not in literal else f"{literal[1]}")
    return n


def resolve(c1, c2):
    resolved = []
    for r1 in c1 + c2:
        if r1 not in resolved:
            resolved.append(r1)
    ors = resolved
    for l1 in c1:
        for l2 in c2:
            if l1 == ('~' + l2) or l2 == ('~' + l1):
                resolved.remove(l1)
                resolved.remove(l2)
                if len(resolved) == 0:
                    return False
                elif any(r1 == ('~' + r2) or r2 == ('~' + r1) for r2 in resolved for r1 in resolved):
                    return True
                else:
                    return True if set(resolved) in PROCESSED_KB else resolved
    if resolved == ors:
        return True


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
