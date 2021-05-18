import pickle
import pandas as pd
import json
import csv
def sample():
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

    cnt = 0
    for key in history_u_lists.keys():
        cnt = cnt+len(history_u_lists[key])
    print(cnt)

    cnt = 0
    for key in history_v_lists.keys():
        cnt = cnt+len(history_v_lists[key])
    print(cnt)
    print(len(train_u))

    test_u = []
    test_v = []
    test_r = []
    for user_id in history_u_lists.keys():
        n = len(history_u_lists[user_id])
        if(n >= 4):
            i = n-1
            business_ids = history_u_lists[user_id]
            u_b_stars = history_ur_lists[user_id]
            while i >= 0:
                del_b_id = business_ids[i]
                del_u_b_star = u_b_stars[i]
                user_ids = history_v_lists[del_b_id]
                b_u_stars = history_vr_lists[del_b_id]
                for j in range(0, len(user_ids)):
                    if(user_ids[j] == user_id and b_u_stars[j] == del_u_b_star):
                        del business_ids[i]
                        del u_b_stars[i]
                        del user_ids[j]
                        del b_u_stars[j]
                        test_u.append(user_id)
                        test_v.append(del_b_id)
                        test_r.append(del_u_b_star)
                        break

                history_v_lists[del_b_id] = user_ids
                history_vr_lists[del_b_id] = b_u_stars

                i = i-4
            history_u_lists[user_id] = business_ids
            history_ur_lists[user_id] = u_b_stars

    print(len)

def city():
    cites = {}
    with open('business.json', 'r') as f:
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
    with open('business.json', 'r') as f:
        reader = json.load(f)
        for row in reader:
            if row['city'] == city :
                business.add(row['business_id'])


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
            print("review" + str(i))
            i = i + 1
            user_id = row[7]
            business_id = row[4]
            star = row[5]
            if business.__contains__(business_id):
                users.add(user_id)
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
                    cnt = cnt + 1



    df = pd.read_csv('yelp_academic_dataset_user.csv', usecols=[7, 14])
    social_adj_lists = {}
    i = 0
    for row in df.iterrows():
        id = row[1]['user_id']
        friends = row[1]['friends']
        print("user"+str(i))
        i = i+1
        if users.__contains__(id):
            friends = friends.split(', ')
            for f in friends:
                if users.__contains__(f):
                    continue
                else:
                    friends.remove(f)
            social_adj_lists[id] = friends
    #         social_adj_lists[id] = friends

    # bytes_out = pickle.dumps(social_adj_lists)
    # max_bytes = 2 ** 31 - 1
    # with open('social_list.pickle', 'wb') as f_out:
    #     for idx in range(0, len(bytes_out), max_bytes):
    #         f_out.write(bytes_out[idx:idx + max_bytes])

    with open('social_list.pickle', 'wb') as f:
        a = [social_adj_lists]
        pickle.dump(a, f)

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

    print(len(business))
    print(len(users))





if __name__ == '__main__':
    # sample()
    # df = pd.read_csv('yelp_academic_dataset_user.csv', usecols=[7,14])
    # i = 0
    # for row in df.iterrows():
    #     print(row[1]['friends'])
    create_pickle_include_test(city())
    with open('social_list.pickle', 'rb') as f:
        [social_list] = pickle.load(f)

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

