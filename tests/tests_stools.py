import unittest
import random

import nds.stools as st


class TestStools(unittest.TestCase):

    def setUp(self):
        random.seed(2)
        self.dom_pairs_seq = (
            ((0, 0), (1, 1)),
            ((1, 0), (1, 1)),
            ((1, 1), (1, 1)),
            ((2, 1), (1, 1)),
            ((2, 2), (1, 1)),
            ((0, 1, 0), (1, 0, 0)),
            ((0, 0, 1), (0, 0, 1))
        )

        self.dom_answers = (True, True, False, False, False, False, False)

        self.max_size = 30

    def test_is_dominate(self):
        for ((left, right), answer) in zip(self.dom_pairs_seq, self.dom_answers):
            self.assertEqual(st.is_dominate(left, right), answer)


if __name__ == "__main__":
    unitest.main()
