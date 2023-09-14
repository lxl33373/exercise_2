import sqlite3

# Read the file and copy content to a list
with open('stephen_king_adaptations.txt', 'r') as file:
    stephen_king_adaptations_list = file.readlines()

# Establish connection with SQLite database
conn = sqlite3.connect('stephen_king_adaptations.db')
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                    movieID INTEGER PRIMARY KEY AUTOINCREMENT,
                    movieName TEXT,
                    movieYear INTEGER,
                    imdbRating REAL
                )''')

# Insert data into the table
for line in stephen_king_adaptations_list:
    movie_data = line.split(',')
    cursor.execute('''INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating)
                      VALUES (?, ?, ?)''', (movie_data[1], int(movie_data[2]), float(movie_data[3])))

# Commit changes to the database
conn.commit()

# User interaction loop
while True:
    print("Select an option:")
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. STOP")

    option = input("Enter your choice: ")

    if option == '1':
        movie_name = input("Enter the movie name: ")
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?''', (movie_name,))
        result = cursor.fetchone()

        if result:
            print("Movie details:")
            print("Name:", result[1])
            print("Year:", result[2])
            print("Rating:", result[3])
        else:
            print("No such movie exists in our database")

    elif option == '2':
        movie_year = input("Enter the movie year: ")
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?''', (int(movie_year),))
        results = cursor.fetchall()

        if results:
            print("Movies released in", movie_year, ":")
            for result in results:
                print("Name:", result[1])
                print("Year:", result[2])
                print("Rating:", result[3])
        else:
            print("No movies were found for that year in our database.")

    elif option == '3':
        rating = input("Enter the minimum rating: ")
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?''', (float(rating),))
        results = cursor.fetchall()

        if results:
            print("Movies with a rating of", rating, "or above:")
            for result in results:
                print("Name:", result[1])
                print("Year:", result[2])
                print("Rating:", result[3])
        else:
            print("No movies at or above that rating were found in the database.")

    elif option == '4':
        break

    print()

# Close the database connection
conn.close()