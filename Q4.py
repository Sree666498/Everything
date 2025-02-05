def count_vowels(input_string):
    vowels = "aeiouAEIOU"
    count = 0
    for char in input_string:
        if char in vowels:
            count = count + 1
    return count

str1 = input("Enter a string: ")
vowel_count = count_vowels(str1)
print(f"The number of vowels in the given string is {vowel_count}")