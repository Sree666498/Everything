#!/usr/bin/env python3
"""Final test of the working algorithm"""

import re
import collections
from collections import Counter, defaultdict

# Simulate the basic algorithm logic
def test_algorithm():
    print("Testing basic Hangman algorithm logic...")
    
    # Sample dictionary
    sample_dict = ["hello", "world", "python", "programming", "algorithm", "computer"]
    
    # Build frequency data like the real algorithm
    full_dict_common_letters = collections.Counter("".join(sample_dict)).most_common()
    print(f"Dictionary letter frequency: {full_dict_common_letters[:10]}")
    
    # Simulate a game on "hello"
    target = "hello"
    current_dict = sample_dict
    guessed = []
    
    # First guess
    word_pattern = "_ _ _ _ _"
    clean_word = word_pattern[::2].replace("_", ".")
    
    # Filter dictionary
    new_dict = []
    for word in current_dict:
        if len(word) == len(clean_word) and re.match(clean_word, word):
            new_dict.append(word)
    
    print(f"Pattern: {word_pattern}")
    print(f"Matching words: {new_dict}")
    
    # Count letters
    full_dict_string = "".join(new_dict)
    c = collections.Counter(full_dict_string)
    sorted_letter_count = c.most_common()
    
    print(f"Letter frequencies in candidates: {sorted_letter_count}")
    
    # First guess
    for letter, count in sorted_letter_count:
        if letter not in guessed:
            first_guess = letter
            break
    
    print(f"First guess: {first_guess}")
    
    # Check if it would be in "hello"
    if first_guess in target:
        print("✅ First guess would be CORRECT!")
    else:
        print("❌ First guess would be wrong")

def main():
    print("FINAL ALGORITHM TEST")
    print("=" * 30)
    test_algorithm()

if __name__ == "__main__":
    main()
