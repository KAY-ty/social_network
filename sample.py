import pickle
import pandas as pd
import json
import csv
from tqdm import tqdm

def city():
    cites = {}
    with open('data/business.json', 'r') as f:
        reader = json.load(f)
        print(type(reader))
        for row in reader:
            city = row['city']
            if cites.__contains__(city):
                cites[city] = cites[city]+1
            else:
                cites[city] = 1

        max = -1
        city = ''
        for key in cites.keys():
            if cites[key] > max:
                max = cites[key]
                city = key

        print(max)
        print(city)
        return city

def create_pickle_include_test(city):
    business = set()
    users = set()
    b2i={}
    u2i={}
    idx=0
    with open('data/business.json', 'r') as f:
        reader = json.load(f)
        for row in reader:
            if row['city'] == city :
                if row['business_id'] not in business:
                    b2i[row['business_id']] = idx
                    idx += 1
                business.add(row['business_id'])



    # with open('data/yelp_academic_dataset_review.csv', 'r') as f:
    reader = pd.read_csv('data/yelp_academic_dataset_review.csv')
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
    idx=0
    for row in tqdm(reader.iterrows()):
        i = i + 1
        user_id = row[1]['user_id']
        business_id = row[1]['business_id']
        star = row[1]['stars']
        if isinstance(user_id, bytes):
            user_id = user_id.decode('utf-8')
        if isinstance(business_id, bytes):
            business_id = business_id.decode('utf-8')
        if isinstance(star, bytes):
            star = star.decode('utf-8')
        star = float(star)
        if business.__contains__(business_id):
            if user_id not in users:
                u2i[user_id] = idx
                idx += 1
            users.add(user_id)

            if cnt >= 10 and history_u_lists.__contains__(u2i[user_id]) and history_v_lists.__contains__(b2i[business_id]):
                cnt = 0
                test_u.append(u2i[user_id])
                test_v.append(b2i[business_id])
                test_r.append(star)
            else:
                if user_id == 'user_id':
                    continue
                if history_u_lists.__contains__(u2i[user_id]):
                    temp = history_u_lists[u2i[user_id]]
                    temp.append(b2i[business_id])
                    history_u_lists[u2i[user_id]] = temp

                    temp = history_ur_lists[u2i[user_id]]
                    temp.append(star)
                    history_ur_lists[u2i[user_id]] = temp
                else:
                    history_u_lists[u2i[user_id]] = [b2i[business_id]]
                    history_ur_lists[u2i[user_id]] = [star]

                if history_v_lists.__contains__(b2i[business_id]):
                    temp = history_v_lists[b2i[business_id]]
                    temp.append(u2i[user_id])
                    history_v_lists[b2i[business_id]] = temp

                    temp = history_vr_lists[b2i[business_id]]
                    temp.append(star)
                    history_vr_lists[b2i[business_id]] = temp
                else:
                    history_v_lists[b2i[business_id]] = [u2i[user_id]]
                    history_vr_lists[b2i[business_id]] = [star]

                train_u.append(u2i[user_id])
                train_v.append(b2i[business_id])
                train_r.append(star)
                cnt = cnt + 1



    df = pd.read_csv('data/yelp_academic_dataset_user.csv', usecols=['user_id','friends'])
    social_adj_lists = {}
    # i = 0
    # for row in tqdm(df.iterrows()):
    #     id = row[1]['user_id']
    #     friends = row[1]['friends']
    #     # print("user"+str(i))
    #     i = i+1
    #     if id in u2i:
    #         friends = friends.split(', ')
    #         fri=[]
    #         for f in friends:
    #             if f in u2i:
    #                 fri.append(u2i[f])
    #         social_adj_lists[u2i[id]] = fri
    #
    # with open('data/social_list.pickle', 'wb') as f:
    #     a = [social_adj_lists]
    #     pickle.dump(a, f)

    with open('data/history_u.pickle', 'wb') as f:
        a = [history_u_lists, history_ur_lists]
        pickle.dump(a, f)
    with open('data/history_v.pickle', 'wb') as f:
        a = [history_v_lists, history_vr_lists]
        pickle.dump(a, f)
    with open('data/train.pickle', 'wb') as f:
        a = [train_u, train_v, train_r]
        pickle.dump(a, f)
    with open('data/test.pickle', 'wb') as f:
        a = [test_u, test_v, test_r]
        pickle.dump(a, f)

    with open('data/uv2i.pickle','wb') as f:
        pickle.dump([u2i,b2i],f)


    print(len(business))
    print(len(users))


if __name__ == '__main__':
    create_pickle_include_test(city())
    # with open('data/social_list.pickle', 'rb') as f:
    #     [social_list] = pickle.load(f)
    #
    # with open('data/history_u.pickle', 'rb') as f:
    #     reader = pickle.load(f)
    #     history_u_lists = reader[0]
    #     history_ur_lists = reader[1]
    #
    # with open('data/history_v.pickle', 'rb') as f:
    #     reader = pickle.load(f)
    #     history_v_lists = reader[0]
    #     history_vr_lists = reader[1]
    #
    # with open('data/train.pickle', 'rb') as f:
    #     [train_u, train_v, train_r] = pickle.load(f)
    #
    # with open('data/test.pickle', 'rb') as f:
    #     [test_u, test_v, test_r] = pickle.load(f)
    #
    # print(len(social_list))
    #
    # cnt = 0
    # for key in history_u_lists.keys():
    #     cnt = cnt + len(history_u_lists[key])
    # print(cnt)
    #
    # cnt = 0
    # for key in history_v_lists.keys():
    #     cnt = cnt + len(history_v_lists[key])
    # print(cnt)
    # print(len(train_u))
    # print(len(test_u))
    # for key in social_list.keys():
    #     print(type(social_list[key]))
    #
    #
    #     break
    #
    # for key in history_u_lists.keys():
    #     print(type(history_u_lists[key]))
    #     break