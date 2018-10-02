#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/GrammarCoverageFuzzer.html
# Last change: 2018-10-01 06:50:42-07:00
#
#
# Copyright (c) 2018 Saarland University, CISPA, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# # Grammar Coverage

if __name__ == "__main__":
    print('# Grammar Coverage')




# ## Covering Grammar Elements

if __name__ == "__main__":
    print('\n## Covering Grammar Elements')




# import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from Grammars import DIGIT_GRAMMAR, EXPR_GRAMMAR, CGI_GRAMMAR, URL_GRAMMAR, START_SYMBOL
else:
    from .Grammars import DIGIT_GRAMMAR, EXPR_GRAMMAR, CGI_GRAMMAR, URL_GRAMMAR, START_SYMBOL


if __package__ is None or __package__ == "":
    from GrammarFuzzer import GrammarFuzzer, all_terminals, nonterminals, display_tree
else:
    from .GrammarFuzzer import GrammarFuzzer, all_terminals, nonterminals, display_tree


import random

class GrammarCoverageFuzzer(GrammarFuzzer):
    def __init__(self, *args, **kwargs):
        # invoke superclass __init__(), passing all arguments
        super().__init__(*args, **kwargs)
        self.reset_coverage()

    def reset_coverage(self):
        self.covered_expansions = set()

    def expansion_coverage(self):
        return self.covered_expansions


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR)
    f.fuzz()


class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def expansion_key(self, symbol, children):
        """Convert (symbol, children) into a key.  `children` can be an expansion string or a derivation tree."""
        if not isinstance(children, str):
            children = all_terminals((symbol, children))
        return symbol + " -> " + children

    def max_expansion_coverage(self):
        """Return set of all expansions in a grammar"""
        expansions = set()
        for nonterminal in self.grammar:
            for expansion in self.grammar[nonterminal]:
                expansions.add(self.expansion_key(nonterminal, expansion))
        return expansions

if __name__ == "__main__":
    f = GrammarCoverageFuzzer(DIGIT_GRAMMAR)
    f.max_expansion_coverage()


class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def choose_node_expansion(self, node, possible_children):
        # Prefer uncovered expansions
        (symbol, children) = node
        uncovered_children = [(i, c) for (i, c) in enumerate(possible_children)
                              if self.expansion_key(symbol, c) not in self.covered_expansions]

        # print("Uncovered:", uncovered_children)

        if len(uncovered_children) == 0:
            # All expansions covered - use superclass method
            if self.log:
                print("All", symbol, "alternatives covered")

            return super().choose_node_expansion(node, possible_children)

        # select a random expansion
        index = random.randrange(len(uncovered_children))
        (new_children_index, new_children) = uncovered_children[index]

        # Save the expansion as covered
        key = self.expansion_key(symbol, new_children)
        assert key not in self.covered_expansions

        if self.log:
            print("Now covered:", key)
        self.covered_expansions.add(key)

        return new_children_index


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(DIGIT_GRAMMAR, log=True)
    f.fuzz()


if __name__ == "__main__":
    f.fuzz()


if __name__ == "__main__":
    f.fuzz()


if __name__ == "__main__":
    f.covered_expansions


if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR)
    for i in range(10):
        print(f.fuzz())


if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


# ## Grammar Coverage and Code Coverage

if __name__ == "__main__":
    print('\n## Grammar Coverage and Code Coverage')




if __name__ == "__main__":
    f = GrammarCoverageFuzzer(CGI_GRAMMAR)


if __name__ == "__main__":
    for i in range(10):
        print(f.fuzz())


if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


# ## Deep Foresight

if __name__ == "__main__":
    print('\n## Deep Foresight')




class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def _max_symbol_expansion_coverage(
            self, symbol, max_depth, cov, symbols_seen):
        """Return set of all expansions in a grammar starting with `symbol`"""
        if max_depth > 0:
            symbols_seen.add(symbol)
            for expansion in self.grammar[symbol]:
                key = self.expansion_key(symbol, expansion)
                if key not in cov:
                    cov.add(key)
                    for s in nonterminals(expansion):
                        if s not in symbols_seen:
                            new_cov, new_symbols_seen = self._max_symbol_expansion_coverage(s, max_depth - 1,
                                                                                            cov, symbols_seen)
                            cov |= new_cov
                            symbols_seen |= new_symbols_seen

        return (cov, symbols_seen)

    def max_symbol_expansion_coverage(self, symbol, max_depth=float('inf')):
        cov, symbols_seen = self._max_symbol_expansion_coverage(
            symbol, max_depth, set(), set())
        return cov


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR)
    f.max_symbol_expansion_coverage('<integer>')


if __name__ == "__main__":
    f.max_symbol_expansion_coverage('<digit>')


if __name__ == "__main__":
    assert f.max_expansion_coverage() == f.max_symbol_expansion_coverage(START_SYMBOL)


class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def _new_child_coverage(self, children, max_depth):
        new_cov = set()
        for (c_symbol, _) in children:
            if c_symbol in self.grammar:
                new_cov |= self.max_symbol_expansion_coverage(
                    c_symbol, max_depth)
        return new_cov

    def new_child_coverage(self, symbol, children, max_depth):
        new_cov = self._new_child_coverage(children, max_depth)
        for c in children:
            new_cov.add(self.expansion_key(symbol, children))
        new_cov -= self.expansion_coverage()
        return new_cov


class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def choose_node_expansion(self, node, possible_children):
        # Prefer uncovered expansions
        (symbol, children) = node
        # print("Possible children:", possible_children)

        # Find maximum depth at which we discover uncovered nodes
        for max_depth in range(len(self.grammar)):
            new_coverages = [
                self.new_child_coverage(
                    symbol, c, max_depth) for c in possible_children]
            max_new_coverage = max(len(new_coverage)
                                   for new_coverage in new_coverages)
            if max_new_coverage > 0:
                break

        if max_new_coverage == 0:
            # All expansions covered - use superclass method
            if self.log:
                print("All", symbol, "alternatives covered")
            return super().choose_node_expansion(node, possible_children)

        if self.log:
            print("New coverages at depth", max_depth)
            for i in range(len(possible_children)):
                print(i,
                      possible_children[i],
                      new_coverages[i],
                      len(new_coverages[i]))

        children_with_max_new_coverage = [(i, c) for (i, c) in enumerate(possible_children)
                                          if len(new_coverages[i]) == max_new_coverage]
        if self.log:
            print("Children with max new coverage:",
                  [c for (i, c) in children_with_max_new_coverage])

        # select a random expansion
        new_children_index, new_children = random.choice(
            children_with_max_new_coverage)

        # Save the expansion as covered
        key = self.expansion_key(symbol, new_children)

        if self.log:
            print("Now covered:", key)
        self.covered_expansions.add(key)

        return new_children_index


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR, min_nonterminals=3)
    f.fuzz()


if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(CGI_GRAMMAR, min_nonterminals=5)
    for i in range(10):
        print(f.fuzz(), f.max_expansion_coverage() - f.expansion_coverage())


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(URL_GRAMMAR, min_nonterminals=5)
    for i in range(10):
        print(f.fuzz(), f.max_expansion_coverage() - f.expansion_coverage())


# ## Combinatorial Coverage

if __name__ == "__main__":
    print('\n## Combinatorial Coverage')




def flatten_tree(tree):
    """Return `tree` without grandchildren"""
    (symbol, children) = tree
    if children is None:
        return symbol
    new_children = [c for (c, _) in children]
    return (symbol, new_children)

def match_path(path, tree):
    def _match_path(path, tree):
        (symbol, children) = tree
        (path_symbol, path_children) = path
        if symbol != path_symbol:
            return False

        if path_children is not None and len(path_children) > 0:
            if len(children) > 1:
                # Multiple children given; must all match
                if len(children) != len(path_children):
                    return False
                return all(_match_path(
                    path_children[i], children[i]) for i in range(len(children)))
            # One child given; can match any
            return any(_match_path(path_children[0], c) for c in children)
        else:
            return True

    # print("Matching", path, "in", tree)
    matched = _match_path(path, tree)
    # print("Matched" if matched else "Did not match", path, "in", tree)
    return matched


if __name__ == "__main__":
    derivation_tree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])
    display_tree(derivation_tree)



if __name__ == "__main__":
    path = ("<start>", None)

    assert match_path(path, derivation_tree)


if __name__ == "__main__":
    start_tree = ('<start>', [('4', [])])
    display_tree(start_tree)


if __name__ == "__main__":
    path = ('<start>', [('4', None)])

    assert match_path(start_tree, path)


def find_path(path, tree):
    def _find_path(path, tree):
        (symbol, children) = tree
        (path_symbol, path_children) = path
        if symbol == path_symbol:
            if len(path_children) == 1:
                # One child given: any can match
                if any(match_path(path_children[0], c) for c in children):
                    return True
            elif match_path(path, tree):
                # Multiple children given; must all match
                return True

        return any(_find_path(path, c) for c in children)

    # print("Searching", path, "in", tree)
    found = _find_path(path, tree)
    # print("Found" if found else "Did not find", path, "in", tree)
    return found

if __name__ == "__main__":
    path = ("<expr>", [(" + ", None)])

    assert find_path(path, derivation_tree)
    assert not match_path(path, derivation_tree)


class CombinatorialCoverageFuzzer(GrammarFuzzer):
    def __init__(self, *args, **kwargs):
        # invoke superclass __init__(), passing all arguments
        super().__init__(*args, **kwargs)
        self.reset_coverage()

    def reset_coverage(self):
        self._current_depth = 0
        self.covered_expansions = set()

    def expand_tree_once(self, tree):
        if self._current_depth == 0:
            self._current_tree = tree
        self._current_depth += 1
        tree = super().expand_tree_once(tree)
        self._current_depth -= 1
        return tree


if __name__ == "__main__":
    f = CombinatorialCoverageFuzzer(EXPR_GRAMMAR)
    f.fuzz()


class CombinatorialCoverageFuzzer(CombinatorialCoverageFuzzer):
    def path_to_node(self, tree, node):
        (symbol, children) = tree
        if id(tree) == id(node):
            return node

        if children is None:
            return None

        for c in children:
            p = self.path_to_node(c, node)
            if p is not None:
                return (symbol, [p])

        return None


if __name__ == "__main__":
    derivation_tree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])
    display_tree(derivation_tree)



if __name__ == "__main__":
    node = derivation_tree[1][0][1][0]
    node


if __name__ == "__main__":
    f = CombinatorialCoverageFuzzer(EXPR_GRAMMAR)
    path = f.path_to_node(derivation_tree, node)
    path


if __name__ == "__main__":
    display_tree(path)


class CombinatorialCoverageFuzzer(CombinatorialCoverageFuzzer):
    def subpath(self, path, height):
        def _subpath(path, height):
            # print(path, height)
            (symbol, children) = path
            if children is None or len(children) == 0:
                return (path, 0)

            subpath, subheight = _subpath(children[0], height)
            if subheight < height:
                return ((symbol, [subpath]), subheight + 1)
            else:
                return (subpath, subheight)

        subpath, subheight = _subpath(path, height)
        return subpath


if __name__ == "__main__":
    f = CombinatorialCoverageFuzzer(EXPR_GRAMMAR)
    f.subpath(path, height=0)


if __name__ == "__main__":
    f.subpath(path, height=1)


if __name__ == "__main__":
    f.subpath(('<start>', [('<expr>', [('<expr>', None)])]), height=0)


class CombinatorialCoverageFuzzer(CombinatorialCoverageFuzzer):
    def append_to_path(self, path, new_children):
        (symbol, children) = path
        if children is None or len(children) == 0:
            return (symbol, new_children)
        else:
            assert len(children) == 1
            return (symbol, [self.append_to_path(children[0], new_children)])

if __name__ == "__main__":
    f = CombinatorialCoverageFuzzer(EXPR_GRAMMAR)
    new_children = [("<term>", None)]


if __name__ == "__main__":
    new_path = f.append_to_path(path, new_children)
    display_tree(new_path)


class CombinatorialCoverageFuzzer(CombinatorialCoverageFuzzer):
    def expansion_key(self, path):
        return repr(path)

    def choose_node_expansion(self, node, possible_children):
        (symbol, children) = node

        path_to_node = self.path_to_node(self._current_tree, node)
        # print(path_to_node)

        for path_height in range(0, len(path_to_node)):
            possible_indexes = []
            subpath = self.subpath(path_to_node, height=path_height)

            if self.log:
                print(
                    "Choosing from subpaths of height",
                    path_height,
                    ":",
                    subpath)

            for i in range(len(possible_children)):
                expansion_path = self.append_to_path(
                    subpath, possible_children[i])
                key = self.expansion_key(expansion_path)
                if key not in self.covered_expansions:
                    # print(key, "not seen before")
                    possible_indexes.append(i)

            if len(possible_indexes) > 0:
                index = random.choice(possible_indexes)
                expansion_path = self.append_to_path(
                    subpath, possible_children[index])
                key = self.expansion_key(expansion_path)
                assert key not in self.covered_expansions
                self.covered_expansions.add(key)
                return index

        if self.log:
            print("All combinations covered")
        return super().choose_node_expansion(node, possible_children)


if __name__ == "__main__":
    f = CombinatorialCoverageFuzzer(EXPR_GRAMMAR)

    for i in range(10):
        before = len(f.covered_expansions)
        s = f.fuzz()
        after = len(f.covered_expansions)
        print(s, "  #", after - before, "new")


if __name__ == "__main__":
    f.covered_expansions


# ## Advanced Grammar Coverage Metrics

if __name__ == "__main__":
    print('\n## Advanced Grammar Coverage Metrics')




# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1

if __name__ == "__main__":
    print('\n### Exercise 1')




if __name__ == "__main__":
    # Some code that is part of the exercise
    pass


if __name__ == "__main__":
    # Some code for the solution
    2 + 2


# ### Exercise 2

if __name__ == "__main__":
    print('\n### Exercise 2')



