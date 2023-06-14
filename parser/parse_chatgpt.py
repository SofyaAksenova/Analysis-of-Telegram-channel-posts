#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import os
import openai
import time
openai.api_key = "##-################################################"


# функция, отправляющая chatgpt запрос для поиска в тексте ключевых слов
# (в т.ч. это может быть как заголовок, так и полный текст поста)
def cgpt(content):
    # так как у chatgpt есть ограничение об отправке не больше трех запросов в минуту,
    # код стоит в режиме ожидание 20 секунд, перед тем как отправить новый запрос
    time.sleep(20)

    # функция, которая преобразовывает ответ, полученный от chatgpt,
    # в список, состоящий из ключевых слов
    def keywords_to_list(content):
        result = content.split(", ")
        result = result[:-1]
        return result

    # конкретный запрос для chatgpt, который отправится с текстом
    req = "\nПеречисли ключевые слова данного текста через запятую."

    # переменная req с конкретным запросом прибавляется к переменной content,
    # содержащий текст, чтобы сформировать единый запрос к chatgpt
    content += req

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": content}
      ]
    )

    # переменная, содержащая ответ от chatgpt
    response = completion.choices[0].message.content

    # переменная, содержащая ответ от chatgpt в формате списка,
    # полученного из ответа, преобразованного функцией keywords_to_list()
    result = keywords_to_list(response)

    return result
