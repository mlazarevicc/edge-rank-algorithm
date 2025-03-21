import pickle

from edge_rank import EdgeRank
from trie import Trie


def serilize_data(edge_rank):
    file1 = open("serilize_data.pickle", "wb")

    edge_rank.triePhrases = None
    pickle.dump(edge_rank, file1)

    file1.close()

def deserilize_data():
    file1 = open("serilize_data.pickle", "rb")

    edge_rank = EdgeRank()
    edge_rank = pickle.load(file1)
    edge_rank.triePhrases = Trie()

    make_trie_phrases(edge_rank)

    file1.close()
    return edge_rank

def make_trie_phrases(edge_rank):

    for post_list in edge_rank.posts.values():
        for post in post_list:
            edge_rank.triePhrases.add_phrases(post.post_id, post.content.lower())