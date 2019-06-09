import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared
from mysql.connector import Error


class DatabaseManager(object):
    """
    class that helps to connect to msql server and fetch records
    """

    def __init__(self, config):
        """
        constructor
        :param config: dictionary with hostname, database name, port, user, password
        """
        self.config = config
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        set connection to db
        :return: None
        """
        print("\nConnecting to {} Database".format(self.config['DATABASE']))
        try:
            self.connection = mysql.connector.connect(
                host=self.config['HOST'],
                database=self.config['DATABASE'],
                port=self.config['PORT'],
                user=self.config['USER'],
                password=self.config['PASSWORD'],
                use_pure=True
            )
        except Error as err:
            print(str(err))
            raise err
        else:
            self.cursor = self.connection.cursor(cursor_class=MySQLCursorPrepared)
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        close connection
        :param exc_type: exception type
        :param exc_val: exception value
        :param exc_tb: traceback
        :return: None
        """
        print("\nClosing connection to {} Database".format(self.config['DATABASE']))
        self.connection.close()

    def execute_query(self, query, input=None):
        """
        :param self:
        :param query: string -> query to execute
        :return: records
        """
        print("\nFetching records with the following query: \n{query} \n{input}".format(query=query, input=input))

        if input == None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, input)

        records = self.cursor.fetchall()

        return records

    def update(self):
        #self.connection.commit()
        pass