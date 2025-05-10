"""Regex"""

from __future__ import annotations
from abc import ABC, abstractmethod


class State(ABC):
    """State"""
    def __init__(self) -> None:
        self.related_key_state = {}
        self.e_transitions = []

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """check self"""
        return False

    def add_related_key_state(self, symbol, state):
        """Add a symbol-based transition from the current state to another state"""
        self.related_key_state.setdefault(symbol, []).append(state)

    def add_e_transitions(self, state):
        """add an e-transition from the current state to another state"""
        self.e_transitions.append(state)


class StartState(State):
    """StartState"""
    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return super().check_self(char)


class TerminationState(State):
    """TerminationState"""
    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return super().check_self(char)

class DotState(State):
    """DotState"""
    def __init__(self):
        super().__init__()

    def check_self(self, char: str):
        return True


class AsciiState(State):
    """AsciiState"""
    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.curr_sym = symbol

    def check_self(self, curr_char: str) -> bool:
        return self.curr_sym == curr_char


class StarState(State):
    """StarState"""
    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return super().check_self(char)


class PlusState(State):
    """PlusState"""
    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return super().check_self(char)


class TempState(State):
    """Empty state placeholder for constructing NFA"""
    def __init__(self):
        super().__init__()

    def check_self(self, char: str) -> bool:
        return super().check_self(char)


class RegexFSM:
    """RegexFSM"""
    def __init__(self, messege: str) -> None:
        self.start_state = StartState()
        self.termination_state = TerminationState()

        curr_start, curr_end = None, None
        i = 0
        while i < len(messege):
            el = messege[i]
            if el == "." or el.isascii():
                fragment_start, fragment_end = self.make_start_end(el)
                if i + 1 < len(messege) and messege[i+1] in ("*","+"):
                    i += 1
                    if messege[i] == "*":
                        temp_start, temp_end = StarState(), StarState()
                        temp_start.add_e_transitions(fragment_start)
                        temp_start.add_e_transitions(temp_end)
                        fragment_end.add_e_transitions(fragment_start)
                        fragment_end.add_e_transitions(temp_end)
                        fragment_start, fragment_end = temp_start, temp_end
                    else:
                        temp_start, temp_end = PlusState(), PlusState()
                        temp_start.add_e_transitions(fragment_start)
                        fragment_end.add_e_transitions(fragment_start)
                        fragment_end.add_e_transitions(temp_end)
                        fragment_start, fragment_end = temp_start, temp_end

                if curr_end is None:
                    curr_start, curr_end = fragment_start, fragment_end
                else:
                    curr_end.add_e_transitions(fragment_start)
                    curr_end = fragment_end
            else:
                raise AttributeError("Character is not supported'")
            i += 1

        if curr_end is None:
            self.start_state.add_e_transitions(self.termination_state)
        else:
            self.start_state.add_e_transitions(curr_start)
            curr_end.add_e_transitions(self.termination_state)

    @staticmethod
    def make_start_end(key: str):
        """creates a fragment of a single-character automaton"""
        start_ = TempState()
        end_ = TempState()
        start_.add_related_key_state(key, end_)
        return start_, end_

    def e_transitions_closure(self, states):
        """All attainable states from the set states via ε-transitions"""
        stack_ = list(states)
        res = set(states)
        while stack_:
            state = stack_.pop()
            for way_e in state.e_transitions:
                if way_e not in res:
                    res.add(way_e)
                    stack_.append(way_e)
        return res

    def check_string(self, messege: str) -> bool:
        """check messege"""
        current_set_of_states  = self.e_transitions_closure({self.start_state})
        for el in messege:
            next_ = set()
            for state in current_set_of_states:
                for key, list_state in state.related_key_state.items():
                    if key in ('.', el):
                        next_.update(list_state)
            current_set_of_states = self.e_transitions_closure(next_)
            if not current_set_of_states:
                return False
        return self.termination_state in current_set_of_states


if __name__ == "__main__":
    regex_pattern = "a*4.+hi"

    regex_compiled = RegexFSM(regex_pattern)

    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))  # True
    print(regex_compiled.check_string("meow"))  # False
