import mysql.connector as my
import datetime
import tkinter as tk

root= tk.Tk()


con = my.connect(
    host='localhost',
    user='root',
    password='10032006',
    database="company"
)
cursor = con.cursor()

def takenbook(book_id, member_id):
    cursor.execute("SELECT name FROM members WHERE member_id = %s",(member_id,))
    mem = cursor.fetchone()
    if not mem :
        print("No member found the person you entered cannot take the book !!!")
        return 
    cursor.execute("SELECT available_copies FROM books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()

    if result is None:
        print("Book not found.")
        return
    
    available_copies = result[0]

    if available_copies > 0 :
        
        cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s",(book_id,))
        
        loan_date = datetime.datetime.now()  
        due_date = loan_date + datetime.timedelta(days=14)  

       
        cursor.execute("""
            INSERT INTO loans (member_id, book_id, loan_date, due_date, return_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (member_id, book_id, loan_date, due_date, None))
        
        con.commit()
        cursor.execute("SELECT title FROM books WHERE book_id = %s",(book_id,))
        l=cursor.fetchone()
        if l:
         o=l[0]
         cursor.execute("SELECT name FROM  members WHERE  member_id = %s",(member_id,))
        mw=cursor.fetchone()
        if mw :
            k=mw[0]
            print(f"The book -> {o}   BOOK ID -> {book_id} was taken by -> {k}.")
    else:
        print("Sorry, no copies available for this book.")


def order_copies (number,book_id ):
    cursor.execute("SELECT available_copies FROM books WHERE book_id = %s ",(book_id,))
    m=cursor.fetchone()
    
    if not m :
        print(f"NO book having ID {book_id} ")
        return
    cursor.execute("UPDATE books SET available_copies = available_copies + %s WHERE book_id = %s",(number,book_id))
    print("BOOKS added in LIBRARY  THANKU FOR THE ORDERS ")
    

    con.commit()






def exitprogram():
    con.close()
    



root.title("Library Management System")
root.geometry("500x350")


tk.Label(root, text="Book ID->").pack(pady=5)
entry_book_id = tk.Entry(root)
entry_book_id.pack(pady=5)

tk.Label(root, text="Member ID->").pack(pady=5)
entry_member_id = tk.Entry(root)
entry_member_id.pack(pady=5)

tk.Label(root, text="Number of Copies (for Add Copies)->").pack(pady=5)
entry_num_copies = tk.Entry(root)
entry_num_copies.pack(pady=5)


tk.Button(root, text="Take Book",
          command=lambda: takenbook(entry_book_id.get(), entry_member_id.get()),
          width=20, bg="red").pack(pady=10)

tk.Button(root, text="Add Copies",
          command=lambda: order_copies(int(entry_num_copies.get()), entry_book_id.get()),
          width=20, bg="yellow").pack(pady=10)

tk.Button(root, text="Exit", command=exitprogram, width=20, bg="green").pack(pady=10)

root.mainloop()











        

