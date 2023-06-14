import asyncio
from pyrogram import Client
import datetime
import parse_chatgpt as gpt
import json

# api_id = ########
# api_hash = '################################'
phone = '+###########'
chat_id = -1001071195907

# при первом запуске кода в переменной app создаем новую сессию my_account в telegram,
# которую будет использовать для работы код
# app = Client("my_account", api_id=api_id, api_hash=api_hash)
# после создания сессия продолжает использоваться повторно с помощью переменной app
app = Client("my_account")


# функция, которая возвращает обрезанный заголовок текста
def get_headline(content):
    if content is None:
        return content
    headline = content.split('\n\n')
    return headline[0]


# функция, которая считает и возвращает количество слов в тексте
# (в т.ч. это может быть заголовок)
def count_words(content):
    if content is None:
        return 0
    arr = content.split(' ')
    return len(arr)


# функция, возвращающая переменную времени в формате HH:MM:SS
def get_time(content):
    return content.strftime('%H:%M:%S')


# функция, подсчитывающая количество хэштегов в посте
def count_tags(content):
    count = 0
    for symbol in content:
        if symbol == "#":
            count += 1
    return count


# основная функция, отвечающая за парсинг постов
# функция ничего не возвращает, но записывает собранные данные
# в файл в формате json
async def parse():
    result = []

    # переменная для подсчета количества медиа в посте
    count = 0

    # переменная, позволяющая задать количество постов, которые необходимо обработать
    limit = 1000

    # две переменные ниже используются для отслеживания прогресса обработки постов
    loading1 = 100 / limit
    loading = loading1

    # запускаем сессию
    await app.start()

    # цикл ниже обрабатывает каждый полученный пост в диапазоне
    # от последнего (новейшего) поста до поста с номером limit.
    # так как в telegram каждое медиа считается за отдельный пост, мы проверяем,
    # что именно есть у поста, caption (текст поста с медиа) или text (текст поста без медиа),
    # и записываем полученный текст в соответствующую переменную text.
    # далее, так как caption в качестве текста поста относится только к первому медиа в посте,
    # мы не записываем данные об остальных медиа, но подсчитываем их в переменной count
    async for message in app.get_chat_history(chat_id, limit=limit):
        one_message = {}
        text = ""

        if message.text is not None:
            text = message.text

        elif message.caption is not None:
            text = message.caption
            count += 1

        else:
            count += 1

        if message.text is not None or message.caption is not None:
            # получаем ключевые слова заголовка и текста с помощью chatgpt
            hl_gpt = gpt.cgpt(get_headline(text))
            text_gpt = gpt.cgpt(text)

            # добавляем в словарь все интересующие нас данные
            one_message['headline'] = get_headline(text)
            one_message['text'] = text
            one_message['views'] = message.views
            one_message['headline_words'] = count_words(get_headline(text))
            one_message['text_words'] = count_words(text)
            one_message['hl_keywords'] = hl_gpt
            one_message['text_keywords'] = text_gpt
            one_message['time'] = get_time(message.date)
            one_message['media_amount'] = count
            one_message['tags_amount'] = count_tags(text)

            # добавляем в массив постов словарь текущего обрабатываемого поста с собранными данными
            result.append(one_message)

            count = 0
            if loading < 100:
                print(round(loading, 2), "%", sep='')

        loading += loading1

    # останавливаем сессию
    await app.stop()

    print('100%')
    print('Done')

    # записываем результат в файл в формате json
    with open('json.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(result, ensure_ascii=False, indent=2))

app.run(parse())
