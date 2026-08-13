# Password Strength Analyser

A Python command-line tool that evaluates password strength based on length, character variety, common password matching, repeated/sequential character detection, and Shannon entropy.

## Features

- **Length scoring** — rewards longer passwords (8, 12, and 16+ character thresholds)
- **Character variety checks** — lowercase, uppercase, digits, and symbols
- **Common password detection** — flags passwords found in a known weak-password list
- **Pattern detection** — penalises repeated characters (e.g. `aaa`) and sequential runs (e.g. `abc`, `123`)
- **Entropy estimation** — calculates bits of entropy based on character set size and password length
- **Actionable feedback** — returns a list of suggestions for improving the password

## Requirements

- Python 3.7+
- No external dependencies (uses only the standard library: `re`, `math`, `string`)

## Installation

Clone the repository and run the script directly — no extra setup required.

```bash
git clone <your-repo-url>
cd <your-repo-folder>
python password_analyser.py
```

## Usage

Run the script and enter a password when prompted:

```bash
python password_analyser.py
```

```
----- Password Strength Analyser -----
enter a password: Tr0ub4dor&3

Strength: strong
Score: 75/100
Entropy: 65.14

Feedback:
- excellent password
```

### Using it in your own code

```python
from password_analyser import PasswordStrengthAnalyser

analyser = PasswordStrengthAnalyser("MyP@ssw0rd123")
result = analyser.analyse()

print(result["strength"])   # e.g. "strong"
print(result["score"])      # e.g. 75
print(result["entropy"])    # e.g. 61.35
print(result["feedback"])   # list of suggestions
```

## How Scoring Works

The score starts at 0 and is adjusted as follows, then capped between 0 and 100:

| Check | Effect |
|---|---|
| Length ≥ 16 | +40 |
| Length 12–15 | +30 |
| Length 8–11 | +20 |
| Length < 8 | Feedback only, no points |
| Each character type present (lower/upper/digit/symbol) | +15 each |
| Password is in the common password list | Score reset to 0 |
| Contains 3+ repeated characters (e.g. `aaa`) | -15 |
| Contains a 3-character sequential run (e.g. `abc`, `789`) | -10 per match |

### Strength Bands

| Score | Strength |
|---|---|
| 80–100 | Very Strong |
| 60–79 | Strong |
| 40–59 | Average |
| 20–39 | Weak |
| 0–19 | Very Weak |

## Entropy Calculation

Entropy is estimated using the formula:

```
entropy = password_length × log2(charset_size)
```

Where `charset_size` is the sum of the character set sizes actually used in the password:

- Lowercase letters: 26
- Uppercase letters: 26
- Digits: 10
- Symbols: 32 (via `string.punctuation`)

Higher entropy generally indicates a password that is harder to brute-force.

## Security Notes

- The analysed password is **never printed in plaintext** — output masks it with asterisks.
- This tool provides a heuristic estimate of strength; it is not a substitute for a proper password manager or a real-world breach database check (e.g. [Have I Been Pwned](https://haveibeenpwned.com/)).
- The common password list included here is a small sample for demonstration purposes and should be expanded (or replaced with a larger dataset) for production use.

## Possible Improvements

- Load a larger common-password/breach dataset from a file
- Add a check against dictionary words
- Support batch analysis of multiple passwords from a file
- Add unit tests

## License

MIT License — feel free to use and modify.
