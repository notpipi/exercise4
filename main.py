import sqlite3

# 连接到数据库
conn = sqlite3.connect('library.db')
cursor = conn.cursor()


def create_table():
    # 创建Books表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            BookID TEXT PRIMARY KEY,
            Title TEXT,
            Author TEXT,
            ISBN TEXT,
            Status TEXT
        )
    ''')
    # 创建Users表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID TEXT PRIMARY KEY,
            Name TEXT,
            Email TEXT
        )
    ''')
    # 创建Reservations表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservations (
            ReservationID TEXT PRIMARY KEY,
            BookID TEXT,
            UserID TEXT,
            ReservationDate TEXT
        )
    ''')
    # 提交更改
    conn.commit()


def add_book(BookID, Title, Author, ISBN, Status):
    # 添加书籍到Books表
    cursor.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",
                   (BookID, Title, Author, ISBN, Status))
    conn.commit()


def find_book_by_id(BookID):
    # 根据BookID查找书籍
    cursor.execute("SELECT * FROM Books WHERE BookID=?", (BookID,))
    book = cursor.fetchone()
    if book:
        return book
    else:
        return None


def find_reservation_status(search_term):
    # 根据BookID、Title、UserID、ReservationID查找预订状态
    if search_term.startswith("LB"):  # BookID
        cursor.execute("SELECT * FROM Books WHERE BookID=?", (search_term,))
        book = cursor.fetchone()
        if book:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Status:", book[4])

            # 查找是否有预订信息
            cursor.execute("SELECT * FROM Reservations WHERE BookID=?", (book[0],))
            reservations = cursor.fetchall()

            if reservations:
                print("Reservations:")
                for reservation in reservations:
                    print("ReservationID:", reservation[0])
                    print("UserID:", reservation[2])
                    print("ReservationDate:", reservation[3])
            else:
                print("No reservations for this book.")
        else:
            print("Book not found.")
    elif search_term.startswith("LU"):  # UserID
        user_id = search_term
        cursor.execute("SELECT * FROM Reservations WHERE UserID=?", (user_id,))
        reservations = cursor.fetchall()
        if reservations:
            print("Reservations for User", user_id)
            for reservation in reservations:
                cursor.execute("SELECT * FROM Books WHERE BookID=?", (reservation[1],))
                book = cursor.fetchone()
                print("ReservationID:", reservation[0])
                print("BookID:", reservation[1])
                print("Book Title:", book[1])
                print("Status:", book[4])
                print("ReservationDate:", reservation[3])
        else:
            print("No reservations found for User", user_id)
    elif search_term.startswith("LR"):  # ReservationID
        cursor.execute("SELECT * FROM Reservations WHERE ReservationID=?", (search_term,))
        reservation = cursor.fetchone()
        if reservation:
            cursor.execute("SELECT * FROM Books WHERE BookID=?", (reservation[1],))
            book = cursor.fetchone()
            print("ReservationID:", reservation[0])
            print("BookID:", reservation[1])
            print("Book Title:", book[1])
            print("UserID:", reservation[2])
            print("ReservationDate:", reservation[3])
        else:
            print("Reservation not found.")
    else:  # Title
        cursor.execute("SELECT * FROM Books WHERE Title=?", (search_term,))
        book = cursor.fetchone()
        if book:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
        else:
            print("Book not found.")


def find_all_books():
    # 查找所有书籍（包括书籍、用户和预订信息）
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()

    for book in books:
        print("BookID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])

        cursor.execute("SELECT * FROM Reservations WHERE BookID=?", (book[0],))
        reservations = cursor.fetchall()

        if reservations:
            print("Reservations:")
            for reservation in reservations:
                print("ReservationID:", reservation[0])
                print("UserID:", reservation[2])
                print("ReservationDate:", reservation[3])
        else:
            print("No reservations for this book.")

        cursor.execute("SELECT * FROM Users WHERE UserID=?", (book[4],))
        user = cursor.fetchone()
        if user:
            print("User Name:", user[1])
            print("User Email:", user[2])


def update_book_details(BookID, new_title, new_author, new_isbn):
    # 更新书籍详情（仅限Books表）
    cursor.execute("UPDATE Books SET Title=?, Author=?, ISBN=? WHERE BookID=?",
                   (new_title, new_author, new_isbn, BookID))
    conn.commit()


def delete_book(BookID):
    # 删除书籍及相关预订信息
    cursor.execute("DELETE FROM Books WHERE BookID=?", (BookID,))
    cursor.execute("DELETE FROM Reservations WHERE BookID=?", (BookID,))
    conn.commit()


# 创建表格
create_table()

while True:
    print("\nLibrary Management System Menu:")
    print("1. Add a new book")
    print("2. Find a book by BookID, Title, UserID, or ReservationID")
    print("3. Find all books")
    print("4. Update book details")
    print("5. Delete a book")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        BookID = input("Enter BookID: ")
        Title = input("Enter Title: ")
        Author = input("Enter Author: ")
        ISBN = input("Enter ISBN: ")
        Status = input("Enter Status: ")
        add_book(BookID, Title, Author, ISBN, Status)
        print("Book added successfully!")
    elif choice == "2":
        search_term = input("Enter BookID, Title, UserID, or ReservationID: ")
        find_reservation_status(search_term)
    elif choice == "3":
        find_all_books()
    elif choice == "4":
        BookID = input("Enter BookID: ")
        new_title = input("Enter new Title: ")
        new_author = input("Enter new Author: ")
        new_isbn = input("Enter new ISBN: ")
        update_book_details(BookID, new_title, new_author, new_isbn)
        print("Book details updated successfully!")
    elif choice == "5":
        BookID = input("Enter BookID: ")
        delete_book(BookID)
        print("Book deleted successfully!")
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

# 关闭数据库连接
conn.close()
