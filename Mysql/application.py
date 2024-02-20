from flask import Flask, request, render_template
import pymysql


application = Flask(__name__)

# Database connection
connection = pymysql.connect(host="sql6.freemysqlhosting.net", user="sql6684654", password="lWwyUtD647", database="sql6684654")
cursor = connection.cursor()

@application.route("/")
def helloworld():
    return render_template('index.html')

@application.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":    
        # Check if the request contains files
        if 'file' not in request.files:
            return 'No file part'
        
        files = request.files.getlist('file')
        for file in files:
            filename = file.filename
            if filename == "":
                continue
            cursor.execute("INSERT INTO Images (name, user_id) VALUES (%s, 1)", (filename,))
            connection.commit()
        
        return 'Files uploaded successfully'

if __name__ == "__main__":
    application.run()
