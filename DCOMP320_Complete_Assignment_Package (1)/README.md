# DCOMP320 Stack-Based Expression Evaluator

## Files
- `main.py`: Python program and stack-based expression evaluator.
- `input.txt`: sample expressions.
- `output.txt`: generated results.
- `DCOMP320_Report.docx`: report following the assignment's required sections.
- `TEST_RESULTS.txt`: short test summary.

## Run the program
1. Keep `main.py` and `input.txt` in the same folder.
2. Open the folder in VS Code and open Terminal → New Terminal.
3. Run `python main.py` (or `py main.py` on Windows).
4. Results are printed and written to `output.txt`.

## Input format
Put one expression per line. Use `+`, `-`, `*`, `/`, and parentheses. Separator lines made from at least three `-`, `=`, `*`, or `_` characters are retained in output. Decimal values and unary signs such as `-5` are supported.

## Sample
Input:
```
3 + 5 * 2
-----
(8 / 4) + 7 * 2
-----
10 - (2 + 3) * 4
```
Output:
```
13
-----
16
-----
-10
```

## Assumptions and limitations
The program supports basic arithmetic, parentheses, decimals, and unary signs. It does not support exponentiation, variables, or mathematical functions. Invalid expressions and division by zero produce an error line. The assignment sheet's printed example appears inconsistent: `(8 / 4) + 7 * 2` evaluates to 16 using standard precedence, not 17.

## GitHub
Create a repository, add the source, input/output, README and report files, commit and push them, then invite your lecturer as a collaborator via repository Settings → Collaborators.
