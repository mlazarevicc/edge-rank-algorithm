import re

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word_count = 0
        self.phrase_count = 0
        self.post_ids = set()  # Skup post_id-jeva povezanih sa rečju

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add_words(self, post_id, content):
        words = content.split()
        for word in words:
            self.add_word(post_id, word)

    def add_word(self, post_id, word):
        current = self.root
        for char in word:
            if char in [".", ",", "!", "?", '"', ";"]:
                break
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True
        current.word_count += 1
        current.post_ids.add(post_id)  # Dodaj post_id u skup post_id-jeva

    def search(self, words):
        result = []

        if len(words) > 1:
            result = self.search_word(words[0])

            for word in words[1:]:
                result2 = self.search_word(word)
                result = list(set(result).intersection(result2))

        else:
            result = self.search_word(words[0])

        return result

    def search_word(self, word):
        current = self.root
        for char in word:
            if char not in current.children:
                return []
            current = current.children[char]
        if current.is_end_of_word:
            return list(current.post_ids)
        return []

    # Pretraga autocomplete
    def autocomplete(self, prefix):
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        return self._get_autocomplete_words(current, prefix)

    def _get_autocomplete_words(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)

        for char, child in node.children.items():
            words.extend(self._get_autocomplete_words(child, prefix + char))

        return words

    # Regex za nalazenje fraza u tekstu
    def extract_phrases(self, text):
        pattern = r'"([^"]*)"'
        phrases = re.findall(pattern, text)

        return phrases

    def add_phrases(self, post_id, content):
        phrases = self.extract_phrases(content)
        for ph in phrases:
            self.add_phrase(post_id, ph)

    def add_phrase(self, post_id, phrase):
        words = phrase.lower().split()
        current = self.root
        for word in words:
            if word not in current.children:
                current.children[word] = TrieNode()
            current = current.children[word]

        current.phrase_count += 1
        current.post_ids.add(post_id)

        current.is_end_of_word = True

    def search_phrase(self, phrase):
        words = phrase.lower().split()
        current = self.root

        for word in words:
            if word not in current.children:
                return []
            current = current.children[word]

        return list(current.post_ids)