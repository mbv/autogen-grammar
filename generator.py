from grammar import *
import random

LEN_RULES = 2


class AutoGenerateText:
    def __init__(self, sequences):
        self.sequences = sequences
        self.grammar = Grammar()
        self.level = 1

    def run(self):
        self.first_step()
        self.second_step()
        self.third_step()
        self.print_result()
        self.print_example()

    def sort_sequences(self):
        self.sequences.sort(key=len, reverse=True)

    def get_new_grammar(self, grammar, letter):
        if self.grammar != grammar and len(grammar.nodes) == 0:
            grammar.set_level(self.level)
            self.level += 1
        return Grammar(letter, grammar)

    def update_grammar_level(self, grammar, letter):
        for node in grammar.nodes:
            if node.is_equals(letter):
                grammar = node
                break
        else:
            new_node = self.get_new_grammar(grammar, letter)
            grammar.add_node(new_node)
            grammar = new_node
        return grammar

    @staticmethod
    def print_used_line(line):
        print('Use "{0}"'.format(line))

    def print_grammar(self):
        print("\n")
        print("Now grammar is:")
        self.grammar.print()
        print("\n")

    def update_max_len_lines(self, max_len, lines):
        max_len_lines = [x for x in lines if len(x) == max_len]
        for currentLine in max_len_lines:
            self.print_used_line(currentLine)
            grammar_level = self.grammar
            for letter in currentLine[:-LEN_RULES]:
                grammar_level = self.update_grammar_level(grammar_level, letter)
            self.update_grammar_level(grammar_level, currentLine[-LEN_RULES:])
            self.print_grammar()
        return len(max_len_lines)

    def update_other_lines(self, used_lines_count, lines):
        other_lines = lines[used_lines_count:]
        for currentLine in other_lines:
            self.print_used_line(currentLine)
            grammar_level = self.grammar
            for letter in currentLine:
                grammar_level = self.update_grammar_level(grammar_level, letter)
            self.print_grammar()

    def first_step(self):
        print('First step')
        self.sort_sequences()
        print('Using sequences %s' % self.sequences)
        print("\n")
        max_len = len(self.sequences[0])
        used_lines_count = self.update_max_len_lines(max_len, self.sequences)
        self.update_other_lines(used_lines_count, self.sequences)
        print('-' * 80)

    def find_rules(self, rules, grammar):
        for node in grammar.nodes:
            if node.is_rules():
                rules.append(node)
            self.find_rules(rules, node)

    @staticmethod
    def change_recursion(rule, node):
        rule.update_parent_recursion(node)

    def update_recursion(self, rules, grammar):
        for node in grammar.nodes:
            if len(rules) == 0:
                break

            removed_rules = []
            for rule in rules:
                if node.get_recursion_object(rule) is not None:
                    print('Found recursion "{0}" at "{1}"'.format(node, rule))
                    removed_rules.append(rule)

            if len(removed_rules) > 0:
                for rule in removed_rules:
                    self.change_recursion(rule, node)
                    rules.remove(rule)

            self.update_recursion(rules, grammar)

    def second_step(self):
        print('Second step')
        rules = []
        for node in self.grammar.nodes:
            self.find_rules(rules, node)
        print('Rules {0}'.format(rules))
        for node in self.grammar.nodes:
            self.update_recursion(rules, node)
        self.print_grammar()
        print('-' * 80)

    @staticmethod
    def inject_grammar_block(left, right):
        if right.parent == left:
            left.merge_grammar(right)
        else:
            right.merge_grammar(left)

    def find_single_equal_grammar(self):
        result = Grammar.find_equal_grammar(self.grammar, self.grammar)
        find_result = result
        if find_result:
            print('*')
            for grammar_block in result:
                print('Node block')
                for node in grammar_block.nodes:
                    print(node)
                print('*')

            self.inject_grammar_block(result[0], result[1])
            self.print_grammar()

        return find_result

    def third_step(self):
        print('Third step')
        while self.find_single_equal_grammar():
            pass
        print('_' * 80)

    def print_result(self):
        print("\n")
        print("Result set")
        self.print_grammar()

    def print_example(self):
        print('Grammatic Example')
        count = 21
        max_depth = 50
        for i in range(count):
            grammar_line = ''
            grammar_pos = self.grammar
            for j in range(random.randint(1, max_depth)):
                count_nodes = len(grammar_pos.nodes)
                if count_nodes == 0:
                    break
                grammar_pos = grammar_pos.nodes[random.randint(0, count_nodes - 1)]
                grammar_line += grammar_pos.letter
            print(grammar_line)
