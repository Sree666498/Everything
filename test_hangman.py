#!/usr/bin/env python3
"""
Test script for the enhanced Hangman algorithm.
This demonstrates the algorithm functionality without requiring API access.
"""

import random
import re
from hangman_solution import HangmanAPI

class LocalHangmanTester:
    """Local tester for the Hangman algorithm without API calls"""
    
    def __init__(self, dictionary_file="words_250000_train.txt"):
        self.dictionary_file = dictionary_file
        self.load_dictionary()
        
    def load_dictionary(self):
        """Load the dictionary file"""
        try:
            with open(self.dictionary_file, 'r') as f:
                self.test_words = [line.strip().lower() for line in f.readlines()]
            print(f"Loaded {len(self.test_words)} words from {self.dictionary_file}")
        except FileNotFoundError:
            print(f"Dictionary file {self.dictionary_file} not found.")
            print("Run create_sample_dictionary.py first to create a sample dictionary.")
            return
    
    def simulate_game(self, secret_word, verbose=False):
        """Simulate a Hangman game with a given secret word"""
        if not hasattr(self, 'test_words'):
            return False
            
        # Initialize mock API object (without actual API calls)
        class MockAPI:
            def __init__(self, dictionary_file):
                # Load dictionary
                with open(dictionary_file, 'r') as f:
                    self.full_dictionary = [line.strip().lower() for line in f.readlines()]
                
                # Initialize the same way as real API
                self.full_dictionary_common_letter_sorted = []
                from collections import Counter, defaultdict
                counter = Counter("".join(self.full_dictionary))
                self.full_dictionary_common_letter_sorted = counter.most_common()
                
                self.guessed_letters = []
                self.current_dictionary = []
                self.word_length_dict = self._build_word_length_dict()
                self.position_frequency = self._build_position_frequency()
                self.common_patterns = self._build_common_patterns()
                self.vowels = set('aeiou')
                self.consonants = set('bcdfghjklmnpqrstvwxyz')
            
            def _build_word_length_dict(self):
                from collections import defaultdict
                word_length_dict = defaultdict(list)
                for word in self.full_dictionary:
                    word_length_dict[len(word)].append(word)
                return word_length_dict
            
            def _build_position_frequency(self):
                from collections import defaultdict
                position_freq = defaultdict(lambda: defaultdict(int))
                for word in self.full_dictionary:
                    for i, letter in enumerate(word):
                        position_freq[len(word)][i][letter] += 1
                return position_freq
            
            def _build_common_patterns(self):
                from collections import defaultdict
                patterns = defaultdict(int)
                for word in self.full_dictionary:
                    for i in range(len(word) - 1):
                        bigram = word[i:i+2]
                        patterns[bigram] += 1
                return patterns
        
        # Create mock API instance
        mock_api = MockAPI(self.dictionary_file)
        
        # Copy all the guess methods from HangmanAPI
        mock_api.guess = HangmanAPI.guess.__get__(mock_api, MockAPI)
        mock_api._guess_from_few_candidates = HangmanAPI._guess_from_few_candidates.__get__(mock_api, MockAPI)
        mock_api._position_aware_guess = HangmanAPI._position_aware_guess.__get__(mock_api, MockAPI)
        mock_api._pattern_based_guess = HangmanAPI._pattern_based_guess.__get__(mock_api, MockAPI)
        mock_api._vowel_consonant_strategy = HangmanAPI._vowel_consonant_strategy.__get__(mock_api, MockAPI)
        mock_api._fallback_guess = HangmanAPI._fallback_guess.__get__(mock_api, MockAPI)
        
        # Initialize game state
        mock_api.guessed_letters = []
        mock_api.current_dictionary = mock_api.full_dictionary
        
        secret_word = secret_word.lower()
        current_word = ['_'] * len(secret_word)
        incorrect_guesses = 0
        max_incorrect = 6
        
        if verbose:
            print(f"\nStarting game with word: {'*' * len(secret_word)} ({len(secret_word)} letters)")
        
        while incorrect_guesses < max_incorrect:
            # Create current word display (space-separated)
            word_display = ' '.join(current_word)
            
            if verbose:
                print(f"Current word: {word_display}")
                print(f"Guessed letters: {', '.join(sorted(mock_api.guessed_letters))}")
                print(f"Incorrect guesses: {incorrect_guesses}/{max_incorrect}")
            
            # Check if word is complete
            if '_' not in current_word:
                if verbose:
                    print(f"SUCCESS! Word was: {secret_word}")
                return True
            
            # Get guess from algorithm
            guess = mock_api.guess(word_display)
            
            if verbose:
                print(f"Algorithm guesses: {guess}")
            
            # Process guess
            if guess in secret_word:
                # Correct guess - reveal letters
                for i, letter in enumerate(secret_word):
                    if letter == guess:
                        current_word[i] = letter
                if verbose:
                    print(f"Correct! '{guess}' is in the word.")
            else:
                # Incorrect guess
                incorrect_guesses += 1
                if verbose:
                    print(f"Incorrect! '{guess}' is not in the word.")
            
            # Add to guessed letters
            mock_api.guessed_letters.append(guess)
            
            if verbose:
                print("-" * 40)
        
        if verbose:
            print(f"FAILED! Word was: {secret_word}")
            print(f"Final state: {' '.join(current_word)}")
        
        return False
    
    def run_test_suite(self, num_games=100, verbose=False):
        """Run a test suite with random words"""
        if not hasattr(self, 'test_words'):
            return
            
        print(f"\nRunning test suite with {num_games} games...")
        
        successes = 0
        test_words = random.sample(self.test_words, min(num_games, len(self.test_words)))
        
        for i, word in enumerate(test_words):
            if verbose:
                print(f"\n=== Game {i+1}/{num_games} ===")
            
            success = self.simulate_game(word, verbose=verbose)
            if success:
                successes += 1
            
            if not verbose and (i + 1) % 10 == 0:
                print(f"Completed {i+1}/{num_games} games... Current success rate: {successes/(i+1):.3f}")
        
        success_rate = successes / num_games
        print(f"\n=== TEST RESULTS ===")
        print(f"Games played: {num_games}")
        print(f"Successes: {successes}")
        print(f"Success rate: {success_rate:.3f} ({success_rate*100:.1f}%)")
        
        if success_rate > 0.18:
            improvement = success_rate / 0.18
            print(f"Improvement over baseline: {improvement:.2f}x")
            print("✅ Algorithm successfully outperforms 18% baseline!")
        else:
            print("❌ Algorithm needs improvement to beat baseline.")
        
        return success_rate

def main():
    """Main test function"""
    print("Enhanced Hangman Algorithm Tester")
    print("=" * 40)
    
    # Create tester
    tester = LocalHangmanTester()
    
    # Test with a few specific words first
    print("\n1. Testing specific words:")
    test_words = ["python", "algorithm", "computer", "science", "hangman"]
    for word in test_words:
        print(f"\nTesting word: {word}")
        success = tester.simulate_game(word, verbose=True)
        print(f"Result: {'SUCCESS' if success else 'FAILED'}")
    
    # Run larger test suite
    print("\n" + "=" * 60)
    print("2. Running larger test suite:")
    tester.run_test_suite(num_games=50, verbose=False)

if __name__ == "__main__":
    main()