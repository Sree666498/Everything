#!/usr/bin/env python3
"""
Setup and test script for the Enhanced Hangman Algorithm.
This script will create a sample dictionary and run tests to demonstrate the algorithm.
"""

import os
import sys

def setup():
    """Setup the testing environment"""
    print("Setting up Enhanced Hangman Algorithm test environment...")
    print("=" * 60)
    
    # Check if dictionary exists
    if not os.path.exists("words_250000_train.txt"):
        print("Creating sample dictionary...")
        try:
            # Import and run the dictionary creator
            from create_sample_dictionary import main as create_dict
            create_dict()
            print("✅ Sample dictionary created successfully!")
        except ImportError:
            print("❌ Could not import create_sample_dictionary module")
            return False
    else:
        print("✅ Dictionary file already exists")
    
    return True

def run_tests():
    """Run the test suite"""
    print("\n" + "=" * 60)
    print("Running Enhanced Hangman Algorithm Tests")
    print("=" * 60)
    
    try:
        from test_hangman import main as run_tests
        run_tests()
        return True
    except ImportError as e:
        print(f"❌ Could not import test module: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Main setup and test function"""
    print("🎯 Enhanced Hangman Algorithm - Trexquant Interview Project")
    print("Developed to significantly outperform the 18% baseline success rate")
    print()
    
    # Setup
    if not setup():
        print("❌ Setup failed. Exiting.")
        return
    
    # Run tests
    if not run_tests():
        print("❌ Tests failed.")
        return
    
    print("\n" + "=" * 60)
    print("🎉 SETUP AND TESTING COMPLETE!")
    print("=" * 60)
    print()
    print("Next steps for submission:")
    print("1. Replace the sample dictionary with the actual words_250000_train.txt from Trexquant")
    print("2. Add your API access token to hangman_solution.py")
    print("3. Run practice games to validate performance")
    print("4. Submit hangman_solution.py when satisfied with results")
    print()
    print("Files created:")
    print("  📄 hangman_solution.py - Main enhanced algorithm")
    print("  📄 test_hangman.py - Local testing framework")
    print("  📄 create_sample_dictionary.py - Sample dictionary generator")
    print("  📄 words_250000_train.txt - Training dictionary")
    print("  📄 README.md - Comprehensive documentation")

if __name__ == "__main__":
    main()