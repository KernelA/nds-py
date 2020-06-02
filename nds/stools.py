"""The module contains additional functions for 'ndomsort'.

"""

__all__ = ["is_dominate"]

from typing import Sequence, Iterable, Optional, Any


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
