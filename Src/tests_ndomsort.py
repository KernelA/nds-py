import unittest
import random

import ndomsort as nds
import stools as st

class TestNdomsort(unittest.TestCase):
    def setUp(self):
        random.seed(2)
        self.max_fronts = 20
    def test_non_domin_sort_many_fronts(self):
        seq = [(i,) * 4 for i in range(self.max_fronts)]

        res = nds.non_domin_sort(seq)

        self.assertEqual(len(res), self.max_fronts)
        self.assertSetEqual(set(range(self.max_fronts)), set(res.keys()))

        for front in res:
            for res_seq in res[front]:
                self.assertTupleEqual(res_seq, seq[front])

    def test_non_domin_sort_one_elem(self):
        seq = [(2,3,4)]

        res = nds.non_domin_sort(seq)

        self.assertEqual(len(res), 1)

        self.assertSetEqual(set(range(1)), set(res.keys()))

        self.assertTupleEqual(seq[0], res[0][0])

    def test_non_domin_sort_one_front(self):

        seq = ((1,1), (1,1), (1,1))

        res = nds.non_domin_sort(seq)

        self.assertEqual(len(res), 1)

        self.assertSetEqual(set(range(1)), set(res.keys()))

        for res_seq in res[0]:
            self.assertTupleEqual(res_seq, seq[0])

    def test_non_domin_sort_two_front(self):
        seq = ((1,0,1), (0,1,1), (-2, -3, 0))

        res = nds.non_domin_sort(seq)

        self.assertEqual(len(res), 2)

        self.assertSetEqual(set(range(2)), set(res.keys()))

        for res_seq in res[1]:
            self.assertIn(res_seq, seq[:2])

    def test_non_domin_sort_random_elem(self):

        for dim in range(2, 6): 
            numbers = [i for i in range(-1, 2)]
            total_seq = len(numbers) ** dim
            seq = [[numbers[0]] * dim for i in range(total_seq)]

            # Generate an all possible combinations numbers from the range 'numbers'.
            # For example, if 'numbers' is  [-1,0,1], than combinations are:
            # {-1, -1, -1}
            # {-1, -1, 0}
            # {-1, -1, 1}
            # {-1, 0, -1}
            # ...
            # {1, 1, 0}
            # {1, 1, 1}
            for index in range(len(seq[0])):
                for count in range(len(numbers) ** (index + 1)):
                    num = numbers[count % len(numbers)]
                    max_repeat = len(numbers) ** (dim - index - 1)
                    for repeat in range(max_repeat):
                        seq[max_repeat * count + repeat][index] = num

            random.shuffle(seq)

            fronts = nds.non_domin_sort(seq)
    
            self.assertSetEqual(set(fronts.keys()), set(range(len(fronts))))
    
            for front_index in range(len(fronts) - 1):
                for seq_curr_front in fronts[front_index]:
                    for seq_curr_front2 in fronts[front_index]:
                        if seq_curr_front != seq_curr_front2:
                            self.assertFalse(st.is_dominate(seq_curr_front2, seq_curr_front) or st.is_dominate(seq_curr_front, seq_curr_front2))
                    for seq_next_front in fronts[front_index + 1]:
                        self.assertFalse(st.is_dominate(seq_next_front, seq_curr_front))
                    


if __name__ == "__main__":
    unittest.main()