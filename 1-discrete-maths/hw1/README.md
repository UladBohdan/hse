## The problem

Given boolean formulas `A` and `B`: each may contain conjunction (`&`),
disjunction (`∨`), implication (`=>`), equality (`~`) symbols,
`0`, `1` and variables (such as `p`, `q`, etc)

The problem is: to generate a boolean formula `C` such that: `A => C` and `C => B` are both **tautologies**. `C` contains the same variables as `A` and `B`.

## The algorithm

`A => C` and `C => B` must be true for any instantiation of the variables. This means we can iterate through all possible instantiations, calculate values of `A` and `B` and get the restrictions on `C`.
The following cases are possible:

`B` \ `A` | 0 | 1
--- | --- | ---
0 | `C` must be equal `0` | `C` does not exist
1 | no restrictions on `C` | `C` must be equal `1`

The algorithm then is as following:
* to iterate through all the instantiations of the variables,
* if at some point we realize `C` does not exist - to report about that,
* the answer is of the following format:
`!(A_1|A_2|...|A_n)|B_1|B_2|...|B_n`,
where each `A_i` is a disjunction of all literals with negations
put in a way that `A_i` is only equal to `1` when `A=0` and `B=0`.
Same for `B_i` but with `A=1` and `B=1`.

## Running the code
```
bash setup.sh
bash run.sh
```
