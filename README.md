# Non-dominated sorting

## Description of the method

You can read about the method in the next article:

Buzdalov M., Shalyto A. A Provably Asymptotically Fast Version of the Generalized Jensen Algorithm for Non-dominated Sorting  // Parallel Problem Solving from Nature XIII.- 2015. - P. 528-537. - (Lecture Notes on Computer Science; 8672)

## Installation

`python setup.py install`

## How to use

The example:

```python
import random

# Package must be installed.
from nds import ndomsort

seq = [random.sample(range(-10, 11), 5) for i in range(30)]

# It is dictionary.
fronts = ndomsort.non_domin_sort(seq)

# Or we can get values of objectives.
# fronts = ndomsort.non_domin_sort(seq, lambda x: x[:4])

for front in fronts:
    print("\nFront index is {}".format(front))
    for seq in fronts[front]:
        print("\t{}".format(seq))

```

## Other implementations

* [Java](https://github.com/mbuzdalov/non-dominated-sorting)
* [C#](https://github.com/KernelA/nds)
