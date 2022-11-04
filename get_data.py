import csv
import vk_api

def auth_handler():
    code = input('Code: ')
    return code, 1

def captcha_handler(captcha):
    print(captcha.get_url())
    answer = input('Captcha answer: ')
    captcha.try_again(answer)

session = vk_api.VkApi('login', 'password', auth_handler=auth_handler, captcha_handler=captcha_handler)
session.auth()
vk = session.get_api()

def get_data():
    rpl_comments = []
    apl_comments = []
    rpl_posts = vk.wall.get(owner_id='-51812607', domain='rpl', count=100)['items']
    for post in rpl_posts:
        comments = vk.wall.getComments(owner_id='-51812607', post_id=post['id'], count=100)['items']
        for comment in comments:
            rpl_comments.append(comment['text'])
    apl_posts = vk.wall.get(owner_id='-39803480', domain='uefa_fans', count=100)['items']
    for post in apl_posts:
        comments = vk.wall.getComments(owner_id='-39803480', post_id=post['id'], count=100)['items']
        for comment in comments:
            apl_comments.append(comment['text'])
    with open('rpl_comments.csv', mode='w', encoding="utf-8") as rpl_data:
        writer = csv.writer(rpl_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['comment', 'mark'])
        for comment in rpl_comments:
            writer.writerow([comment, 1])
    with open('apl_comments.csv', mode='w', encoding="utf-8") as apl_data:
        writer = csv.writer(apl_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(['comment', 'mark'])
        for comment in apl_comments:
            writer.writerow([comment, 1])
    # with open('check_apl_comments.txt', mode='w', encoding="utf-8") as apl_data:
    #     for comment in apl_comments:
    #         apl_data.write('"' + comment + '",\n')

get_data()
