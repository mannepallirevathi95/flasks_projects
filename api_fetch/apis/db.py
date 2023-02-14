import psycopg2 as pg2
from user_details import user_section

# Step1 : Get connection
conn = pg2.connect(host="localhost",
                            port="5432",
                            database="api_DB",
                            user="postgres",
                            password="sridevi123")

# Step2 : Get cursor on db connection
cursor = conn.cursor()

# Step3: Prepare SQL Query
def create_table():
    try:

        query = "CREATE TABLE BASIC_INFO(user_id SERIAL PRIMARY KEY NOT NULL, first_name VARCHAR(100), last_name VARCHAR(100), state VARCHAR(100), country VARCHAR(100), email VARCHAR(100), user_name VARCHAR(100), password VARCHAR(100), age VARCHAR(100), cell VARCHAR(100))"

        # Step4 : Execute SQL query
        cursor.execute(query)

        # Step5: Commit the transaction
        conn.commit()
        print("** Table created successfully **")
    
    except Exception as exce:
            print("Exception occured : ", exce)

data = user_section()

def insert_table(data):

    try:

        query = """
        INSERT INTO basic_info
        (
          "first_name","last_name","state","country","email","user_name","password","age","cell"
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s)

        """
        cursor.execute(query,(data["first_name"],data["last_name"],data["state"],data["country"],data["email"],data["user_name"],data["password"],data["age"], data["cell"])
)
        conn.commit()
    except Exception as exce:
        print("Exception occured : ", exce)    


def get_user_data():
    cursor.execute('SELECT * FROM BASIC_INFO;')
    results = cursor.fetchmany(100)
    return results

insert_table(data)

def populate(num):
    print(f"Populating {num} new users into table....")
    i = 0
    while i < num:
        data = user_section()
        insert_table(data)
        i = i+1
    print(f"succesfully inserted {num} users.")

populate(30)