import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),          # Your database host
            user=os.getenv("MYSQL_USER"),      # Your MySQL username
            password=os.getenv("MYSQL_PASSWORD"),  # Your MySQL password
            database=os.getenv("MYSQL_DATABASE")         # Database name
        )
        
        if connection.is_connected():
            print("Successfully connected to the database!")
            return connection
            
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed.")

class UserManager:
    def __init__(self):
        self.connection = connect_to_database()
        self.cursor = self.connection.cursor(dictionary=True)

    def create_user(self, email_id, first_name, last_name):
        try:
            query = """
                INSERT INTO users (email_id, first_name, last_name)
                VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, (email_id, first_name, last_name))
            self.connection.commit()
            return email_id
        except Error as e:
            print(f"Error creating user: {e}")
            return None

    def get_user_by_email(self, email_id):
        try:
            query = "SELECT * FROM users WHERE email_id = %s"
            self.cursor.execute(query, (email_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching user: {e}")
            return None

    def get_all_users(self):
        try:
            query = "SELECT * FROM users"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching users: {e}")
            return None

    def update_user(self, email_id, first_name=None, last_name=None):
        try:
            updates = []
            values = []
            if first_name:
                updates.append("first_name = %s")
                values.append(first_name)
            if last_name:
                updates.append("last_name = %s")
                values.append(last_name)
            
            if not updates:
                return False

            values.append(email_id)
            query = f"""
                UPDATE users 
                SET {', '.join(updates)}
                WHERE email_id = %s
            """
            self.cursor.execute(query, tuple(values))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Error updating user: {e}")
            return False

    def delete_user(self, email_id):
        try:
            query = "DELETE FROM users WHERE email_id = %s"
            self.cursor.execute(query, (email_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting user: {e}")
            return False

    def execute_action(self, action_name, parameters):
        if action_name == "CREATE":
            return self.create_user(parameters["email_id"], parameters["first_name"], parameters["last_name"])
        elif action_name == "READ":
            return self.get_user_by_email(parameters["email_id"])
        elif action_name == "UPDATE":
            return self.update_user(parameters["email_id"], parameters["first_name"], parameters["last_name"])
        elif action_name == "DELETE":
            return self.delete_user(parameters["email_id"])


# Example usage
if __name__ == "__main__":
    db_connection = connect_to_database()
    
    if db_connection:
        user_manager = UserManager()
        
        # Create a new user
        new_user_id = user_manager.create_user("john_doe@example.com", "John", "Doe")
        
        # Read user
        user = user_manager.get_user_by_email("john_doe@example.com")
        print("New user:", user)
        
        # Update user
        user_manager.update_user("john_doe@example.com", first_name="John", last_name="Doe")
        
        # Delete user
        user_manager.delete_user("john_doe@example.com")
        
        # Close the connection when done
        close_connection(db_connection)
