# a program the analyses the strength of password based on:
# - Length
# - character variety
# - common patterns
# - entropy

import re 
import math 
import string

class PasswordStrengthAnalyser:

    Common_Passwords = {
        "password", "123456", "qwerty", "admin", "letmein", "welcome", "abc123"
    }

    def __init__(self, password: str):
        self.password = password
# a function to estimate password entropy
    def calculate_entropy(self) -> float:
        charset_size = 0

        if any(c.islower() for c in self.password):
            charset_size += 26
        if any(c.isupper() for c in self.password):
            charset_size += 26
        if any(c.isdigit() for c in self.password):
            charset_size += 10
        if any(c in string.punctuation for c in self.password):
            charset_size += len(string.punctuation)

        if charset_size == 0:
            return 0

        return round(len(self.password) * math.log2(charset_size), 2) 
# a function to analyse the password strength
    def analyse(self) -> dict:
        score = 0
        feedback = []

        length = len(self.password)
        if length >= 16:
            score += 40
        elif length >= 12:
            score += 30
        elif length >= 8:
            score += 20
        else:
            feedback.append("Password should be at least 8 characters long")
# checks character variety
        checks = {
            "lowercase": bool(re.search(r"[a-z]", self.password)),
            "uppercase": bool(re.search(r"[A-Z]", self.password)),
            "digits": bool(re.search(r"\d", self.password)),
            "symbols": bool(re.search(rf"[{re.escape(string.punctuation)}]", self.password))
        }

        score += sum(checks.values()) * 15

        for category, present in checks.items():
            if not present:
                feedback.append(f"Add {category} characters")
# checks if the password is a common password
        if self.password.lower() in self.Common_Passwords:
            score = 0
            feedback.append("This is a very common password")
# checks for repeated characters in the password
        if re.search(r"(.)\1{2,}", self.password): 
            score -= 15
            feedback.append("Avoid repeated characters")

        sequences = [
            "abcdefghijklmnopqrstuvwxyz",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "0123456789"
        ]
# check for squential charcters
        for sequence in sequences:
            for i in range(len(sequence) - 2):
                if sequence[i: i + 3 ] in self.password:
                    score -= 10
                    feedback.append("Avoid sequential characters")
                    break
        
        score = max (0, min(score, 100))
        entropy = self.calculate_entropy()

        if score >= 80:
            strength = "very strong"
        elif score >= 60:
            strength = "strong" 
        elif score >= 40:
            strength = "average"
        elif score >= 20:
            strength = "weak"
        else:
            strength = "very weak"
        
        return {
            "password": "*" * len(self.password),
            "score": score,
            "strength": strength,
            "entropy" : entropy,
            "feedback": feedback or ["excellent password"]

        }

def main():
    print("----- Password Strength Analyser -----")

    password = input("enter a password: ")
    analyser = PasswordStrengthAnalyser(password)

    result = analyser.analyse()

    print (f"\nStrength: {result['strength']}")
    print (f"Score: {result['score']}/100")
    print(f"Entropy: {result['entropy']}")

    print("\nFeedback:")
    for item in result["feedback"]:
        print(f"- {item}")

if __name__ == "__main__":
    main()
