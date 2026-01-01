'''Cosmic Core: Cosmic Databases
\n\tA library of data types and functions built to simplify database access.'''
import sqlite3
import csv
import json
__all__ = ['sqlitedb']


#___SQLite Database Class___
class sqlitedb(object):
    '''A simplified interface for interacting with SQLite databases.'''

    def __init__(self, db_name):
        if not isinstance(db_name, str):
            raise TypeError("db_name must be a string")
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        '''Context management protocol: Connect to the database on entry.'''
        self.connect()
        return self

    def __exit__(self, exception_type, exception_val, trace):
        '''Context management protocol: Disconnect from the database on exit,
        committing if no exception occurred, rolling back otherwise.'''
        if exception_type:
            self.rollback()  # Rollback if an exception occurred
        else:
            self.commit()    # Commit if everything was successful
        self.disconnect()
    
    def __str__(self):
        '''Return the object in string form.'''
        return f'SQLite Database: {self.db_name}'
    
    def __repr__(self):
        '''Return a debug-friendly string.'''
        return f'sqlitedb({self.db_name})'
    
    def __eq__(self, other):
        '''Return True if the two databases are equal, False otherwise.'''
        if self is other:
            return True
        if type(self) != type(other):
            return False
        #Simple equality check is that the db names are the same.
        return self.db_name == other.db_name

    def connect(self):
        '''Establish a connection to the SQLite database.'''
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            raise e
        
    def disconnect(self):
        '''Close the SQLite database connection.'''
        try:
            if self.cursor:
                self.cursor.close()  # Close the cursor first
            if self.connection:
                self.connection.close()
                self.connection = None #Avoid double-closing
                self.cursor = None
        except sqlite3.Error as e:
            print(f'Error during disconnection: {e}')

    def query(self, query, params = None):
        '''Execute a SQL query on the database.'''
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                if 'where' in query.lower() or 'values' in query.lower():
                    raise ValueError('queries with WHERE or VALUES must have parameters to avoid SQL injection')
                self.cursor.execute(query)
                
            return self.cursor
        except sqlite3.Error as e:
            raise e

    def fetchall(self):
        '''Fetch all results from a SQL query into a Python list.
        \nPrecondition: A query has already been executed.'''
        try:
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise e

    def fetchone(self):
        '''Fetch the first result from a SQL query.
        \nPrecondition: A query has already been executed.'''
        try:
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            raise e
        
    def insert(self, table_name, data):
        '''Insert data into a SQL table.
        \nPrecondition: data is a dictionary where keys are column names
        and values are the values to insert.'''
        if not isinstance(table_name, str):
            raise TypeError('table_name must be a string')
        if not isinstance(data, dict):
            raise TypeError('data must be a dictionary')

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        values = tuple(data.values())

        self.query(query, values)

    def update(self, table_name, data, where_clause, where_params):
        '''Update data in a SQL table.
        \nPrecondition: data is a dictionary where keys are column names
        and values are the values to update. where_clause is a string specifying
        the WHERE condition.'''
        if not isinstance(table_name, str):
            raise TypeError('table_name must be a string')
        if not isinstance(data, dict):
            raise TypeError('data must be a dictionary')
        if not isinstance(where_clause, str):
            raise TypeError('where_clause must be a string')
        if not isinstance(where_params, tuple):
            raise TypeError('where_params must be a tuple')

        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        values = tuple(data.values()) + where_params

        self.query(query, values)

    def delete(self, table_name, where_clause, where_params):
        '''Delete data from a SQL table.
        \nPrecondition: where_clause is a string specifying the WHERE condition.
        where_params is a tuple of parameters for the where clause'''
        if not isinstance(table_name, str):
            raise TypeError('table_name must be a string')
        if not isinstance(where_clause, str):
            raise TypeError('where_clause must be a string')
        if not isinstance(where_params, tuple):
            raise TypeError('where_params must be a tuple')

        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        self.query(query, where_params)

    def commit(self):
        '''Commit changes to the SQL database.'''
        try:
            if self.connection:
                self.connection.commit()
        except sqlite3.Error as e:
            raise e

    def rollback(self):
        '''Roll back changes to the SQL database.'''
        try:
            if self.connection:
                self.connection.rollback()
        except sqlite3.Error as e:
            raise e
        
    def importcsv(self, table_name, csv_file):
        '''Import data from a CSV file into a SQL table.
        \nPrecondition: table_name is the name of the table to import into,
        and csv_file is the path to the CSV file.'''
        if not isinstance(table_name, str):
            raise TypeError('table_name must be a string')
        if not isinstance(csv_file, str):
            raise TypeError('csv_file must be a string')

        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.insert(table_name, row)

    def exportcsv(self, table_name, csv_file):
        '''Export data from a SQL table to a CSV file.
        \nPrecondition: table_name is the name of the table to export from,
        and csv_file is the path to the CSV file.'''
        if not isinstance(table_name, str):
            raise TypeError('table_name must be a string')
        if not isinstance(csv_file, str):
            raise TypeError('csv_file must be a string')

        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            cursor = self.query(f"SELECT * FROM {table_name}")
            columns = [description[0] for description in cursor.description]
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            for row in cursor.fetchall():
                writer.writerow(dict(zip(columns, row)))

    def importjson(self, table_name, json_file):
        '''Import data from a JSON file into a SQL table.
        \nPrecondition: table_name is the name of the table to import into,
        and json_file is the path to the JSON file.'''
        if not isinstance(table_name, str):
            raise TypeError('table_name must be a string')
        if not isinstance(json_file, str):
            raise TypeError('json_file must be a string')

        with open(json_file, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError('JSON file must contain a list of objects')
            for row in data:
                self.insert(table_name, row)

    def exportjson(self, table_name, json_file):
        '''Export data from a SQL table to a JSON file.
        \nPrecondition: table_name is the name of the table to export from,
        and json_file is the path to the JSON file.'''
        if not isinstance(table_name, str):
            raise TypeError('table_name must be a string')
        if not isinstance(json_file, str):
            raise TypeError('json_file must be a string')

        cursor = self.query(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)