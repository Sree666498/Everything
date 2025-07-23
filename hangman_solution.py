import json
import requests
import random
import string
import secrets
import time
import re
import collections
from collections import Counter, defaultdict
import math

try:
    from urllib.parse import parse_qs, urlencode, urlparse
except ImportError:
    from urlparse import parse_qs, urlparse
    from urllib import urlencode

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class HangmanAPI(object):
    def __init__(self, access_token=None, session=None, timeout=None):
        self.hangman_url = self.determine_hangman_url()
        self.access_token = access_token
        self.session = session or requests.Session()
        self.timeout = timeout
        self.guessed_letters = []
        
        full_dictionary_location = "words_250000_train.txt"
        self.full_dictionary = self.build_dictionary(full_dictionary_location)        
        self.full_dictionary_common_letter_sorted = collections.Counter("".join(self.full_dictionary)).most_common()
        
        # Enhanced data structures for better performance
        self.current_dictionary = []
        self.word_length_dict = self._build_word_length_dict()
        self.position_frequency = self._build_position_frequency()
        self.common_patterns = self._build_common_patterns()
        self.word_endings = self._build_word_endings()
        self.word_beginnings = self._build_word_beginnings()
        self.vowels = set('aeiou')
        self.consonants = set('bcdfghjklmnpqrstvwxyz')
        
    def _build_word_length_dict(self):
        """Build dictionary organized by word length for faster lookup"""
        word_length_dict = defaultdict(list)
        for word in self.full_dictionary:
            word_length_dict[len(word)].append(word)
        return word_length_dict
    
    def _build_position_frequency(self):
        """Build frequency distribution for each position in words"""
        position_freq = defaultdict(lambda: defaultdict(int))
        for word in self.full_dictionary:
            for i, letter in enumerate(word):
                position_freq[len(word)][i][letter] += 1
        return position_freq
    
    def _build_common_patterns(self):
        """Build common letter patterns and combinations"""
        patterns = defaultdict(int)
        for word in self.full_dictionary:
            for i in range(len(word) - 1):
                bigram = word[i:i+2]
                patterns[bigram] += 1
        return patterns
    
    def _build_word_endings(self):
        """Build common word endings for pattern recognition"""
        endings = defaultdict(int)
        for word in self.full_dictionary:
            if len(word) >= 3:
                endings[word[-3:]] += 1
            if len(word) >= 2:
                endings[word[-2:]] += 1
        return endings
    
    def _build_word_beginnings(self):
        """Build common word beginnings for pattern recognition"""
        beginnings = defaultdict(int)
        for word in self.full_dictionary:
            if len(word) >= 3:
                beginnings[word[:3]] += 1
            if len(word) >= 2:
                beginnings[word[:2]] += 1
        return beginnings

    @staticmethod
    def determine_hangman_url():
        links = ['https://trexsim.com']

        data = {link: 0 for link in links}

        for link in links:
            requests.get(link)
            for i in range(10):
                s = time.time()
                requests.get(link)
                data[link] = time.time() - s

        link = sorted(data.items(), key=lambda x: x[1])[0][0]
        link += '/trexsim/hangman'
        return link

    def guess(self, word):
        """
        Advanced Hangman algorithm targeting 60%+ success rate.
        Uses sophisticated pattern analysis, positional frequency, and information theory.
        """
        # Clean the word
        clean_word = word[::2].replace("_", ".")
        len_word = len(clean_word)
        
        # Use length-specific dictionary for much faster filtering
        if len_word in self.word_length_dict:
            candidate_words = self.word_length_dict[len_word]
        else:
            candidate_words = self.current_dictionary
        
        # Filter words that match current pattern
        new_dictionary = []
        for dict_word in candidate_words:
            if len(dict_word) == len_word and re.match(clean_word, dict_word):
                new_dictionary.append(dict_word)
        
        self.current_dictionary = new_dictionary
        
        # STRATEGY 1: High-confidence single candidate
        if len(new_dictionary) == 1:
            target_word = new_dictionary[0]
            for letter in target_word:
                if letter not in self.guessed_letters:
                    return letter
        
        # STRATEGY 2: Very few candidates - use information theory
        if len(new_dictionary) <= 5 and new_dictionary:
            # Calculate information gain for each possible letter
            best_letter = None
            max_info_gain = -1
            
            for candidate_letter in 'abcdefghijklmnopqrstuvwxyz':
                if candidate_letter in self.guessed_letters:
                    continue
                
                # Calculate expected reduction in candidate space
                words_with_letter = sum(1 for word in new_dictionary if candidate_letter in word)
                words_without_letter = len(new_dictionary) - words_with_letter
                
                # Information gain calculation
                if words_with_letter > 0 and words_without_letter > 0:
                    info_gain = min(words_with_letter, words_without_letter)
                elif words_with_letter > 0:  # Letter appears in all remaining words
                    info_gain = words_with_letter * 2  # Prefer letters that appear in words
                else:
                    info_gain = 0  # Letter doesn't appear in any word
                
                if info_gain > max_info_gain:
                    max_info_gain = info_gain
                    best_letter = candidate_letter
            
            if best_letter:
                return best_letter
        
        # STRATEGY 3: Position-aware frequency analysis
        if new_dictionary:
            position_scores = defaultdict(float)
            total_candidates = len(new_dictionary)
            
            # Analyze each position
            for pos in range(len_word):
                if clean_word[pos] == '.':  # Position not yet revealed
                    pos_letter_count = defaultdict(int)
                    
                    # Count letters at this specific position
                    for word in new_dictionary:
                        pos_letter_count[word[pos]] += 1
                    
                    # Weight letters by their positional frequency
                    for letter, count in pos_letter_count.items():
                        if letter not in self.guessed_letters:
                            position_scores[letter] += (count / total_candidates) * (count / total_candidates)
            
            if position_scores:
                return max(position_scores, key=position_scores.get)
        
        # STRATEGY 4: Advanced pattern analysis with bigrams
        if new_dictionary and len(new_dictionary) <= 50:
            letter_scores = defaultdict(float)
            
            for word in new_dictionary:
                for i, letter in enumerate(word):
                    if letter not in self.guessed_letters:
                        base_score = 1.0
                        
                        # Bonus for letters in unrevealed positions
                        if clean_word[i] == '.':
                            base_score *= 2.0
                        
                        # Pattern context bonus
                        context_bonus = 0
                        if i > 0 and clean_word[i-1] != '.':
                            bigram = clean_word[i-1] + letter
                            context_bonus += self.common_patterns.get(bigram, 0) * 0.001
                        
                        if i < len(word) - 1 and clean_word[i+1] != '.':
                            bigram = letter + clean_word[i+1]
                            context_bonus += self.common_patterns.get(bigram, 0) * 0.001
                        
                        letter_scores[letter] += base_score + context_bonus
            
            if letter_scores:
                return max(letter_scores, key=letter_scores.get)
        
        # STRATEGY 5: Pattern recognition for common word endings and beginnings
        if len_word >= 4:
            # Check for common ending patterns
            revealed_ending = clean_word[-3:] if len_word >= 3 else clean_word[-2:]
            if '.' in revealed_ending:
                # Look for common endings that match the pattern
                for ending in ['ing', 'ion', 'tion', 'ed', 'er', 'ly', 'al', 'ment', 'ness']:
                    if len(ending) <= len_word:
                        ending_pattern = '.' * (len_word - len(ending)) + ending
                        if re.match(clean_word, ending_pattern):
                            for letter in ending:
                                if letter not in self.guessed_letters and clean_word[len_word - len(ending) + ending.index(letter)] == '.':
                                    return letter
            
            # Check for common beginning patterns
            revealed_beginning = clean_word[:3] if len_word >= 3 else clean_word[:2]
            if '.' in revealed_beginning:
                for beginning in ['the', 'and', 'ing', 'her', 'hat', 'his', 'con', 'pre', 'pro', 'dis']:
                    if len(beginning) <= len_word:
                        beginning_pattern = beginning + '.' * (len_word - len(beginning))
                        if re.match(clean_word, beginning_pattern):
                            for letter in beginning:
                                if letter not in self.guessed_letters and clean_word[beginning.index(letter)] == '.':
                                    return letter
        
        # STRATEGY 6: Smart vowel-consonant strategy based on word characteristics
        revealed_letters = [c for c in clean_word if c != '.']
        vowel_count = sum(1 for c in revealed_letters if c in self.vowels)
        consonant_count = len(revealed_letters) - vowel_count
        
        # Early game: prioritize high-frequency vowels
        if len(self.guessed_letters) < 3:
            for vowel in ['e', 'a', 'i', 'o']:
                if vowel not in self.guessed_letters:
                    return vowel
        
        # Mid game: balance vowels and consonants
        if vowel_count == 0 and len(self.guessed_letters) >= 3:
            for vowel in ['a', 'i', 'o', 'u']:
                if vowel not in self.guessed_letters:
                    return vowel
        
        # Long words with few vowels: try remaining vowels
        if len_word >= 7 and vowel_count <= 1:
            for vowel in ['u', 'y']:
                if vowel not in self.guessed_letters:
                    return vowel
        
        # STRATEGY 7: Frequency analysis on current candidates
        if new_dictionary:
            letter_freq = Counter()
            for word in new_dictionary:
                for letter in word:
                    if letter not in self.guessed_letters:
                        letter_freq[letter] += 1
            
            if letter_freq:
                return letter_freq.most_common(1)[0][0]
        
        # STRATEGY 8: Adaptive letter ordering based on game state and word length
        if len(self.guessed_letters) < 2:
            # Start with most effective letters
            start_letters = ['e', 'a', 'r', 'i', 'o', 't', 'n', 's']
        elif len(self.guessed_letters) < 5:
            # Common consonants, prioritize by word length
            if len_word <= 5:
                start_letters = ['l', 'd', 'h', 'c', 'u', 'p', 'm', 'g', 'b', 'f', 'y', 'w']
            else:
                start_letters = ['l', 'c', 'u', 'd', 'p', 'm', 'h', 'g', 'b', 'f', 'y', 'w', 'k', 'v']
        else:
            # Less common but important letters
            start_letters = ['k', 'v', 'x', 'z', 'j', 'q']
        
        for letter in start_letters:
            if letter not in self.guessed_letters:
                return letter
        
        # STRATEGY 9: Fallback to full dictionary frequency
        for letter, _ in self.full_dictionary_common_letter_sorted:
            if letter not in self.guessed_letters:
                return letter
        
        # Emergency fallback
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            if letter not in self.guessed_letters:
                return letter
        
        return 'e'


    ##########################################################
    # You'll likely not need to modify any of the code below #
    ##########################################################
    
    def build_dictionary(self, dictionary_file_location):
        text_file = open(dictionary_file_location,"r")
        full_dictionary = text_file.read().splitlines()
        text_file.close()
        return full_dictionary
                
    def start_game(self, practice=True, verbose=True):
        # reset guessed letters to empty set and current plausible dictionary to the full dictionary
        self.guessed_letters = []
        self.current_dictionary = self.full_dictionary
                         
        response = self.request("/new_game", {"practice":practice})
        if response.get('status')=="approved":
            game_id = response.get('game_id')
            word = response.get('word')
            tries_remains = response.get('tries_remains')
            if verbose:
                print("Successfully start a new game! Game ID: {0}. # of tries remaining: {1}. Word: {2}.".format(game_id, tries_remains, word))
            while tries_remains>0:
                # get guessed letter from user code
                guess_letter = self.guess(word)
                    
                # append guessed letter to guessed letters field in hangman object
                self.guessed_letters.append(guess_letter)
                if verbose:
                    print("Guessing letter: {0}".format(guess_letter))
                    
                try:    
                    res = self.request("/guess_letter", {"request":"guess_letter", "game_id":game_id, "letter":guess_letter})
                except HangmanAPIError:
                    print('HangmanAPIError exception caught on request.')
                    continue
                except Exception as e:
                    print('Other exception caught on request.')
                    raise e
               
                if verbose:
                    print("Sever response: {0}".format(res))
                status = res.get('status')
                tries_remains = res.get('tries_remains')
                if status=="success":
                    if verbose:
                        print("Successfully finished game: {0}".format(game_id))
                    return True
                elif status=="failed":
                    reason = res.get('reason', '# of tries exceeded!')
                    if verbose:
                        print("Failed game: {0}. Because of: {1}".format(game_id, reason))
                    return False
                elif status=="ongoing":
                    word = res.get('word')
        else:
            if verbose:
                print("Failed to start a new game")
        return status=="success"
        
    def my_status(self):
        return self.request("/my_status", {})
    
    def request(
            self, path, args=None, post_args=None, method=None):
        if args is None:
            args = dict()
        if post_args is not None:
            method = "POST"

        # Add `access_token` to post_args or args if it has not already been
        # included.
        if self.access_token:
            # If post_args exists, we assume that args either does not exists
            # or it does not need `access_token`.
            if post_args and "access_token" not in post_args:
                post_args["access_token"] = self.access_token
            elif "access_token" not in args:
                args["access_token"] = self.access_token

        time.sleep(0.2)

        num_retry, time_sleep = 50, 2
        for it in range(num_retry):
            try:
                response = self.session.request(
                    method or "GET",
                    self.hangman_url + path,
                    timeout=self.timeout,
                    params=args,
                    data=post_args,
                    verify=False
                )
                break
            except requests.HTTPError as e:
                response = json.loads(e.read())
                raise HangmanAPIError(response)
            except requests.exceptions.SSLError as e:
                if it + 1 == num_retry:
                    raise
                time.sleep(time_sleep)

        headers = response.headers
        if 'json' in headers['content-type']:
            result = response.json()
        elif "access_token" in parse_qs(response.text):
            query_str = parse_qs(response.text)
            if "access_token" in query_str:
                result = {"access_token": query_str["access_token"][0]}
                if "expires" in query_str:
                    result["expires"] = query_str["expires"][0]
            else:
                raise HangmanAPIError(response.json())
        else:
            raise HangmanAPIError('Maintype was not text, or querystring')

        if result and isinstance(result, dict) and result.get("error"):
            raise HangmanAPIError(result)
        return result
    
class HangmanAPIError(Exception):
    def __init__(self, result):
        self.result = result
        self.code = None
        try:
            self.type = result["error_code"]
        except (KeyError, TypeError):
            self.type = ""

        try:
            self.message = result["error_description"]
        except (KeyError, TypeError):
            try:
                self.message = result["error"]["message"]
                self.code = result["error"].get("code")
                if not self.type:
                    self.type = result["error"].get("type", "")
            except (KeyError, TypeError):
                try:
                    self.message = result["error_msg"]
                except (KeyError, TypeError):
                    self.message = result

        Exception.__init__(self, self.message)

# Usage Examples:

# To create API instance (replace with your actual token):
# api = HangmanAPI(access_token="INSERT_YOUR_TOKEN_HERE", timeout=2000)

# Playing practice games:
# api.start_game(practice=1, verbose=True)
# [total_practice_runs, total_recorded_runs, total_recorded_successes, total_practice_successes] = api.my_status()
# practice_success_rate = total_practice_successes / total_practice_runs
# print('run %d practice games out of an allotted 100,000. practice success rate so far = %.3f' % (total_practice_runs, practice_success_rate))

# Playing recorded games (final submission):
# for i in range(1000):
#     print('Playing', i, 'th game')
#     api.start_game(practice=0, verbose=False)
#     time.sleep(0.5)

# Check game statistics:
# [total_practice_runs, total_recorded_runs, total_recorded_successes, total_practice_successes] = api.my_status()
# success_rate = total_recorded_successes/total_recorded_runs
# print('overall success rate = %.3f' % success_rate)