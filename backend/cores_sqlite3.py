import sqlite3
import os
from datetime import datetime
from backend.cores_hash import get_salt_hash, authenticate

# define a dictionary that sets the attributes of the class User and the columns of the table 'users'
def init_user_dict():
    # the values are used simply to show the formatting. The User class is set with None values. 
    user_dict = {   'id'             : '123',
                    'email'          : 'John.Doe@mail.edu',         # previously named user_id 
                    'name'           : 'John Doe',                  # previously named user_name
                    'nickname'       : 'Nick',                      # previously named user_nickname
                    'phone'          : '123-456-7890', 	            # previously user_phone
                    'pi_name'        : 'Dr. Pie',
                    'pi_phone'       : '555-555-5555',
                    'type'           : 'user | admin',              # previously user_type
                    'last_mod_type'  : 'iLab',
                    'last_mod'       : '2023-08-18 21:20:00',
                    'first_login'    : '2023-07-17 17:20:00',
                    'last_login'     : '2023-07-18 09:20:00',
                    'salt'           : '12345678901234567890',
                    'hash'           : 'ofiae98aeikjs;aelsij',
                    'login_attempts' : '1', 
                    'locked_after'   : '2024-12-31 00:00:00'  }
    return user_dict

# define a dictionary that sets the attributes of the class Event and the columns of the table 'events'
def init_event_dict():
    event_dict = {  'id'          : '123',
                    'email'     : 'xyz@chop.edu',
                    'device'      : 'Aurora alpha',
                    'login_time'  : '2023-08-18 14:20:00',
                    'login_type'  : 'local | iLab | EMERGENCY',
                    'logout_time' : '2023-08-18 16:20:00',
                    'logout_type' : 'by_user  | by_inactivity  | pending' }
    return event_dict


# The functions below are outside of any class
# they should not need the @staticmethod decorator
def conn_cores_db(path_to_folder= None): 
    # if no path_to_folder is provided, use the script's folder
    if path_to_folder == None:
        path_to_folder = os.path.dirname(os.path.abspath(__file__)) 
    path_to_cores_db = os.path.join(path_to_folder, 'cores.db')
    
    # check if the file named cores.db already exists in path_to_cores_db 
    if os.path.exists(path_to_cores_db):
        conn = sqlite3.connect(path_to_cores_db)
        # print("Connected to 'cores.db' ...")             
        return conn
    
    # show warning and ask if user wants to create new DB
    else:
        print("WARNING: 'cores.db' not found.")
        user_input = input("Would you like to create a new database? (yes/no): ").upper() 

        # if yes, create cores.db file
        if (user_input == 'YES' or user_input == 'Y') : 
            try:
                conn = sqlite3.connect(path_to_cores_db)
                print("'cores.db' has been created.")
                create_tables(conn)         

                # create & add admin user when new db created 
                admin_user = User()
                admin_user.email = 'admin'
                admin_user.name = 'Admin User'
                admin_user.type = 'admin'
                admin_user.salt, admin_user.hash = get_salt_hash('admin', 'admin')
                admin_user.add_user()
                print('Admin user created.')

                return conn
            except sqlite3.Error as e:
                print("Error:", e)
                return False
        else:
            print("Aborted.")
            return False

# Create two tables ('users' and 'events') in cores.db, if they do not exist
def create_tables(conn):
    empty_user = User()
    user_dict = empty_user.__dict__
    del user_dict['id']   # remove the id key which will need to be handled differently

    event_dict = init_event_dict()
    del event_dict['id']  # remove the id key (handled differently)

    # add two table 'users' to cores.db
    try:
        # Create a cursor object using the cursor() method
        cursor = conn.cursor()

        # i) Create 'users' table with necessary columns
        sql_users_0 = ", ".join([f"{col} TEXT" for col in user_dict.keys()]) 
        sql_users = f"CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, {sql_users_0} )"
        cursor.execute(sql_users)
        conn.commit()
    except sqlite3.Error as e:
        print("Error while creating the 'users' table:", e)
        return False
    
    # add two table 'events' to cores.db
    try:
        # ii) Create 'logins' table with necessary columns
        sql_events_0 = ", ".join([f"{col} TEXT" for col in event_dict.keys()]) 
        sql_events = f"CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, {sql_events_0} )"
        cursor.execute(sql_events)
        conn.commit()
        conn.close
        print("Tables 'users' and 'logins' created successfully.")  
    except sqlite3.Error as e:
        print("Error while creating the 'logins' table:", e)
        return False

    return True


class User:
    def __init__(self, user_dict=init_user_dict()):
        # usage: user1 = User() will generate an empty instance
        for key, value in user_dict.items():
            setattr(self, key, None)

    # Method to add a user to the 'users' table
    def add_user(self):
        try:
            # Generate the dictionary of attribute names and values for user
            user_dict = self.__dict__

            # Generate the placeholders for SQL values   :id, :email, :name ...
            placeholders = ", ".join([f":{col}" for col in user_dict.keys()])   #--FT Excellent idea! 

            # Generate the SQL query using named placeholders
            sql = f"INSERT INTO users VALUES ({placeholders})"
            
            # connect to cores.db;  
            conn = conn_cores_db()   
            with conn:
                cursor = conn.cursor()
                cursor.execute(sql, user_dict)
                conn.commit()
                row_id = cursor.lastrowid

            print(f"User added successfully on row {row_id}.")
            self.id = row_id
            return row_id  # Return the row ID of the added user
        
        except sqlite3.Error as e:
            print("Error:", e)
            return None  
        

    @classmethod
    # This method constructs a User instance with attributes values existing in the the 'users' table
    # The function does the following:
    #           - read a line from database; 
    #           - create an new instance of the User class; 
    #           - set the values read from database to the attributes of the instance;
    #           - return the instance
    # Usage: new_user = User.from_database(id)
    def from_database(cls, row_id):
        # connect to cores.db;  
        conn = conn_cores_db()   
        with conn:
            cursor = conn.cursor()
            try:
                # Fetch the user's information from the database
                cursor.execute("SELECT * FROM users WHERE id=?", (row_id,))
                user_info = cursor.fetchone()

                if user_info:
                    user_instance = cls()  # Create an empty instance of the class
                    # Create empty dict to put loaded user into
                    user_dict = {}

                    # Use zip to create something like ("id", 1), ...
                    for key, value in zip(user_instance.__dict__.keys(), user_info):
                        user_dict[key] = value
                    user_instance.__dict__.update(user_dict)   # the builtin update function is very convenient here!

                    print("User information loaded successfully.")
                    return user_instance
                else:
                    print("Error: User not found.")
                    return None

            except sqlite3.Error as e:
                print("Error:", e)
                return None
    
    @classmethod
    def from_database_by_email(cls, email):
        # Get the row ID for the given email
        row_id = get_rowid_for_email(email)
        
        # If row ID is found, call the generic method
        if row_id is not None:
            return cls.from_database(row_id)
        else:
            print(f"Error: User with email '{email}' not found.")
            return None

    # Update one property of one user with known rowid
    def update_user_property(self, id, column_name, new_value):
        
        try:
            sql = """--sql 
                UPDATE  users 
                SET     {}  = ? 
                WHERE   id == ?
            """.format(column_name)


            # connect to cores_db;  
            # EDITED
            #conn = conn_cores_db(script_directory)   
            conn = conn_cores_db()
            with conn:
                cur = conn.cursor()
                cur.execute(sql, (new_value, id))
                conn.commit()
            print("User updated successfully.")
            return True
        except sqlite3.Error as e:
            print("Error:", e)
            return False

    @staticmethod
    def authenticate_user(email, password) :
         # connect to cores_db;  
        conn = conn_cores_db()

        # get stored salt and hash in user's row 
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT salt, hash FROM users WHERE email=?", (email,))
                user_info = cursor.fetchone()

                if user_info:
                    salt_db_str, hash_db_str = user_info
                else:
                    # User not found
                    return False

        except sqlite3.Error as e:
            print("Error while retrieving user info:", e)
            return False
        
        result = authenticate(email, password, salt_db_str, hash_db_str)
        
        return result

# get the rowid of a user existing in the 'users' table, based on email and pi_name 
def get_rowid_for(email, pi_name):

    # connect to cores_db;  
    # EDITED
    #conn = conn_cores_db(script_directory) 
    conn = conn_cores_db()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email=? AND pi_name=?", (email, pi_name))
        user_ids = cur.fetchall()
        print(user_ids, "  |  len(user_id):", len(user_ids))
    
    if len(user_ids)==1:
        (int_user_id,) = user_ids      
        print('int_user_id:', int_user_id)
        return int_user_id
    elif len(user_ids)==0:
        print('Error: no user found!')
        return None
    else:
        print("WARNING: More than one user with the same email address and the same PI!")
        return user_ids

def get_rowid_for_email(email):
    # connect to cores_db;  
    conn = conn_cores_db()   
    with conn:
        cursor = conn.cursor()
        try:
            # Fetch the user's row ID from the database
            cursor.execute("SELECT id FROM users WHERE email=?", (email,))
            row_id = cursor.fetchone()

            if row_id:
                return row_id[0]
            else:
                print(f"Error: User with email '{email}' not found.")
                return None

        except sqlite3.Error as e:
            print("Error:", e)
            return None
    

class Event:
    def __init__(self, event_dict=init_event_dict()):
        for key, value in event_dict.items():
            setattr(self, key, None)

    def record_login(self):
        # 3) Func: record_login(...):
        # Purpose: add one row to 'logins' table to record a login event
        # return row_id if successful
        # Usage:  current_event.record_login()
        conn = conn_cores_db() 
        with conn:
            cursor = conn.cursor()
            # Generate the dictionary of attribute names and values for log
            event_dict = self.__dict__

            try:
                # Generate the placeholders for SQL values
                placeholders = ', '.join([f":{col}" for col in event_dict.keys()])
                # Generate the SQL query using named placeholders
                sql = f"INSERT INTO events VALUES ({placeholders})"
                cursor.execute(sql, event_dict)
                conn.commit()

                # Store lastrowid in the Event instance
                self.lastrowid = cursor.lastrowid

                print("Login event recorded successfully.")
                return self.lastrowid
            except sqlite3.Error as e:
                print("Error while recording login event:", e)
                return None
        
    def record_logout(self):
        # Function to record logout datetime using lastrowid
        if hasattr(self, 'lastrowid') and self.lastrowid is not None:
            conn = conn_cores_db()
            with conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("UPDATE events SET logout_time=? WHERE id=?", (datetime.now(), self.lastrowid))
                    conn.commit()
                    print("Logout event recorded successfully.")
                    return True
                except sqlite3.Error as e:
                    print("Error while recording logout event:", e)
                    return False
        else:
            print("Error: Cannot record logout event without a valid login event.")
            return False


def initialize_database():
    # Set the path to the database (cores.db)
    script_directory = os.path.dirname(os.path.abspath(__file__))
    path_to_folder = os.path.dirname(os.path.abspath(__file__))
    conn = conn_cores_db(path_to_folder)

    # create an instance user
    #user1 = User() 

    # set values for some attributes 
    #user1.email = 'user1@chop.edu'  
    #user1.name = 'Jim Smith'
    #user1.nickname = 'Jim'
    #user1.phone = '111-456-7890'
    #user1.pi_name = 'Dr. Sam'
    #user1.pi_phone = '445-444-4444'
    #user1.first_login = '2023-08-02 13:31:03'
    #user1.login_attempts = '1'

    # add user
    #user1.add_user()

    # get the row_id of the user
    #row_id = get_rowid_for('user1@chop.edu', "Dr.Sam")
    #print ('row_id:', row_id)  

    #salt_str, hash_db =  get_salt_hash('user1@chop.edu', 'psw')
    #print('hash_db:', hash_db) 

    # update the the user property
    #id = 1
    #user1.update_user_property(id, "salt", salt_str)
    #user1.update_user_property(id, "hash", hash_db)
    
    #print(User.authenticate_user("user1@chop.edu","psw"))