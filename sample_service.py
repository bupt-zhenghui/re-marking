import time
import pymongo
import utils
import random
import platform

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["redb"]
sample_col = mydb['samples']
dataset_dir = '/Users/zhenghui/Downloads/Image_Harmonization_Dataset/'
if platform.system() == 'Linux':
    dataset_dir = "/workspace/dataset/Image_Harmonization_Dataset/"

re_dic = utils.get_re_data(dataset_dir)
iou_dic = utils.get_iou_data(dataset_dir)


def get_a_sample(samples, available_index):
    n = random.randint(0, len(available_index) - 1)
    sample_id = available_index[n]
    sample = samples[sample_id]
    mask, real = sample
    refs = re_dic[mask]
    ious = iou_dic[mask]
    return {
        "sample_id": sample_id,
        "mask": mask[len(dataset_dir):],
        "real": real[len(dataset_dir):],
        "refs": refs,
        "ious": ious
    }


def get_sample_refs(samples, sample_id):
    sample = samples[sample_id]
    mask = sample[0]
    refs = re_dic[mask]
    return refs


def remove_marked_samples(available_index):
    for sample in sample_col.find():
        if sample['re'] != "" or int(time.time()) - sample['timestamp'] < 1800:
            available_index.remove(sample['sample_id'])


def create_sample(sample_id, mask_path, user_name):
    sample = {
        "sample_id": sample_id,
        "user": user_name,
        "mask_path": mask_path,
        "re": "",
        "time": utils.get_cur_time(),
        "timestamp": int(time.time())
    }
    ret = sample_col.insert_one(sample)
    return ret


def search_sample_by_id(sample_id):
    query = {"sample_id": sample_id}
    return sample_col.count_documents(query) == 1


def recheck_sample(sample_id):
    query = {"sample_id": sample_id}
    result = sample_col.find_one(query)
    return result['re'] == '' and int(time.time()) - result['timestamp'] > 1800


def update_sample(sample_id, name, prompt):
    query_dic = {"sample_id": sample_id}
    update_dic = {"$set": {"re": prompt, "user": name}}
    sample_col.update_one(query_dic, update_dic)


def backup_sample(sample_id, mask_path, name, prompt):
    info = '\t'.join([str(sample_id), mask_path, name, prompt])
    with open('./static/re.txt', 'a') as f:
        f.write(info + '\n')
    f.close()


if __name__ == '__main__':
    # tmp_dataset_dir = '/Users/zhenghui/Downloads/Image_Harmonization_Dataset'
    # samples = utils.get_sample_data(tmp_dataset_dir)
    # available_index = range(len(samples))
    # # print(len(samples))
    # # print(samples[0])
    # print(get_a_sample(samples, available_index))
    print(platform.system())
