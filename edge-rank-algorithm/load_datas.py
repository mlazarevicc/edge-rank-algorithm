def load_Users(self, path):
    with open(path) as file:
        lines = file.readlines()
        for line in lines[1:]:
            datas = line.strip().split(",")
            self.add_user(datas[0], [item for item in datas[2:]])

def load_shares(self, path):
    with open(path) as file:
        lines = file.readlines()
        for line in lines[1:]:
            a = line.strip().split(",")
            self.add_share(a[0], a[1], a[2])

def load_reactions(self, path):
    with open(path) as file:
        lines = file.readlines()
        for line in lines[1:]:
            a = line.strip().split(",")
            self.add_reactions(a[0], a[1], a[2], a[3])


def load_Posts(self, path):
    with open(path) as file:
        lines = file.readlines()
        comment = ""
        paired_ellipses = True

        for index in range(1, len(lines)):
            line = lines[index]

            if line == "\n":
                comment += line
                continue

            # if line[-1] == "\n":
            #     line = line[:-1]
            line = line.strip()

            previous_index = -1

            while True:
                index = line.index("\"", previous_index + 1) if "\"" in line[previous_index + 1:] else -1
                if index == -1:
                    break
                paired_ellipses = not paired_ellipses
                previous_index = index

            comment += line
            if not paired_ellipses:
                continue

            data = comment.split(",")
            n = len(data)

            if n < 16:
                raise Exception("Status does not contain necessary data.")
            elif n > 16:
                comment_text = "".join(data[1:n - 14])
                
            else:
                comment_text = data[1]
                n -= 1

            self.add_post(data[0], comment_text, data[n - 14], data[n - 13], data[n - 12], data[n - 11],
                          data[n - 10], data[n - 9], data[n - 8], data[n - 7], data[n - 6], data[n - 5], data[n - 4],
                          data[n - 3], data[n - 2], data[n - 1])
            comment = ""
            paired_ellipses = True


def load_comments(self, path):
    output_data = []
    with open(path) as file:
        lines = file.readlines()
        comment = ""
        found_open_ellipsis = False
        found_close_ellipsis = False

        for index in range(1, len(lines)):

            line = lines[index]

            if line == "\n":
                comment += line

            if line[-1] == "\n":
                line = line[:-1]

            first_index = line.index("\"") if "\"" in line else -1
            if first_index > -1:
                found_open_ellipsis = True

            next_index = line.index("\"", first_index + 1) if "\"" in line[first_index + 1:] else -1
            if next_index > -1:
                found_close_ellipsis = True

            if found_open_ellipsis and not found_close_ellipsis:
                comment += line
                continue
            else:
                comment = line

            data = comment.split(",")
            n = len(data)

            if n < 14:
                raise Exception("Comment does not contain necessary data.")
            elif n > 14:
                comment_text = "".join(data[3:n - 10])
            else:
                comment_text = data[3]

            self.add_comment(data[0], data[1], data[2], comment_text, data[n - 10], data[n - 9], data[n - 8],
                             data[n - 7],
                             data[n - 6], data[n - 5], data[n - 4], data[n - 3], data[n - 2], data[n - 1])

            found_open_ellipsis = found_close_ellipsis = False
            comment = ""
    return output_data

def load_data(edge_rank, path1, path2, path3, path4, path5):
    #load_Users(edge_rank,path1)
    load_Posts(edge_rank,path2)
    load_shares(edge_rank,path3)
    load_comments(edge_rank,path4)
    load_reactions(edge_rank,path5)