
from datetime import datetime
from load_datas import load_data
from edge_rank import EdgeRank
from serilization import *

if __name__ == "__main__":

    # edge_rank = EdgeRank()
    # load_data(edge_rank,"dataset/friends.csv","dataset/statuses.csv", "dataset/shares.csv", "dataset/comments.csv",
    #                     "dataset/reactions.csv")
    #
    # t = datetime.now()
    # edge_rank.makeGraph()
    # print(datetime.now() - t)
    #
    # serilize_data(edge_rank)

    edge_rank = deserilize_data()

    load_data(edge_rank,"","dataset/test_statuses.csv","dataset/test_shares.csv","dataset/test_comments.csv","dataset/test_reactions.csv")
    edge_rank.makeGraph()

    user = ""
    print("-------------------------------")

    while 1:
        user = input("Unesite vase ime: ")

        if user in [a for a in edge_rank.users.keys()]:
            break

    while 1:

        print("-------------------------------")
        print("    1. Pregled objava")
        print("    2. Pretraga")
        print("    3. Exit")

        option = "1"
        while 1:
            option = input("Izaberite opciju: ")
            if option in ["1","2","3"]:
                break

        print("-------------------------------")
        if option == "3":
            break
        if option == "1":
            results = edge_rank.top10_posts(user)
            for post in results:
                print("\nPost: " + post.content + "\n")

        if option == "2":
            text = input("Pretraga: ").strip()

            if text[len(text)-1] == "*":
                results = edge_rank.trie.autocomplete(text[:len(text)-1])
                print("\n")
                for a in results:
                    print(a + " ")
            
            elif (text[0] == '"' and text[len(text)-1] == '"') or (text[0] == "'" and text[len(text)-1] == "'"):
                results = edge_rank.rank_posts(user, text[1:len(text)-1])
                for a in results:
                    print("Phrase: " + a.content)
            else:
                results = edge_rank.search_posts(text,user)
                for post in results:
                    print("\nPost: " + post.content + "\n")
