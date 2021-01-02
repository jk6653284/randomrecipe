"""
Idea: upon running, retrieve n random recipes (where n is specified in the config.yml)
Later, I will create another table that lists whether or nothe recipe has been tried or not, what my verdict was
The randomness then will be based on not total randomness, but based on tries and non-tries

"""
import os
import sqlite3
import webbrowser

import yaml
file_dir = os.path.dirname(__file__)
configs = yaml.safe_load(open(os.path.join(file_dir, 'config.yml')))


def main():
    # create new connection
    conn = sqlite3.connect(configs['TABLE_SCHEMA'])
    cursor = conn.cursor()

    # read sql script based on configs
    file_name = f'retrieve_recipes_{configs["RANDOMNESS"]}.sql'
    q = open(os.path.join(file_dir, f'sql/{file_name}')).read()

    # retrieve results
    results = cursor.execute(q.format(TABLE_NAME = configs['TABLE_NAME'],
                                      RETRIEVE_NUM = configs['RETRIEVE_N'])).fetchall()

    for i, recipe in enumerate(results):
        print(f"Recipe {i}: {recipe[1]} from <{recipe[0]}>")

    # get user response to return link
    user_input = input("Enter one of the numbers above to open url: ")

    if int(user_input) in list(range(len(results))):
        webbrowser.open_new_tab(results[int(user_input)][2])


if __name__ == '__main__':
    main()