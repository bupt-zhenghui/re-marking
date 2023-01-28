import pymongo
import argparse

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["redb"]
user_col = mydb['users']


def create_user(name, account="10000"):
    if user_col.count_documents({"name": name}) == 1:
        print(f'user {name} repeated...')
        return None
    user = {
        "name": name,
        "count": 0,
        "mark_count": 0,
        "none_count": 0,
        "bank_account": account
    }
    ret = user_col.insert_one(user)
    print(f'Create a new user {name} successfully...')
    return ret


def search_user_by_name(name):
    return user_col.count_documents({"name": name}) == 1


def search_user_count(name):
    query = {"name": name}
    result = user_col.find_one(query)
    return result['count']


def update_user_count(name):
    query_dic = {"name": name}
    update_dic = {"$inc": {"count": 1}}
    user_col.update_one(query_dic, update_dic)


def update_user_none_count(name):
    query_dic = {"name": name}
    update_dic = {"$inc": {"none_count": 1}}
    user_col.update_one(query_dic, update_dic)


def update_user_mark_count(name):
    query_dic = {"name": name}
    update_dic = {"$inc": {"mark_count": 1}}
    user_col.update_one(query_dic, update_dic)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True)

    args = parser.parse_args()
    create_user(args.name)
