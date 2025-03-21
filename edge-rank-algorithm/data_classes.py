class User:
    def __init__(self, user_id, friends):
        self.user_id = user_id
        self.friends = friends
        self.interactions = {}


class Comment:
    def __init__(self, comment_id, status_id, parent_id, comment_message, comment_author, comment_published,
                 num_reactions, num_likes, num_loves, num_wows, num_hahas, num_sads, num_angrys, num_special):
        self.comment_id = comment_id
        self.status_id = status_id
        self.parent_id = parent_id
        self.comment_message = comment_message
        self.comment_author = comment_author
        self.comment_published = comment_published
        self.num_reactions = num_reactions
        self.interactions = {"likes": num_likes,
                             "loves": num_loves,
                             "wows": num_wows,
                             "hahas": num_hahas,
                             "sads": num_sads,
                             "angrys": num_angrys,
                             "special": num_special}


class Post:
    def __init__(self, post_id, content, link_name, status_type, status_link, status_published, author_id,
                 num_reactions=0, num_comments=0, num_shares=0, num_likes=0, num_loves=0, num_wows=0, num_hahas=0,
                 num_sads=0, num_angrys=0, num_special=0):
        self.post_id = post_id
        self.content = content
        self.link_name = link_name
        self.status_type = status_type
        self.status_link = status_link
        self.status_published = status_published
        self.author_id = author_id
        self.num_reactions = num_reactions
        self.interactionsNum = {"comments": num_comments,
                                "shares": num_shares,
                                "likes": num_likes,
                                "loves": num_loves,
                                "wows": num_wows,
                                "hahas": num_hahas,
                                "sads": num_sads,
                                "angrys": num_angrys,
                                "special": num_special}


class Share:
    def __init__(self, status_id, sharer, status_shared):
        self.status_id = status_id
        self.sharer = sharer
        self.status_shared = status_shared


class Reaction:
    def __init__(self, status_id, type_of_reaction, reactor, reacted):
        self.type_of_reaction = type_of_reaction
        self.status_id = status_id
        self.reactor = reactor
        self.reacted = reacted