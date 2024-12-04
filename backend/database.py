import psycopg2

# PostgreSQL connection
def connect_db():
    """
    Provides the necessary connection to the database.
    """
    conn = psycopg2.connect(
        dbname="skymodcert",  # Database name
        user="skymod",        # PostgreSQL username
        password="123456",    # PostgreSQL password
        host="localhost",     # Connection address
        port="5432"           # Connection port
    )
    return conn

# Save certificate to the database
def save_certificate_to_db(token, data, pdf_data):
    """
    Saves the certificate data to the PostgreSQL database.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the 'certificates' table exists and create it if not
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS certificates (
        id SERIAL PRIMARY KEY,
        certificate_number VARCHAR(64) UNIQUE NOT NULL,
        candidate_name VARCHAR(255) NOT NULL,
        training_name VARCHAR(255) NOT NULL,
        training_duration VARCHAR(255) NOT NULL,
        training_date DATE NOT NULL,
        pdf BYTEA NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''
    cursor.execute(create_table_query)  # Execute the command to create the table

    # Insert the certificate data into the 'certificates' table
    insert_query = '''
    INSERT INTO certificates (
        certificate_number, candidate_name, training_name, 
        training_duration, training_date, pdf
    ) VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (token, data.name, data.type, data.duration, data.date, psycopg2.Binary(pdf_data)))

    # Commit the changes to the database
    conn.commit()

    cursor.close()
    conn.close()
