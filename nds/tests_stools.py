import unittest
import random

import stools as st

class TestStools(unittest.TestCase):

    def setUp(self):
        random.seed(2)
        self.dom_pairs_seq = (
            ((0,0), (1,1)),
            ((1,0), (1,1)),
            ((1,1), (1,1)),
            ((2,1), (1,1)),
            ((2,2), (1,1)),
            ((0,1,0), (1,0,0)),
            ((0,0,1), (0,0,1))
            )

        self.dom_asnwers = (True, True, False, False, False, False, False)

        self.max_size = 30


    def test_is_dominate(self):
            for ((left, right), answer) in zip(self.dom_pairs_seq, self.dom_asnwers):
                self.assertEqual(st.is_dominate(left, right), answer)

    def test_find_median(self):
        for size in range(1, self.max_size + 1):
            seq = [random.uniform(-100,100) for i in range(size)]
            sort_seq = sorted(seq)
            self.assertEqual(st.find_low_median(seq), sort_seq[(size - 1) // 2])


if __name__ == "__main__":
    unitest.main()

