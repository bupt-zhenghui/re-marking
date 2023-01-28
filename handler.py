import user_service
import sample_service
import utils
import platform

dataset_dir = '/Users/zhenghui/Downloads/Image_Harmonization_Dataset'
if platform.system() == 'Linux':
    dataset_dir = '/workspace/dataset/Image_Harmonization_Dataset'
samples = utils.get_sample_data(dataset_dir)
available_index = [i for i in range(len(samples))]
sample_service.remove_marked_samples(available_index)
print(f'totally {len(samples)} samples, {len(available_index)} samples remaining...')
choice_dic = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3
}


def validation_handler(name):
    return user_service.search_user_by_name(name)


def sample_handler(user_name):
    sample = sample_service.get_a_sample(samples, available_index)
    user_count = user_service.search_user_count(user_name)
    available_count = len(available_index)
    sample_service.create_sample(sample['sample_id'], sample['mask'], user_name)
    return {
        "data": {
            "sample": sample,
            "user_count": user_count,
            "remain": available_count
        }
    }


def update_handler(user_name, sample_id, form):
    info = form.split('&')
    refs = sample_service.get_sample_refs(samples, sample_id)
    re_list = []
    for i in range(len(info) - 1):
        key = info[i][-1]
        re_list.append(refs[choice_dic[key]])

    mark = info[-1][3:].strip().replace("%20", " ")
    if mark:
        if mark == 'none': user_service.update_user_none_count(user_name)
        else: user_service.update_user_mark_count(user_name)
        re_list.append(mark)
    referring = ';'.join(re_list)
    print('referring: ', referring)

    user_service.update_user_count(user_name)
    sample_service.update_sample(sample_id, user_name, referring)

    mask_path = samples[sample_id][0]
    sample_service.backup_sample(sample_id, mask_path, user_name, referring)

    available_index.remove(sample_id)


if __name__ == '__main__':
    sample_service.update_sample(40600, "test_user", 'baby in green')
