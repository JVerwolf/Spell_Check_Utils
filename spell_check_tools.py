import sys


class Dictionary:
    """
    This class provides the back end for spell checking and predictive typing.
    The spell checking will return True if a word is in the dictionary, False otherwise.
    The predictive typing recomendation is based on frequency of usage.

    These methods provide good performance:
        For spell checking, performance is O(n) of the word being searched. (ie "algorithm" takes 9 steps)
        For predictive typing, performance is ~O(n) of the number of words in the dictionary that are the specified
        number of characters away from the input word. (ie "abso" will return "absolute, absolutely, absolution, ...
        with ~O(n) of all words that start with "abso" in the dictionary)
    """
    DICT_POS = 2
    FIRST_LETTER = 0
    USE_COUNT_POS = 0
    IS_WORD_POS = 1

    def spell_check(self, word):
        """
        This method checks to see if a word is in the dictionary.

        word -- the word spell-check
        Returns:    True if the word is in the dictionary
                    False if it is not
        """

        def recursive_traverse(word_list, sub_list):
            if len(word_list) > 0:
                if word_list[self.FIRST_LETTER] in sub_list[self.DICT_POS]:
                    # recursive call: remove one letter from the word_list and go one node deeper into the trie
                    return recursive_traverse(word_list[1:], sub_list[self.DICT_POS][word_list[self.FIRST_LETTER]])
                else:
                    return False  # case where 'word' branches outside of the trie, thus not in the dictionary
            else:
                return sub_list[1]  # contains a true or false value that indicates if 'word' is in the trie

        word_l = [c for c in word]
        return recursive_traverse(word_l, [0, False, self.trie])  # {letter: [uses, complete word?, subTRIE]}

    # TODO: Add functionality for shorter words to be recomended
    def predict_text(self, word, num_additional_chars=3, num_suggested_words=4):
        """
        Returns a list of suggestions based on 'word' param.
        num_additional_chars -- specifies the number of additional characters the suggestion may have.
        num_suggested_words -- specifies the number of words returned in the list of suggestions
        """

        def recursive_trie_traverse(word_list, sub_list):
            """traverses the TRIE untill the end of the word or until an attempt to traverse a non-existant branch"""
            if len(word_list) > 0:
                if word_list[self.FIRST_LETTER] in sub_list[self.DICT_POS]:
                    recursive_trie_traverse(word_list[1:], sub_list[self.DICT_POS][word_list[self.FIRST_LETTER]])
                else:
                    dfs_word_finder(sub_list, num_additional_chars, word_l[:])
            else:
                dfs_word_finder(sub_list, num_additional_chars, word_l[:])

        def recommend_list_generator(input_word, priority, recommended_list):
            """generates and maintains a sorted list of words of top priority"""

            # TODO: resolve unused params
            def insert(insert_word, pri, recommendation_list):
                """
                This method inserts 'insert_word' into sorted position in the recommendation_list. The length of the
                recommendation_list is maintained by poping off words of the smallest usage rating if the list exceeds
                the specified length
                """
                if len(recommendation_list) == 0:
                    recommendation_list.append((input_word, priority))
                else:
                    if priority > recommendation_list[-1][1]:
                        x = recommendation_list.pop()
                        insert(input_word, priority, recommendation_list)
                        recommendation_list.append(x)
                    else:
                        recommendation_list.append((input_word, priority))

            insert(input_word, priority, recommended_list)
            if len(recommended_list) > num_suggested_words:
                recommended_list.pop()  # maintains the proper list size, cuts down on unnecessary comparisons

        def dfs_word_finder(sub_list, length, word_list):
            """
            A variation of the DFS algorithm is used here to return words up to a given length. The algorithm starts at
            the sub-TRIE, which is the tree below the input word in the main TRIE. It then recursively digs down,
            checking to see if branches below are words, and calling the 'insert' method on them if they are.
            """
            if length > 0:
                for char in sub_list[self.DICT_POS]:
                    word_list.append(char)
                    if sub_list[self.DICT_POS][char][1]:  # Check to see if substring is a word
                        # add the word and used count to the recomended list
                        recommend_list_generator(''.join(word_list), sub_list[self.DICT_POS][char][0], recommended)
                    dfs_word_finder(sub_list[self.DICT_POS][char], length - 1, word_list)
                    word_list.pop()

        recommended = []  # all words that are the value of "count" edges away from the input word
        word_l = [c for c in word]
        recursive_trie_traverse(word_l, [0, False, self.trie])
        return [words[0] for words in recommended]

    def add_word_to_trie(self, word):
        """
        This method adds new words to the TRIE, but does not update theirr usage.
        Use it to input words from a dictionary
        """

        def trie_recursive_traverse(word_list, sub_list):
            if len(word_list) > 1:
                if word_list[self.FIRST_LETTER] in sub_list[self.DICT_POS]:
                    trie_recursive_traverse(word_list[1:], sub_list[self.DICT_POS][word_list[self.FIRST_LETTER]])
                else:
                    leaf_try = [0, False, {}]  # {letter: [uses, complete word?, subTRIE]}
                    sub_list[self.DICT_POS][word_list[self.USE_COUNT_POS]] = leaf_try
                    trie_recursive_traverse(word_list[1:], leaf_try)
            elif len(word_list) == 1:
                if word_list[self.FIRST_LETTER] in sub_list[self.DICT_POS]:
                    # if in the sublist, go to dictionary with first letter of wordlist as key, set sublist value to True
                    sub_list[self.DICT_POS][word_list[self.FIRST_LETTER]][1] = True
                else:
                    leaf_try = [0, True, {}]  # {letter: [uses, complete word?, subTRIE]}
                    sub_list[self.DICT_POS][word_list[self.USE_COUNT_POS]] = leaf_try

        word_l = [c for c in word]
        trie_recursive_traverse(word_l, [0, False, self.trie])  # {letter: [uses, complete word?, subTRIE]}
        return self.trie

    def add_usage(self, word):
        def trie_recursive_traverse(word_list, sub_list):
            if len(word_list) > 0:
                if word_list[self.FIRST_LETTER] in sub_list[self.DICT_POS]:
                    trie_recursive_traverse(word_list[1:], sub_list[self.DICT_POS][word_list[self.FIRST_LETTER]])
                else:
                    leaf_try = [0, False, {}]  # {letter: [uses, complete word?, subTRIE]}
                    sub_list[self.DICT_POS][word_list[self.USE_COUNT_POS]] = leaf_try
                    trie_recursive_traverse(word_list[1:], leaf_try)
            else:
                sub_list[0] += 1

        word_l = [c for c in word]
        trie_recursive_traverse(word_l, [0, False, self.trie])  # {letter: [uses, complete word?, subTRIE]}
        return self.trie

    def __init__(self, dictionary_file):
        """
        :param dictionary_file: the filename of the dictionary words.  Each word should be on a new line.
        """
        self.trie = {}  # Trie/Prefix-Tree that holds all the words in the dictionary
        try:
            dictionary_words = open(dictionary_file)
            for line in dictionary_words:
                line = line.strip()
                self.add_word_to_trie(line)
        except:
            print("Error: Unable to open " + dictionary_file, file=sys.stderr)
            quit()
        finally:
            dictionary_words.close()


t = Dictionary(sys.argv[1])

print(t.spell_check('a'))
print(t.spell_check('able'))
t.add_usage('able')
print(t.predict_text("abl", 10, 3))
