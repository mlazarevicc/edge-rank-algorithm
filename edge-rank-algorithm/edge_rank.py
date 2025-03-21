from datetime import datetime
from data_classes import *

from trie import Trie
import networkx as nx

current_time = datetime.now()

class EdgeRank:

    def __init__(self):
        self.users = {}
        self.posts = {}
        self.shares = {}
        self.comments = {}
        self.reactions = {}
        self.trie = Trie()
        self.graph = nx.DiGraph()
        self.triePhrases = Trie()

    def get_interaction_weight(self, interaction_type):

        if interaction_type == "likes":
            return 0.1
        elif interaction_type == "comments":
            return 0.5
        elif interaction_type == "shares":
            return 1
        elif interaction_type == "loves":
            return 0.2
        else:
            return 0.15  # Default weight

    def add_user(self, user_id, friends):
        user = User(user_id, friends)
        self.users[user_id] = user
        self.graph.add_node(user_id)

    def add_post(self, post_id, content, link_name, status_type, status_link, status_published, author_id,
                 num_reactions=0, num_comments=0, num_shares=0, num_likes=0, num_loves=0, num_wows=0, num_hahas=0,
                 num_sads=0, num_angrys=0, num_special=0):

        post = Post(post_id, content, link_name, status_type, status_link,
                    datetime.strptime(status_published, '%Y-%m-%d %H:%M:%S'), author_id, int(num_reactions),
                    int(num_comments), int(num_shares), int(num_likes), int(num_loves), int(num_wows), int(num_hahas),
                    int(num_sads), int(num_angrys), int(num_special))

        if author_id in self.posts:
            self.posts[author_id].append(post)
        else:
            self.posts[author_id] = [post]

        self.trie.add_words(post_id, content.lower())
        self.triePhrases.add_phrases(post_id, content.lower())

    def add_comment(self, comment_id, status_id, parent_id, comment_message, comment_author, comment_published,
                    num_reactions, num_likes, num_loves, num_wows, num_hahas, num_sads, num_angrys, num_special):
        com = Comment(comment_id, status_id, parent_id, comment_message, comment_author,
                      datetime.strptime(comment_published, '%Y-%m-%d %H:%M:%S'), int(num_reactions), int(num_likes),
                      int(num_loves), int(num_wows), int(num_hahas), int(num_sads), int(num_angrys), int(num_special))

        if (self.users[comment_author].user_id, status_id) in self.comments:
            self.comments[(self.users[comment_author].user_id, status_id)].append(com)
        else:
            self.comments[(self.users[comment_author].user_id, status_id)] = [com]

    def add_share(self, status_id, sharer, status_shared):
        self.shares[(self.users[sharer].user_id, status_id)] = Share(status_id, sharer, datetime.strptime(status_shared,'%Y-%m-%d %H:%M:%S'))

    def add_reactions(self, status_id, type_of_reaction, reactor, reacted):
        reaction = Reaction(status_id, type_of_reaction, reactor, datetime.strptime(reacted, '%Y-%m-%d %H:%M:%S'))

        self.reactions[(self.users[reactor].user_id, status_id)] = reaction

    def calculate_edge_rank(self, user_id, post: Post):

        edge_rank = 0.0
        if self.graph.has_edge(user_id, post.author_id):
            edge_rank += self.graph.get_edge_data(user_id, post.author_id)['weight']

        edge_rank += self.popular_post(post)

        global current_time
        edge_rank *= self.get_decay_factor(current_time - post.status_published)

        return edge_rank

    def popular_post(self, post: Post):

        sum = 0.0

        if post.num_reactions > 0:
            sum += 3 / post.num_reactions
        elif post.interactionsNum["shares"] > 0:
            sum += 3 / (3 * post.interactionsNum["shares"])
        elif post.interactionsNum["comments"] > 0:
            sum += 3 / (2 * post.interactionsNum["comments"])

        if sum > 0:
            return 3 - sum
        return 0

    def get_decay_factor(self, time_difference):
        difference = time_difference.days

        if difference < 5:
            return 0
        else:
            return 1 / (2 * (time_difference.days))

    def top10_posts(self, user_id):
        matching_posts = []
        for post_list in self.posts.values():
            matching_posts.extend(post_list)

        matching_posts.sort(key=lambda post: self.calculate_edge_rank(user_id, post), reverse=True)
        return matching_posts[:10]

    # Pretraga po recima
    def search_posts(self, query, user_id):

        matching_posts = []

        query_words = query.lower().split()
        for post_id in self.trie.search(query_words):
            post = self.find_post(post_id)
            if post not in matching_posts:
                matching_posts.append(post)

        if len(matching_posts) > 0:
            matching_posts.sort(key=lambda post: self.calculate_edge_rank(user_id, post), reverse=True)
            return matching_posts[:10]
        else:
            return matching_posts

    def find_post(self, post_id):
        for posts_list in self.posts.values():
            for p in posts_list:
                if p.post_id == post_id:
                    return p

        return None

    # Pretraga fraza
    def rank_posts(self, user_id, phrase):
        post_ids = self.triePhrases.search_phrase(phrase)

        ranked_posts = []
        for post_id in post_ids:
            post = self.find_post(post_id)
            ranked_posts.append(post)


        ranked_posts.sort(key=lambda post: self.calculate_edge_rank(user_id, post), reverse=True)
        return ranked_posts[:10]

    def makeGraph(self):

        for user_id in self.users:
            for user2_id in self.posts.keys():
                if user2_id != user_id :

                    edge_rank = self.calculate_afinity(user_id, user2_id)
                    if edge_rank > 0:
                        self.graph.add_edge(user_id, user2_id, weight=edge_rank)

    def calculate_afinity(self, user_id, user2_id):
        edge_rank = 0.0
        global current_time

        for post in self.posts[user2_id]:
            edge_rank += self.calculate_reactions(user_id, post) * 0.5

            for friend_id in self.users[user_id].friends:
                if friend_id != post.author_id:
                    edge_rank += self.calculate_reactions(friend_id,post) * 0.1
                else:
                    edge_rank *= 2

                # Da ne bih zakasnio sa predajom projekta sam uklonio iz programa deo koji na edge_rank dodaje i
                # afinitet prijatelja prijatelja

                # for friend_of_friend_id in self.users[friend_id].friends:
                #     if friend_of_friend_id not in [user_id, post.author_id]:
                #         edge_rank += self.calculate_reactions(friend_of_friend_id,post) * 0.005

        return edge_rank

    def calculate_reactions(self, user_id, post: Post):

        sum = 0.0
        if post.post_id in self.users[user_id].interactions:
            sum += self.users[user_id].interactions[post.post_id]
        else:
            if (user_id, post.post_id) in self.shares:
                sum += self.get_interaction_weight("shares") - self.get_decay_factor(
                    current_time - self.shares[(user_id, post.post_id)].status_shared)
            if (user_id, post.post_id) in self.reactions:
                reaction = self.reactions[(user_id, post.post_id)]
                sum += self.get_interaction_weight(reaction.type_of_reaction) - self.get_decay_factor(
                    current_time - reaction.reacted)
            if (user_id, post.post_id) in self.comments:
                for com in self.comments[(user_id, post.post_id)]:
                    sum += self.get_interaction_weight("comments") - self.get_decay_factor(
                        current_time - com.comment_published)

            self.users[user_id].interactions[post.post_id] = sum

        return sum
