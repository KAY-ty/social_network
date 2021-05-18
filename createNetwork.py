import networkx as nx
import json
import os
import csv
import time
import pandas as pd
import pickle

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
        user_dict = {'user_id': {'name': 'user name', 'average_star': 'averange star of the user',
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

def test_pickle():
    file_name = "toy_dataset.pickle"
    with open(file_name, 'rb') as f:
        history_u_lists, history_ur_lists, history_v_lists, history_vr_lists, train_u, train_v, train_r, test_u, test_v, test_r, social_adj_lists, ratings_list = pickle.load(f)

        print(type(history_u_lists))
        cnt = 0
        for key in history_u_lists.keys():
            cnt = cnt+len(history_u_lists[key])
        print(cnt)
        print(len(train_u))
        print(len(test_v))


def create_pickle():
    csv.field_size_limit(500 * 1024 * 1024)
    with open('yelp_academic_dataset_user.csv', 'r') as f:
        social_adj_lists = {}
        reader = csv.reader(f)
        i = 0
        for row in reader:
            print("user"+str(i))
            i = i+1
            friends = row[7]
            id = row[14]
            if id == 'user_id':
                continue
            social_adj_lists[id] = friends
            # if i == 10000:
            #     break
            # break

    bytes_out = pickle.dumps(social_adj_lists)
    n_bytes = 2 ** 31
    max_bytes = 2 ** 31 - 1
    with open('social_list.pickle', 'wb') as f_out:
        for idx in range(0, len(bytes_out), max_bytes):
            f_out.write(bytes_out[idx:idx + max_bytes])
    # with open('social_list.pickle', 'wb') as f:
    #     pickle.dump(social_adj_lists, f)

    with open('yelp_academic_dataset_review.csv', 'r') as f:
        reader = csv.reader(f)
        history_u_lists = {}
        history_ur_lists = {}
        history_v_lists = {}
        history_vr_lists = {}
        train_u = []
        train_v = []
        train_r = []
        i = 0
        for row in reader:
            print("review"+str(i))
            i = i+1
            user_id = row[7]
            business_id = row[4]
            star = row[5]
            if user_id == 'user_id':
                continue
            if history_u_lists.__contains__(user_id):
                temp = history_u_lists[user_id]
                temp.append(business_id)
                history_u_lists[user_id] = temp

                temp = history_ur_lists[user_id]
                temp.append(star)
                history_ur_lists[user_id] = temp
            else:
                history_u_lists[user_id] = [business_id]
                history_ur_lists[user_id] = [star]

            if history_v_lists.__contains__(business_id):
                temp = history_v_lists[business_id]
                temp.append(user_id)
                history_v_lists[business_id] = temp
                # print(temp)

                temp = history_vr_lists[business_id]
                temp.append(star)
                history_vr_lists[business_id] = temp
            else:
                history_v_lists[business_id] = [user_id]
                history_vr_lists[business_id] = [star]

            # history_u_lists[user_id] = business_id
            # history_ur_lists[user_id] = star
            # history_v_lists[business_id] = user_id
            # history_vr_lists[business_id] = star
            train_u.append(user_id)
            train_v.append(business_id)
            train_r.append(star)
            # if i == 10000:
            #     break
            # break


    with open('history_u.pickle', 'wb') as f:
        a = [history_u_lists, history_ur_lists]
        pickle.dump(a, f)
    with open('history_v.pickle', 'wb') as f:
        a = [history_v_lists, history_vr_lists]
        pickle.dump(a, f)
    with open('train.pickle', 'wb') as f:
        a = [train_u, train_v, train_r]
        pickle.dump(a, f)

    # with open('data_set.pickle', 'rb') as f:
    #     reader = pickle.load(f)
    #     for row in reader:
    #         print(type(row))
    #         print(row)

def create_pickle_include_test():
    df = pd.read_csv('yelp_academic_dataset_user.csv', usecols=[7, 14])
    social_adj_lists = {}
    i = 0
    for row in df.iterrows():
        id = row[1]['user_id']
        friends = row[1]['friends']
        print("user"+str(i))
        i = i+1
        social_adj_lists[id] = friends.split(', ')
    # csv.field_size_limit(500 * 1024 * 1024)
    # with open('yelp_academic_dataset_user.csv', 'r') as f:
    #     social_adj_lists = {}
    #     reader = csv.reader(f)
    #     i = 0
    #     for row in reader:
    #         print("user"+str(i))
    #         i = i+1
    #         friends = row[7]
    #         id = row[14]
    #         if id == 'user_id':
    #             continue
    #         social_adj_lists[id] = friends

    bytes_out = pickle.dumps(social_adj_lists)
    n_bytes = 2 ** 31
    max_bytes = 2 ** 31 - 1
    with open('social_list.pickle', 'wb') as f_out:
        for idx in range(0, len(bytes_out), max_bytes):
            f_out.write(bytes_out[idx:idx + max_bytes])

    with open('yelp_academic_dataset_review.csv', 'r') as f:
        reader = csv.reader(f)
        history_u_lists = {}
        history_ur_lists = {}
        history_v_lists = {}
        history_vr_lists = {}
        train_u = []
        train_v = []
        train_r = []
        test_u = []
        test_v = []
        test_r = []
        i = 0
        cnt = 0
        for row in reader:
            print("review"+str(i))
            i = i+1
            user_id = row[7]
            business_id = row[4]
            star = row[5]
            if cnt >= 10 and history_u_lists.__contains__(user_id) and history_v_lists.__contains__(business_id):
                cnt = 0
                test_u.append(user_id)
                test_v.append(business_id)
                test_r.append(star)
            else:
                if user_id == 'user_id':
                    continue
                if history_u_lists.__contains__(user_id):
                    temp = history_u_lists[user_id]
                    temp.append(business_id)
                    history_u_lists[user_id] = temp

                    temp = history_ur_lists[user_id]
                    temp.append(star)
                    history_ur_lists[user_id] = temp
                else:
                    history_u_lists[user_id] = [business_id]
                    history_ur_lists[user_id] = [star]

                if history_v_lists.__contains__(business_id):
                    temp = history_v_lists[business_id]
                    temp.append(user_id)
                    history_v_lists[business_id] = temp

                    temp = history_vr_lists[business_id]
                    temp.append(star)
                    history_vr_lists[business_id] = temp
                else:
                    history_v_lists[business_id] = [user_id]
                    history_vr_lists[business_id] = [star]

                train_u.append(user_id)
                train_v.append(business_id)
                train_r.append(star)
                cnt = cnt+1


    with open('history_u.pickle', 'wb') as f:
        a = [history_u_lists, history_ur_lists]
        pickle.dump(a, f)
    with open('history_v.pickle', 'wb') as f:
        a = [history_v_lists, history_vr_lists]
        pickle.dump(a, f)
    with open('train.pickle', 'wb') as f:
        a = [train_u, train_v, train_r]
        pickle.dump(a, f)
    with open('test.pickle', 'wb') as f:
        a = [test_u, test_v, test_r]
        pickle.dump(a, f)



if __name__ == '__main__':
    # t1 = time.clock()
    # user_graph, user_dict = create_user_graph()
    # t2 = time.clock()
    # user_item_graph = create_user_item_graph()
    # t3 = time.clock()
    # print(t2-t1)
    # print(t3-t2)
    # test_pickle()
    create_pickle_include_test()
    with open('social_list.pickle', 'rb') as f:
        social_list = pickle.load(f)

    with open('history_u.pickle', 'rb') as f:
        reader = pickle.load(f)
        history_u_lists = reader[0]
        history_ur_lists = reader[1]

    with open('history_v.pickle', 'rb') as f:
        reader = pickle.load(f)
        history_v_lists = reader[0]
        history_vr_lists = reader[1]

    with open('train.pickle', 'rb') as f:
        [train_u, train_v, train_r] = pickle.load(f)

    with open('test.pickle', 'rb') as f:
        [test_u, test_v, test_r] = pickle.load(f)

    print(len(social_list))

    cnt = 0
    for key in history_u_lists.keys():
        cnt = cnt + len(history_u_lists[key])
    print(cnt)

    cnt = 0
    for key in history_v_lists.keys():
        cnt = cnt + len(history_v_lists[key])
    print(cnt)
    print(len(train_u))
    print(len(test_u))
    for key in social_list.keys():
        print(type(social_list[key]))


        break

    for key in history_u_lists.keys():
        print(type(history_u_lists[key]))
        break



