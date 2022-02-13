"""
Script to return recipes based on keyword

1. get keyword
2. search db for keyword (lowercase based on title only)
3.  if result from 2 >= 1
4-1. display results (display all and add scroll if necessary)
-> research how to add scroll
4-2. give error message if no result.
5. Leave input on for further searches
"""




import os
import sqlite3
import webbrowser

import yaml
file_dir = os.path.abspath(os.path.dirname(__file__))
configs = yaml.safe_load(open(os.path.join(file_dir, 'config.yml')))

def query_db(keyword):
    # create new connection
    conn = sqlite3.connect(os.path.join(file_dir,configs['TABLE_SCHEMA']))
    cursor = conn.cursor()

    # read sql script based on configs
    q = open(os.path.join(file_dir, f'sql/retrieve_recipes_search.sql')).read()

    # retrieve results
    results = cursor.execute(q.format(TABLE_NAME=configs['TABLE_NAME'],
                                      KEYWORD=keyword.lower(),
                                      RETRIEVE_NUM=configs['RETRIEVE_N'])).fetchall()
    return results


def main():
    # get user response to return link
    user_input = input("Enter keyword to search in the database: ")

    # query db
    print(f"Searching db with keyword: '{user_input.lower()}'")
    results = query_db(user_input)

    if len(results) == 0:
        print(f"No results given for keyword '{user_input.lower()}'.")
    else:
        print(f"Total of {len(results)} results given for keyword '{user_input.lower()}'")
        for i, recipe in enumerate(results):
            print(f"Recipe {i}: {recipe[1]} from <{recipe[0]}>")

            # get user response to return link
        user_input = input("Enter one of the numbers above to open url: ")
        if int(user_input) in list(range(len(results))):
            webbrowser.open_new_tab(results[int(user_input)][2])




# # create window
# window = tk.Tk()
# window.title("RRR - Random Recipe Recommendation")
#
# # frame to contain random recipes
# frm_recipes = tk.Frame(master=window)
# frm_recipes.grid(row=1,column=0)


if __name__ == '__main__':
    main()