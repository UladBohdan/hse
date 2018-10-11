## The problem

Given boolean formulas `A` and `B`: each may contain conjunction (`&`),
disjunction (`∨`), implication (`=>`), equality (`~`) symbols,
`0`, `1` and variables (such as `p`, `q`, etc.)

The problem is: to generate a boolean formula `C` such that `A => C` and `C => B` are both **tautologies**.
`C` may only contain the variables which are both in `A` and `B`.

## To run the code
```
bash setup.sh
bash run.sh
```

## The algorithm

* to distinguish the variables into three groups: those common for `A` and `B`,
those unique for `A` and those unique for `B`.

* to make sure both `A` and `B` only depend on variables common for both formulas -
otherwise `C` does not exist.

* for every instantiation of common variables calculate `A` and `B` and keep the following table in mind:

`B` \ `A` | 0 | 1
--- | --- | ---
0 | `C` must be equal `0` | `C` does not exist
1 | no restrictions on `C` | `C` must be equal `1`

* to produce an answer of the following format:
`!(A_1|A_2|...|A_n)|B_1|B_2|...|B_n`,
where each `A_i` is a disjunction of all literals (of common variables) with negations
put in a way that `A_i` is only equal to `1` when `A=0` and `B=0`.
Same for `B_i` but with `A=1` and `B=1`.
