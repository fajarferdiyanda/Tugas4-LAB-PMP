from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Konfigurasi database MySQL
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = '' 
app.config['MYSQL_DB'] = 'library'

mysql = MySQL(app)

# Halaman utama: Read data
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    return render_template('index.html', books=books)

# Create data
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO books (title, author, year) VALUES (%s, %s, %s)", (title, author, year))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

# Update data
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        cur.execute("UPDATE books SET title=%s, author=%s, year=%s WHERE id=%s", (title, author, year, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    else:
        cur.execute("SELECT * FROM books WHERE id=%s", (id,))
        book = cur.fetchone()
        cur.close()
        return render_template('edit.html', book=book)

# Delete data
@app.route('/delete/<int:id>')
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
