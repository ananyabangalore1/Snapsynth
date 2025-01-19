import sqlite3

# Initialize the database and create the necessary table if it doesn't exist
def init_db():
    conn = sqlite3.connect("snapsynth.db")  # Create or connect to a SQLite database file
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    # Create the table for storing reference images if it doesn't already exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reference_images (
        id INTEGER PRIMARY KEY, 
        name TEXT, 
        image BLOB
    )
    """)
    return conn, cursor  # Return the connection and cursor to be used later

# Save a reference image to the database
def save_reference_image(cursor, conn, uploaded_image):
    image_bytes = uploaded_image.read()  # Read the image content as bytes
    # Insert the image data and its name into the reference_images table
    cursor.execute("INSERT INTO reference_images (name, image) VALUES (?, ?)", 
                   (uploaded_image.name, image_bytes))
    conn.commit()  # Commit the transaction to save the changes in the database

# Retrieve all stored reference images from the database
def get_reference_images(cursor):
    cursor.execute("SELECT name, image FROM reference_images")  # Query to get image names and data
    return cursor.fetchall()  # Fetch and return all results
