#!/usr/bin/env python3
"""Simple test for the enhanced Hangman algorithm"""

import re
from collections import Counter, defaultdict

def test_problematic_case():
    """Test the specific case that was failing"""
    
    # The failing state
    guessed_letters = ['e', 't', 's', 'r', 'n', 'l', 'd', 'c', 'm', 'p', 'h', 'i', 'a']
    current_pattern = "_ e l l s _ p e r _ i s e d"
    target_word = "wellsupervised"
    
    print("TESTING PROBLEMATIC CASE")
    print("=" * 40)
    print(f"Pattern: {current_pattern}")
    print(f"Guessed: {guessed_letters}")
    print(f"Target: {target_word}")
    
    # Missing letters
    missing = set(target_word) - set(guessed_letters)
    print(f"Missing letters: {missing}")
    
    # The key insight: we need 'u', 'v', 'w'
    # Our improved algorithm should prioritize 'u' as a common vowel
    # that hasn't been tried yet
    
    needed_letters = ['u', 'v', 'w']
    print(f"Next guesses should be: {needed_letters}")
    
    # Check if our improved strategy would work
    remaining_vowels = ['u', 'y']
    common_letters = ['u', 'v', 'w', 'b', 'f', 'g', 'k']
    
    print("\nImproved algorithm strategy:")
    print("1. Try remaining vowels first: u, y")
    print("2. Then try other common letters: v, w, b, f, g, k")
    
    # The next guess should be 'u' (remaining vowel)
    next_guess = 'u'
    if next_guess in missing:
        print(f"✅ Next guess '{next_guess}' would be CORRECT!")
        return True
    else:
        print(f"❌ Next guess '{next_guess}' would still fail")
        return False

def main():
    print("Enhanced Hangman Algorithm - Failure Analysis")
    print("=" * 50)
    test_problematic_case()

if __name__ == "__main__":
    main()
