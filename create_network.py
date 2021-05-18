import networkx as nx
import json
import os
import csv
import time

def preprocess():
    # path = os.path.dirname(os.getcwd())+"/yelp_dataset/yelp_academic_dataset_user.json"
    # print(path)

    file = open('yelp_academic_dataset_user.txt')
    temp = open('user.txt', 'w')
    pre = "["
    for line in file.readlines():
        if(pre != ""):
            print(pre)
            temp.write(pre)
        l = list(line)
        l.append(',')
        line = ''.join(l)
        pre = line

    l = list(pre)
    l.pop()
    l.append(']')
    pre = ''.join(l)

    temp.write(pre)


    # with open("temp.json", "r", encoding='utf8') as f:
    #     user_dict = json.load(f)

def create_user_graph():
    csv.field_size_limit(500*1024*1024)
    with open('yelp_academic_dataset_user.csv', 'r') as f:
        reader = csv.reader(f)
        print(type(reader))

        user_graph = nx.Graph()
        user_dict = {'uset_id': {'name': 'user name', 'average_star': 'averange star of the user',
                         'friends_num': 'the number of friends', 'fans_num': 'the number of fans'}}

        i = 0
        for row in reader:
            friends = row[7]
            id = row[14]
            fans = row[8]
            averange_star = row[13]
            fans = row[8]
            name = row[19]
            print(i)
            i = i+1
            user_graph.add_node(id)
            user_dict[id] = {'name': name, 'average_star': averange_star,
                         'friends_num': len(friends.split(',')), 'fans_num': len(fans.split(','))}
            for friend in friends.split(','):
                user_graph.add_node(friend)
                user_graph.add_edge(id, friend)

    return user_graph, user_dict

def create_user_item_graph():
    csv.field_size_limit(500 * 1024 * 1024)
    with open('yelp_academic_dataset_review.csv', 'r') as f:
        reader = csv.reader(f)
        user_item_graph = nx.Graph()
        i = 0
        for row in reader:
            print(i)
            i = i+1
            user_id = row[7]
            business_id = row[4]
            star = row[5]
            user_item_graph.add_node(user_id)
            user_item_graph.add_node(business_id)
            user_item_graph.add_edge(user_id, business_id, weight = star)


    return user_item_graph







if __name__ == '__main__':
    t1 = time.clock()
    user_graph, user_dict = create_user_graph()
    t2 = time.clock()
    user_item_graph = create_user_item_graph()
    t3 = time.clock()
    print(t2-t1)
    print(t3-t2)
