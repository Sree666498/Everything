#!/usr/bin/env python3
"""Debug the algorithm step by step"""

import re
from collections import Counter, defaultdict

def test_pattern_matching():
    """Test if pattern matching works correctly"""
    
    # Test with a simple case
    word_pattern = "_ e _ _ _"
    clean_pattern = word_pattern[::2].replace("_", ".")
    print(f"Original: '{word_pattern}'")
    print(f"Cleaned: '{clean_pattern}'")
    
    # Test words
    test_words = ["hello", "penny", "bread", "beach", "heart"]
    
    print(f"\nTesting pattern '{clean_pattern}' against words:")
    for word in test_words:
        if len(word) == len(clean_pattern):
            match = re.match(clean_pattern, word)
            print(f"  {word}: {'MATCH' if match else 'NO MATCH'}")
        else:
            print(f"  {word}: WRONG LENGTH")

def test_basic_algorithm():
    """Test the basic frequency counting"""
    
    test_dictionary = ["hello", "world", "python", "coding", "test"]
    guessed_letters = ['e']
    
    print(f"\nTesting frequency analysis:")
    print(f"Dictionary: {test_dictionary}")
    print(f"Guessed: {guessed_letters}")
    
    # Count letters
    letter_count = Counter()
    for word in test_dictionary:
        for letter in word:
            if letter not in guessed_letters:
                letter_count[letter] += 1
    
    print(f"Letter frequencies: {letter_count.most_common()}")
    if letter_count:
        print(f"Next guess should be: {letter_count.most_common(1)[0][0]}")

def main():
    print("DEBUGGING HANGMAN ALGORITHM")
    print("=" * 40)
    
    test_pattern_matching()
    test_basic_algorithm()

if __name__ == "__main__":
    main()
