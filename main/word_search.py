# -*- coding: utf-8 -*-
"""
Class to build a TrieNode for word search using a preloaded list of 10000
words.
"""

WORD_LIST_FILE = "wordlist_10000.txt"


class TrieNode:
    def __init__(self):
        self.dict_ = {}
        self.end_of_word = False


class WordSearch:
    def __init__(self):
        self.__word_lst__ = self.__load_word_list__()
        self.__word_dict__ = TrieNode()
        self.__preload_words__()

    def __preload_words__(self) -> None:
        """
        Preload words from the given word list file into memory using TrieNode
        data structure. Time complexity O(n) with n being total number of words
        in the given list.

        """

        for word in self.__word_lst__:
            curr_node = self.__word_dict__
            for char in word:
                if char not in curr_node.dict_:
                    curr_node.dict_[char] = TrieNode()
                curr_node = curr_node.dict_[char]
            curr_node.end_of_word = True

    def __possible_word_dfs__(
        self, node: TrieNode, auto_completed_result: list, curr_word: str
    ) -> None:
        """
        DFS function to search all possible words from the given
        TrieNode branch

        Args:
            auto_completed_result (list): list of all possible words
            curr_word (str): current word from the branch
        """
        # Base cases
        if node.end_of_word:
            auto_completed_result.append(curr_word)

        for char in node.dict_:
            self.__possible_word_dfs__(
                node.dict_[char], auto_completed_result, curr_word + char
            )

    def auto_complete_word(self, curr_word: str) -> list:
        """
        Function to list all possible words based on a given word

        Args:
            curr_word (str): current word entered by the user.

        Returns:
            list: a list of all possible words that can be constructed using
            the user given curren word.

        """

        auto_completed_result = []
        curr_node = self.__word_dict__
        possible_word = ""

        for char in curr_word:
            # Reach the end of possible TrieNode
            if char in curr_node.dict_:
                possible_word += char
                curr_node = curr_node.dict_[char]
            # If a word can't be reach till the end
            # => the word doesn't exist in the dictionary
            else:
                return []

        # Run dfs and add all possible words
        self.__possible_word_dfs__(
            curr_node, auto_completed_result, possible_word
        )

        return auto_completed_result

    def __load_word_list__(self) -> None:
        """
        Open directory for the file with all the words to be preloaded into
        memory.

        """

        with open(WORD_LIST_FILE, "r") as inputfile:
            lst = inputfile.read().splitlines()
            return lst
