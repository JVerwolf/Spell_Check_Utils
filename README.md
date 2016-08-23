# Spell_Check_Utils
A fast module for spell checking and predictive-text.  Part of my self study into suffix-trees/TRIEs, DFS, and Algorithmic thinking in Python.

spell_check_tools.py is written as a module to provide spell check functionality, in addition to predictive text. It contains a Dictionary class to which:
- New words can be added
- A word's usage-count can be updated
- A list of suggestions can be returned when given a partial word (orded by previous usage-count)

Provided in the repository are two text files.  The first, list_of_english_words, is a list of ~38,000 valid English words to use as the input file parameter for the Dictionary class constructor.  Alternatively, a second file, list_of_test_words.txt, is provided for testing.  The two linux shell scripts provided will run the module using each of these respective text files.  The module can also be used as an import.

**Things that I am working-on/aware-of that need fixing:**
- Adding functionality to save usage-count
- Learning proper PEP style/documentation and applying it to this module
- Profiling to see if this TRIE approach even makes sense in terms of memory usage when using hashmaps, and if a TRIE impemented using lists might be better for memory usage (although this would probably cause a bit of a hit to performance).
