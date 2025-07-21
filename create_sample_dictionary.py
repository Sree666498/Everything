#!/usr/bin/env python3
"""
Sample script to create a training dictionary for testing the Hangman algorithm.
This is just for demonstration - you should use the actual words_250000_train.txt 
file provided by Trexquant.
"""

import random

def create_sample_dictionary():
    """Create a small sample dictionary for testing purposes"""
    
    # Common English words of various lengths
    sample_words = [
        # 3-letter words
        "the", "and", "for", "are", "but", "not", "you", "all", "can", "had",
        "her", "was", "one", "our", "out", "day", "get", "has", "him", "his",
        "how", "its", "may", "new", "now", "old", "see", "two", "way", "who",
        "boy", "did", "man", "car", "cat", "dog", "run", "big", "red", "hot",
        
        # 4-letter words
        "that", "with", "have", "this", "will", "your", "from", "they", "know",
        "want", "been", "good", "much", "some", "time", "very", "when", "come",
        "here", "just", "like", "long", "make", "many", "over", "such", "take",
        "than", "them", "well", "work", "call", "first", "last", "name", "part",
        "find", "give", "hand", "high", "keep", "kind", "left", "life", "live",
        
        # 5-letter words
        "which", "their", "would", "there", "could", "other", "after", "first",
        "never", "these", "think", "where", "being", "every", "great", "might",
        "shall", "still", "those", "under", "while", "about", "again", "before",
        "found", "going", "house", "large", "place", "right", "small", "sound",
        "still", "water", "world", "years", "young", "asked", "black", "bring",
        
        # 6-letter words
        "should", "through", "during", "follow", "around", "ground", "number",
        "public", "school", "second", "enough", "though", "little", "change",
        "differ", "between", "another", "example", "because", "without", "country",
        "problem", "against", "nothing", "someone", "machine", "morning", "question",
        "special", "working", "feeling", "picture", "evening", "getting", "reading",
        
        # 7-letter words
        "because", "between", "another", "example", "without", "through", "problem",
        "against", "nothing", "someone", "machine", "morning", "picture", "evening",
        "getting", "reading", "writing", "looking", "working", "feeling", "general",
        "however", "further", "thought", "process", "develop", "require", "present",
        "company", "service", "outside", "program", "project", "provide", "support",
        
        # 8-letter words
        "business", "standard", "language", "together", "building", "national",
        "question", "complete", "remember", "although", "yourself", "yourself",
        "practice", "material", "possible", "research", "industry", "consider",
        "response", "identify", "continue", "specific", "increase", "approach",
        "maintain", "strategy", "security", "analysis", "customer", "decision",
        
        # 9+ letter words
        "important", "different", "following", "community", "available", "education",
        "something", "marketing", "knowledge", "equipment", "effective", "financial",
        "statement", "structure", "executive", "operation", "establish", "influence",
        "character", "determine", "condition", "situation", "including", "authority",
        "advantage", "necessary", "treatment", "agreement", "interview", "management",
        "technology", "information", "development", "environment", "performance",
        "government", "experience", "particular", "understand", "individual"
    ]
    
    # Add more variety by including some less common but valid words
    additional_words = [
        "quiz", "jinx", "waltz", "fizz", "buzz", "jazz", "fuzz", "whiz",
        "gypsy", "kayak", "zebra", "zesty", "quirk", "fjord", "vixen",
        "yacht", "xerus", "azure", "blitz", "chunk", "dwarf", "flunk",
        "gruff", "lymph", "nymph", "psalm", "rugby", "sylph", "truly"
    ]
    
    all_words = sample_words + additional_words
    
    # Remove duplicates and sort
    unique_words = sorted(list(set(all_words)))
    
    return unique_words

def main():
    """Create the sample dictionary file"""
    words = create_sample_dictionary()
    
    # Write to file
    with open("words_250000_train.txt", "w") as f:
        for word in words:
            f.write(word.lower() + "\n")
    
    print(f"Created sample dictionary with {len(words)} words.")
    print("Note: This is just a small sample for testing.")
    print("Use the actual words_250000_train.txt provided by Trexquant for submission.")
    
    # Display some statistics
    length_dist = {}
    for word in words:
        length = len(word)
        length_dist[length] = length_dist.get(length, 0) + 1
    
    print("\nWord length distribution:")
    for length in sorted(length_dist.keys()):
        print(f"  {length} letters: {length_dist[length]} words")

if __name__ == "__main__":
    main()