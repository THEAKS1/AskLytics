import pymysql

from config import *
from prompts import system_initial_prompt

class Conversation:
    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": system_initial_prompt,
            }
        ]

def get_or_create_conversation(conversation_id, all_conversations):
    """
    Retrieves an existing conversation by its ID or creates a new one if it doesn't exist.

    Parameters:
        conversation_id (str): The unique identifier for the conversation.
        all_conversations (dict): A dictionary mapping conversation IDs to Conversation objects.

    Returns:
        Conversation: The existing or newly created Conversation object associated with the given ID.
    """

    if conversation_id not in all_conversations:
        all_conversations[conversation_id] = Conversation()
    
    return all_conversations[conversation_id]

def connect_to_mysql():
    """
    Establishes a connection to a MySQL database using PyMySQL.

    Returns:
        tuple:
            - cursor (pymysql.cursors.Cursor or None): A cursor object for executing MySQL queries if the connection is successful, otherwise None.
            - status (bool): True if the connection is successful, False otherwise.

    Side Effects:
        Prints an error message to the console if the connection fails.

    Notes:
        - The function connects to a MySQL database named 'ecommerce' on 'localhost' 
          using the 'root' user with password 'root'.
        - Autocommit is enabled for the connection.
    """
    try:
        conn = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            autocommit=True
    )
        cursor = conn.cursor()
        return cursor, True
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None, False

def apply_query_sql(query: str, is_read: bool = True):
    """
    Executes a SQL query on a MySQL database and returns the result in JSON-like format.

    Parameters:
        query (str): The SQL query to be executed.
        is_read (bool, optional): Specifies whether the query is a read operation (e.g., SELECT). 
                                  Set to False for write operations (e.g., INSERT, UPDATE, DELETE). 
                                  Defaults to True.

    Returns:
        list[dict] or None: 
            - If is_read is True, returns a list of dictionaries where each dictionary represents a row 
              with column names as keys and row values as values.
            - If is_read is False, commits the transaction and returns None.

    Raises:
        pymysql.MySQLError: If an error occurs while connecting to the database or executing the query.
    """
    try:
        cursor, connectedFlag = connect_to_mysql()
        if not connectedFlag:
            print("Failed to connect to the database.")
            return None, 'Error', None

        cursor.execute(query)

        if is_read:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in rows]
            return result, 'Data', None
        else:
            cursor.connection.commit()
            return None, 'No Data', None

    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None, 'Error', e

