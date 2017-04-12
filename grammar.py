class Grammar:
    def __init__(self, letter=None, parent=None):
        parent = parent if parent is not None else self
        self.level = 0 if parent is None else -1
        self.letter = letter
        self.nodes = []
        self.parent = parent
        self.parent_level = parent.level
        self.is_recursion = False
        self.recursion_repeat = []

    def set_level(self, level):
        self.level = level

    def add_node(self, node):
        self.nodes.append(node)

    def is_equals(self, letter):
        return self.letter == letter

    def get_default_string(self):
        if self.parent_level == -1:
            return 'S->{0}'.format(self.letter)
        else:
            return 'A{0}->{1}'.format(self.parent_level, self.letter)

    def get_printed_string(self):
        default_string = self.get_default_string()
        return '{0}, A{1}'.format(default_string, self.level) if len(self.nodes) > 0 else default_string

    def print(self):
        if self != self.parent:
            print(self.get_printed_string())
        if not self.is_recursion:
            [x.print() for x in self.nodes]

    def __repr__(self):
        return self.get_printed_string()

    def is_rules(self):
        return len(self.letter) > 1 if self.letter is not None else False

    def not_use_in_recursion(self):
        return len(self.letter) > 1 or len(self.nodes) == 0

    def is_last_leaf(self):
        return len(self.letter) == 1 and len(self.nodes) == 0

    def get_recursion_object(self, rule):
        if self.not_use_in_recursion():
            return False

        if self.letter == rule.letter[0]:
            for y in [x for x in self.nodes if x.is_last_leaf()]:
                if y.letter == rule.letter[1]:
                    return True
        return False

    def copy_object(self, new_node):
        self.letter = new_node.letter
        self.level = new_node.parent_level
        self.nodes = new_node.parent.nodes

    def update_parent_recursion(self, new_node):
        self.parent.nodes.remove(self)
        for child in self.parent.nodes:
            for checkNode in new_node.parent.nodes:
                if checkNode.is_equals(child.letter):
                    break
            else:
                new_node.parent.nodes.append(child)
                child.parent = new_node.parent
                child.parent_level = new_node.parent_level

        self.parent.copy_object(new_node)
        self.parent.is_recursion = True
        new_node.recursion_repeat.append(self.parent)

    @staticmethod
    def equal_child(left, right):
        return (left.letter == right.letter) and (
            (left.level == right.level) or (
                (left.level == left.parent_level) and (right.level == right.parent_level)) or (
                (left.level == right.parent_level) and (right.level == left.parent_level)))

    @staticmethod
    def equals_grammar(left, right):
        if len(left.nodes) == 0 or (len(left.nodes) != len(right.nodes)):
            return False

        checked_right = []
        for left_child in left.nodes:
            for right_child in [right_child for right_child in right.nodes if (right_child not in checked_right)]:
                if Grammar.equal_child(left_child, right_child):
                    checked_right.append(right_child)
                    break
        return True if len(checked_right) == len(right.nodes) else False

    @staticmethod
    def find_child_equal(fixed, children):
        for node in children.nodes:
            result = Grammar.find_equal_grammar(fixed, node)
            if result:
                return result
        return False

    @staticmethod
    def find_equal_grammar(left, right):
        if right.is_recursion or left.is_recursion:
            return False
        if (left != right) and (Grammar.equals_grammar(left, right)):
            return [left, right]

        result = Grammar.find_child_equal(left, right)
        if result:
            return result
        if left == right:
            return False
        result = Grammar.find_child_equal(right, left)
        return result

    def merge_grammar(self, merged):
        merged_nodes = merged.recursion_repeat[:]
        merged_nodes.append(merged)

        for copy_node in merged_nodes:
            copy_node.nodes = self.nodes
            copy_node.level = self.level

        merged.is_recursion = True
        merged.recursion_repeat = []
        self.recursion_repeat.extend(merged_nodes)
