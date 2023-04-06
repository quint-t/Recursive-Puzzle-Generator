# Recursive-Puzzle-Generator

The repository contains one Python file — `generator_example.py` — with an example of generating a recursive puzzle.  
Generator is based on [Twelve statements](https://rosettacode.org/wiki/Twelve_statements).  
Requirements: Python 3.11.

## Types of statements by levels

- L1. Exactly X of the previous/next statements is/are true/false.
- L1. Exactly X of the first/last/previous/next Y statements is/are true/false.
- L1. Exactly X of the even/odd statements is/are true/false.
- L1. Exactly X of the previous/next even/odd statements is/are true/false.
- L1. Exactly W of the statements X, Y and Z is/are true/false.
- L2. Either statement X or statement Y is true/false, but not both.
- L2. Either statement X or statement Y is true/false, or both.
- L2. Statements X and Y are either both true or both false.
- L3. At least/most X of the previous/next statements is/are true/false.
- L3. At least/most X of the first/last/previous/next Y statements is/are true/false.
- L3. At least/most X of the even/odd statements is/are true/false.
- L3. At least/most X of the previous/next even/odd statements is/are true/false.
- L4. If statement X is true/false, then statement Y is true/false (sufficient).
- L4. Only if statement X is true/false, then statement Y is true/false (necessary).
- L4. If and only if statement X is true/false, then statement Y is true/false (sufficient and necessary).
- L5. If statement X is true/false, then statements Y and Z are both true/false (sufficient).
- L5. Only if statement X is true/false, then statements Y and Z are both true/false (necessary).
- L5. If and only if statement X is true/false, then statements Y and Z are both true/false (sufficient and necessary).
- L6. Without types of statements from L1.
- L7. Without types of statements from L1, L2.
- L8. Without types of statements from L1, L2, L3.

## Examples

You can see many generated puzzles in the directory `puzzles` (text files `<NumberOfStatements>.txt`).

3 statements, level 8
```
Statements:
1. This is a numbered list of 3 statements.
2. If statement 1 is false, then statement 3 is false (sufficient).
3. If and only if statement 1 is true, then statement 2 is false (sufficient and necessary).
Solutions:
1-True, 2-True, 3-False
```

5 statements, level 3
```
Statements:
1. This is a numbered list of 5 statements.
2. Exactly 2 of the odd statements are true.
3. Statements 4 and 1 are either both true or both false.
4. Either statement 5 or statement 1 is true, but not both.
5. Either statement 2 or statement 3 is true, or both.
Solutions:
1-True, 2-True, 3-False, 4-False, 5-True
```

7 statements, level 1
```
Statements:
1. This is a numbered list of 7 statements.
2. Exactly 4 of the odd statements are true.
3. Exactly 1 of the next odd statements is true.
4. Exactly 1 of the statements 7, 6 and 3 is true.
5. Exactly 3 of the even statements are false.
6. Exactly 1 of the first 2 statements is true.
7. Exactly 4 of the first 5 statements are false.
Solutions:
1-True, 2-False, 3-False, 4-True, 5-False, 6-True, 7-False
```

12 statements, level 5
```
Statements:
 1. This is a numbered list of 12 statements.
 2. At least 3 of the last 8 statements are true.
 3. At least 5 of the last 6 statements are false.
 4. Exactly 1 of the previous statements is true.
 5. Statements 3 and 6 are either both true or both false.
 6. Exactly 3 of the statements 10, 9 and 7 are false.
 7. Statements 3 and 11 are either both true or both false.
 8. If statement 2 is true, then statement 3 is true (sufficient).
 9. Only if statement 8 is true, then statements 12 and 11 are both true (necessary).
10. Either statement 5 or statement 12 is true, or both.
11. At least 6 of the previous 9 statements are true.
12. At most 1 of the odd statements is true.
Solutions:
1-True, 2-True, 3-False, 4-False, 5-True, 6-False, 7-True, 8-False, 9-True, 10-True, 11-False, 12-False
```
