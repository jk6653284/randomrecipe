"""
This file creates the database to store the data.
This should only be ran once.
"""
import sqlite3
import os
import yaml

def main():
    path = os.path.abspath(os.path.dirname(__file__))
    configs = yaml.safe_load(open(os.path.join(path,'config.yml')))
    table_schema = os.path.join(path,configs['TABLE_SCHEMA'])
    table_name = configs['TABLE_NAME']

    # create connection and cursor
    conn = sqlite3.connect(table_schema)
    cursor = conn.cursor()

    # create table
    create_table_q = f"""
        CREATE TABLE {table_name} (
            website_name text NOT NULL
            ,recipe_name text NOT NULL
            ,recipe_url text NOT NULL
        )
        """
    cursor.execute(create_table_q)

    # create unique index
    create_uniqueindex_q = f"""
        CREATE UNIQUE INDEX recipes_index on {table_name} (website_name,recipe_name)
        """
    cursor.execute(create_uniqueindex_q)

    # commit and close connection
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
