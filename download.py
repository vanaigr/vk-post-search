import vk
import os
import time
from datetime import datetime

directory = 'posts'

access_token = 'ваш access token с доступом wall' # https://vkhost.github.io
owner_id = 'id группы (да, строка). Для группы -- с минусом'

if not os.path.exists(directory):
    os.makedirs(directory)

def write_file(time, id, text):
    formatted_time = datetime.fromtimestamp(time).strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(directory, f"{formatted_time}-{id}.txt")
    with open(filename, "w", encoding='utf-8') as file:
        file.write(text)

api = vk.API(access_token, v = '5.199')

count = 100
start_time = time.time()

offset = 0
while True:
    posts = api.wall.get(
        owner_id = owner_id,
        offset = offset,
        count = count
    )['items']

    for i, post in enumerate(posts):
        write_file(post['date'], post['id'], post['text'])

    cur_time = time.time()
    elapsed = '{:.3f}'.format(cur_time - start_time)
    print(f'at {offset} after {elapsed}s')

    if len(posts) != count:
        break

    offset = offset + count

print('done!')
