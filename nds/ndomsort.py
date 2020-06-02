"""Module is implementation of non-dominated sorting.

Original algorithm described in the paper:

Buzdalov M., Shalyto A.
A Provably Asymptotically Fast Version of the Generalized Jensen Algorithm for Non-dominated Sorting
// Parallel Problem Solving from Nature XIII.
- 2015. - P. 528-537. - (Lecture Notes on Computer Science ; 8672)

"""

__all__ = ["non_domin_sort"]

from typing import List, Iterable, Tuple, Callable, Dict, Any, Union
from collections import defaultdict
import statistics

from . import stools as st


def _is_seq_has_one_uniq_value(iterable: Iterable[Any]) -> bool:
    """Check. Has 'iterable' only a one unique value?

    It is equivalent following: 'len({item for item in iterable}) == 1'.

    --------------------
    Args:
        'iterable': An input sequence.

    --------------------
    Returns:
        True, if 'iterable' contains only a one unique value, otherwise False.

    --------------------
    Raises:
        ValueError: If 'iterable' is empty.

    """

    iterator = iter(iterable)

    try:
        first_value = next(iterator)
        is_has_uniq_value = True
    except StopIteration:
        raise ValueError("'iterable' is empty.")

    try:
        while True:
            value = next(iterator)
            if value != first_value:
                is_has_uniq_value = False
                break
    except StopIteration:
        pass

    return is_has_uniq_value


def _merge(indices1: List[int], indices2: List[int]) -> List[int]:
    """Merge the two list of the indices. Each list must be sorted.

    --------------------
    Args:
        'indices1': A sorted list of the indices.
        'indices2': A sorted list of the indices.

    --------------------
    Returns:
        The ordered list of indices.

    """
    merged_list = indices1 + indices2

    index1 = 0
    index2 = 0

    merge_index = 0

    while index1 < len(indices1) and index2 < len(indices2):
        if indices1[index1] < indices2[index2]:
            merged_list[merge_index] = indices1[index1]
            index1 += 1
        else:
            merged_list[merge_index] = indices2[index2]
            index2 += 1
        merge_index += 1

    for i in range(index1, len(indices1)):
        merged_list[merge_index] = indices1[i]
        merge_index += 1

    for i in range(index2, len(indices2)):
        merged_list[merge_index] = indices2[i]
        merge_index += 1

    return merged_list


def _split_by(seq_objs_front: List[Dict[str, Union[int, Any]]], indices: List[int], split_value: Any, index_value: int) \
        -> Tuple[List[int], List[int], List[int]]:
    """'indices' splits into three lists.

    The three lits are the list of indices, where 'index_value'th value of the objectives is less than a 'split_value',
    the list of indices, where 'index_value'th value of the objectives is equal to a 'split_value',
    the list of indices, where 'index_value'th value of the objectives is greater than a 'split_value'.

    --------------------
    Args:
         'seq_objs_front': A dictionary contains the values of the objectives and indices of the fronts.
         'indices': The indices of the objectives in the 'seq_objs_front'.
         'split_value': A value for the splitting.
         'index_value': The index of the value in the objectives, for the split.

    --------------------
    Returns:
         The tuple of lists of the indices.

    """
    indices_less_split_value = []
    indices_greater_split_value = []
    indices_equal_split_value = []

    for index in indices:
        if seq_objs_front[index]["objs"][index_value] < split_value:
            indices_less_split_value.append(index)
        elif seq_objs_front[index]["objs"][index_value] > split_value:
            indices_greater_split_value.append(index)
        else:
            indices_equal_split_value.append(index)

    return indices_less_split_value, indices_equal_split_value, indices_greater_split_value


def _sweep_a(seq_objs_front: List[Dict[str, Union[Any, str]]], indices: List[int]) -> None:
    """Two-objective sorting.

    It attributes front's index to the lexicographically ordered elements in the  'seq_objs_front',
    with the indices in the 'indices', based on the first two values of the objectives using a line-sweep algorithm.

    --------------------
    Args:
        'seq_objs_front': A dictionary contains the values of the objectives and indices of the fronts.
        'indices': The indices of the objectives in the 'seq_objs_front'.

    --------------------
    Returns:
        None

    """
    init_ind = set((indices[0],))

    for k in range(1, len(indices)):
        i = indices[k]
        indices_where_sec_values_less_or_eq = [index for index in init_ind
                                               if seq_objs_front[index]["objs"][1] <= seq_objs_front[i]["objs"][1]]
        if indices_where_sec_values_less_or_eq:
            max_front = max(seq_objs_front[index]["front"]
                            for index in indices_where_sec_values_less_or_eq)
            seq_objs_front[i]["front"] = max(seq_objs_front[i]["front"], max_front + 1)

        init_ind -= {index for index in init_ind if seq_objs_front[index]
                     ["front"] == seq_objs_front[i]["front"]}
        init_ind.add(i)


def _sweep_b(seq_objs_front: List[Dict[str, Union[Any, int]]], comp_indices: List[int], assign_indices: List[int]) -> None:
    """Two-objective sorting procedure.

    It attributes front's indices to elements in the 'seq_objs_front', with the indices in the 'assign_indices',
    based on the first two values of the objectives by comparing them to fitnesses,
    with the indices in the  'comp_indices', using a line-sweep algorithm.

    --------------------
    Args:
        'seq_objs_front': A dictionary contains the values of the objectives and indices of the fronts.
        'comp_indices': The indices for comparing.
        'assign_indices': The indices for assign front.

    --------------------
    Returns:
        None

    """

    init_ind = set()
    p = 0

    for j in assign_indices:
        if p < len(comp_indices):
            fitness_right = seq_objs_front[j]["objs"][:2]

        while p < len(comp_indices):
            i = comp_indices[p]
            fitness_left = seq_objs_front[i]["objs"][:2]
            if fitness_left <= fitness_right:
                indices_less_value_eq_front = [index for index in init_ind
                                               if seq_objs_front[index]["front"] == seq_objs_front[i]["front"]
                                               and seq_objs_front[index]["objs"][1] < seq_objs_front[i]["objs"][1]]

                if not indices_less_value_eq_front:
                    init_ind -= {index for index in init_ind
                                 if seq_objs_front[index]["front"] == seq_objs_front[i]["front"]}
                    init_ind.add(i)
                p += 1
            else:
                break
        indices_less_or_eq_value = [index for index in init_ind
                                    if seq_objs_front[index]["objs"][1] <= seq_objs_front[j]["objs"][1]]

        if indices_less_or_eq_value:
            max_front = max(seq_objs_front[index]["front"] for index in indices_less_or_eq_value)
            seq_objs_front[j]["front"] = max(seq_objs_front[j]["front"], max_front + 1)


def _nd_helper_a(seq_objs_front: List[Dict[str, Union[Any, int]]], indices: List[int], count_of_obj: int) -> None:
    """Recursive procedure.

    It attributes front's indices to all elements in the 'seq_objs_front', with the indices in the 'indices',
    for the first 'count_of_obj' values of the objectives.

    --------------------
    Args:
         'seq_objs_front': A dictionary contains the values of the objectives and indices of the fronts.
         'indices': The indices for assign front.
         'count_of_obj': The number of the values from the objectives, for the sorting.

    --------------------
    Returns:
         None

    """

    if len(indices) < 2:
        return
    elif len(indices) == 2:
        index_l, index_r = indices[0], indices[1]
        fitness1, fitness2 = seq_objs_front[index_l]["objs"][:
                                                             count_of_obj], seq_objs_front[index_r]["objs"][:count_of_obj]

        if st.is_dominate(fitness1, fitness2):
            seq_objs_front[index_r]["front"] = max(
                seq_objs_front[index_r]["front"], seq_objs_front[index_l]["front"] + 1)
    elif count_of_obj == 2:
        _sweep_a(seq_objs_front, indices)
    elif _is_seq_has_one_uniq_value(seq_objs_front[index]["objs"][count_of_obj - 1] for index in indices):
        _nd_helper_a(seq_objs_front, indices, count_of_obj - 1)
    else:
        median = statistics.median_low(
            seq_objs_front[index]["objs"][count_of_obj - 1] for index in indices)

        less_median, equal_median, greater_median = _split_by(
            seq_objs_front, indices, median, count_of_obj - 1)

        less_and_equal_median = _merge(equal_median, less_median)

        _nd_helper_a(seq_objs_front, less_median, count_of_obj)
        _nd_helper_b(seq_objs_front, less_median, equal_median, count_of_obj - 1)
        _nd_helper_a(seq_objs_front, equal_median, count_of_obj - 1)
        _nd_helper_b(seq_objs_front, less_and_equal_median, greater_median, count_of_obj - 1)
        _nd_helper_a(seq_objs_front, greater_median, count_of_obj)


def _nd_helper_b(seq_objs_front: List[Dict[str, Union[Any, int]]], comp_indices: List[int], assign_indices: List[int], count_of_obj: int) -> None:
    """Recursive procedure.

    It attributes a front's indices to all elements in the 'seq_objs_front', with the indices in the  'assign_indices',
    for the first 'count_of_obj' values of the objectives, by comparing them to elements in the 'seq_objs_front',
    with the indices in the 'comp_indices'.

    --------------------
    Args:
         'seq_objs_front': A dictionary contains the values of the objectives and indices of the fronts.
         'comp_indices': The indices for comparing.
         'assign_indices': The indices for assign front.
         'count_of_obj': The number of the values from the objectives, for the sorting.

    --------------------
    Returns:
         None

    """

    if not comp_indices or not assign_indices:
        return
    elif len(comp_indices) == 1 or len(assign_indices) == 1:
        for i in assign_indices:
            hv = seq_objs_front[i]["objs"][:count_of_obj]
            for j in comp_indices:
                lv = seq_objs_front[j]["objs"][:count_of_obj]
                if st.is_dominate(lv, hv) or lv == hv:
                    seq_objs_front[i]["front"] = max(
                        seq_objs_front[i]["front"], seq_objs_front[j]["front"] + 1)
    elif count_of_obj == 2:
        _sweep_b(seq_objs_front, comp_indices, assign_indices)
    else:
        values_objs_from_comp_indices = {
            seq_objs_front[i]["objs"][count_of_obj - 1] for i in comp_indices}
        values_objs_from_assign_indices = {
            seq_objs_front[j]["objs"][count_of_obj - 1] for j in assign_indices}

        min_from_comp_indices, max_from_comp_indices = \
            min(values_objs_from_comp_indices), max(values_objs_from_comp_indices)

        min_from_assign_indices, max_from_assign_indices = \
            min(values_objs_from_assign_indices), max(values_objs_from_assign_indices)

        if max_from_comp_indices <= min_from_assign_indices:
            _nd_helper_b(seq_objs_front, comp_indices, assign_indices, count_of_obj - 1)
        elif min_from_comp_indices <= max_from_assign_indices:
            median = statistics.median_low(values_objs_from_comp_indices |
                                           values_objs_from_assign_indices)

            less_median_indices_1, equal_median_indices_1, greater_median_indices_1 = \
                _split_by(seq_objs_front, comp_indices, median, count_of_obj - 1)
            less_median_indices_2, equal_median_indices_2, greater_median_indices_2 = \
                _split_by(seq_objs_front, assign_indices, median, count_of_obj - 1)

            less_end_equal_median_indices_1 = _merge(less_median_indices_1, equal_median_indices_1)

            _nd_helper_b(seq_objs_front, less_median_indices_1, less_median_indices_2, count_of_obj)
            _nd_helper_b(seq_objs_front, less_median_indices_1,
                         equal_median_indices_2, count_of_obj - 1)
            _nd_helper_b(seq_objs_front, equal_median_indices_1,
                         equal_median_indices_2, count_of_obj - 1)
            _nd_helper_b(seq_objs_front, less_end_equal_median_indices_1,
                         greater_median_indices_2, count_of_obj - 1)
            _nd_helper_b(seq_objs_front, greater_median_indices_1,
                         greater_median_indices_2, count_of_obj)


def non_domin_sort(decisions: Iterable[Any], get_objectives: Callable[[Any], Iterable[Any]] = None,
                   only_front_indices: bool = False) -> Union[Tuple[int], Dict[int, Tuple[Any]]]:
    """A non-dominated sorting.

    If 'get_objectives' is 'None', then it is identity map: 'get_objectives = lambda x: x'.

    --------------------
    Args:
        'decisions': The sequence of the decisions for non-dominated sorting.
        'get_objectives': The function which maps a decision space into a objectives space.
        'only_front_indices':

    --------------------
    Returns:
        If 'only_front_indices' is False:
            A dictionary. It contains indices of fronts as keys and values are tuple consist of
            'decisions' which have a same index of the front.
        Otherwise:
            Tuple of front's indices for the every decision in 'decisions'.
    """

    # The dictionary contains the objectives as keys and indices of the their preimages in the 'decisions' as values.
    objs_dict = defaultdict(list)

    if get_objectives is None:
        objs_gen = map(lambda x: (x, tuple(x)), decisions)
    else:
        objs_gen = map(lambda x: (x, tuple(get_objectives(x))), decisions)

    for (index, (decision, fitness)) in enumerate(objs_gen):
        objs_dict[fitness].append((index, decision))

    total_unique_objs = 0

    for objs in objs_dict:
        if total_unique_objs == 0:
            first_obj = objs
            count_of_obj = len(objs)
            assert count_of_obj > 1, "The number of the objectives must be > 1, " \
                "but image of the decision have the length is {0}." \
                                     "\nThe indices of the decisions: {1}.".format(count_of_obj,
                                                                                   [index for (index, dec)
                                                                                    in objs_dict[objs]])
        else:
            assert count_of_obj == len(objs), "The images of the decisions at positions {0} " \
                                              "have the number of the objectives " \
                                              "is not equal the number of the objectives of the images at positions " \
                                              "{1}.".format([index for (index, dec) in objs_dict[first_obj]],
                                                            [index for (index, dec) in objs_dict[objs]])
        total_unique_objs += 1

    assert total_unique_objs != 0, "The sequence of the decisions or values of the objectives is empty."

    # The list 'unique_objs' never changes, but its elements yes.
    # It sorted in the lexicographical order.
    unique_objs_and_fronts = [{"objs": fitness, "front": 0} for fitness in sorted(objs_dict.keys())]

    # Further, algorithm works only with the indices of list 'unique_objs'.
    indices_uniq_objs = list(range(len(unique_objs_and_fronts)))
    _nd_helper_a(unique_objs_and_fronts, indices_uniq_objs, count_of_obj)

    if only_front_indices is True:
        total_decisions = sum(map(len, (objs_dict[objs] for objs in objs_dict)))
        fronts = list(range(total_decisions))
        for objs in unique_objs_and_fronts:
            for (index, dec) in objs_dict[objs["objs"]]:
                fronts[index] = objs["front"]
        fronts = tuple(fronts)
    else:
        # The dictionary contains indices of the fronts as keys and the tuple of 'decisions' as values.
        fronts = defaultdict(tuple)

        # Generate fronts.
        for objs_front in unique_objs_and_fronts:
            fronts[objs_front["front"]
                   ] += tuple(decision for (index, decision) in objs_dict[objs_front["objs"]])

    return fronts
