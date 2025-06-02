import pymysql
import re

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
        tuple: (conn, cursor, status)
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
        return conn, cursor, True
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None, None, False

def apply_query_sql(query: str, is_read: bool = True):
    """
    Executes a safe SQL query (no DML) on a MySQL database.

    Returns:
        tuple: (result or None, flag string, error or None)
    """

    conn, cursor, connectedFlag = connect_to_mysql()
    if not connectedFlag:
        return None, 'Error', None

    try:
        cursor.execute(query)

        if is_read:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in rows]
            return result, 'Data', None
        else:
            conn.commit()
            return None, 'No Data', None

    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return None, 'Error', str(e)

    finally:
        cursor.close()
        conn.close()
