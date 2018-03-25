"""The module contains additional functions for 'ndomsort'.

"""

__all__ = ["is_dominate", "find_low_median"]

from typing import Sequence, Iterable, Optional, Any
import random


def is_dominate(leftv: Sequence[Any], rightv: Sequence[Any]) -> bool:
    """Check. Does a 'leftv' dominate a 'rightv'?

    A 'leftv' dominates a 'rightv', if and only if leftv[i] <= rightv[i], for all i in {0,1,..., len(leftv) - 1},
    and there exists j in {0,1,...,len(leftv) - 1}: leftv[j] < rightv[j].

    --------------------
    Args:
        'leftv': A first vector of the values.
        'rightv': A second vector of the values.

    --------------------
    Returns:
        True if 'leftv' dominates a 'rightv', otherwise False.

    """

    assert len(leftv) == len(rightv), "'leftv' must have a same length as 'rightv'."

    is_all_values_less_or_eq = True
    is_one_value_less = False

    for i in range(len(leftv)):
        if leftv[i] < rightv[i]:
            is_one_value_less = True
        elif leftv[i] > rightv[i]:
            is_all_values_less_or_eq = False
            break
    return is_all_values_less_or_eq and is_one_value_less


def find_low_median(iterable: Iterable[Any]) -> Optional[Any]:
    """Find median of sequence, if length of sequence is odd,
    otherwise the sequence has two median. The median is the smallest value from them.

    Note:
        Time complexity is O(n), where n is length of the sequence.
    --------------------
    Args:
         'iterable': An input sequence.

    --------------------
    Returns:
       None, if length of the sequence is equal to 0, otherwise "median" of the sequence.

    """

    elements = list(iterable)

    if not elements:
        return None

    median_index = (len(elements) - 1) // 2

    left = 0
    right = len(elements) - 1
    i = -1

    while median_index != i:
        if left != right:
            swap_index = random.randint(left, right - 1)
            elements[swap_index], elements[right] = elements[right], elements[swap_index]
        split_elem = elements[right]
        i = left - 1
        for j in range(left, right + 1):
            if elements[j] <= split_elem:
                i += 1
                elements[i], elements[j] = elements[j], elements[i]
        if i < median_index:
            left = i + 1
        elif i > median_index:
            right = i - 1

    return elements[i]
