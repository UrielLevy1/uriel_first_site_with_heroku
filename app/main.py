import sqlite3
from flask import Flask, render_template, request, redirect

con = sqlite3.connect("tutorial.db", check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS books (book_name, author, year_pub, genre)")

# cur.execute("INSERT INTO books VALUES ('IT ENDS WITH US','Colleen Hoover','1990','drama'),('SOUL TAKEN','Patricia Briggs','1996','comedy'),('BREAKING HISTORY','Jared Kushner','2001','drama')")
# con.commit()   

app = Flask(__name__)
 
@app.route("/")
def hello_world():
   return render_template ("first.html")

@app.route("/books")
def books():
    result = cur.execute("SELECT *,rowid from books").fetchall()
    return render_template ("books.html",books=result)   

@app.route("/deletebook")
def deletebook(): 
    id = request.args.get('id')
    cur.execute(f"DELETE FROM books WHERE rowid={id};")
    con.commit()
    return redirect("/?message=Book Deleted")

@app.route("/menu")
def menu_page():
   return render_template ("base.html")  

@app.route("/addbookindb", methods = ['POST'])
def addbook_indb():
    book_name = request.form.get('book_name')
    author = request.form.get('author')
    year_pub = request.form.get('year_pub')
    genre = request.form.get('genre')
    cur.execute(f"INSERT INTO books VALUES ('{book_name}','{author}','{year_pub}','{genre}')")
    con.commit()
    return redirect("/?message=Book Added")
    
@app.route("/addbook")
def addbook():
    return render_template("addbook.html")

@app.route("/searchbook")
def searchbook():
    search = request.args.get('search')
    result = cur.execute(f"SELECT *,rowid from books WHERE book_name LIKE '%{search}%'").fetchall()
    print(result)
    return render_template ("books.html",books=result)           
 
if __name__ == '__main__':
   app.run(debug=True)