import urllib3
import requests


class User:

    def __init__(self, token, source_uid):
        self.token = token
        self.source_uid = source_uid
        params = {'access_token': token,
                  'user_ids': source_uid,
                  'fields': 'domain',
                  'v': '5.85'}
        response = requests.get('https://api.vk.com/method/users.get', params, verify=False)
        inf_list = response.json()['response']
        inf = inf_list[0]
        self.name = inf["first_name"]
        self.page = "https://vk.com/" + inf['domain']

    def print(self):
         print(self.page)


    def mutual_friends_list(self, target_uids):
        params = {'access_token': self.token,
                  'source_uid': self.source_uid,
                  'target_uids': target_uids,
                  'v': '5.85'}
        response = requests.get('https://api.vk.com/method/friends.getMutual', params, verify=False)
        friends_list = []
        for mutual_friend_info in response.json()['response']:
            friends_list.append(set(mutual_friend_info['common_friends']))
        common_friends_list = friends_list[0]
        for friends in friends_list[1:]:
            common_friends_list &= friends
        return list(common_friends_list)


    def get_mutual_friends(self, target_uids):
        friends_list = self.mutual_friends_list(target_uids)
        mutual_friends_list = []
        for friend_id in friends_list:
            mutual_friends_list.append(User(self.token, friend_id))
        print(mutual_friends_list)


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    TOKEN = ""
    source_uid = int(input('Введите идентификатор текущего пользователя: '))
    target_uids_str = input('Введите идентификаторы пользователей через запятую, с которыми необходимо искать общих друзей: ').split(',')
    target_uids = list(map(int, target_uids_str))
    usr = User(TOKEN, source_uid)
    usr.get_mutual_friends(target_uids)
    usr.print()

# 7613322, 16589338, 207791551
