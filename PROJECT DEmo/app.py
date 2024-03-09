# from flask import Flask, render_template, request, flash, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from flask_login import login_user, login_required, logout_user, current_user,LoginManager
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_bcrypt import Bcrypt
# app = Flask(__name__)
# bcrypt = Bcrypt(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql6684654:lWwyUtD647@sql6.freemysqlhosting.net/sql6684654'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = '872002'

# db = SQLAlchemy(app)


# login_manager = LoginManager()
# login_manager.login_view = 'home'
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     first_name = db.Column(db.String(150))
#     username=db.Column(db.String(150))
#     videos_made=db.Column(db.Integer)

#     def __repr__(self):
#         return '<User %r>' % self.username

# def create_tables():
#     with app.app_context():
#         db.create_all()


# @app.route('/')
# def home():

#     return render_template("home.html")

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method=='POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
        

#         user = User.query.filter_by(email=email).first()
#         # print(user.password)
#         # print(password)
#         # print(generate_password_hash(password))
#         # print(check_password_hash(user.password,password))
#         if user:
#             # if password==user.password:
#             if check_password_hash(user.password, password):
#                 print("YEES")
#                 # flash('Logged in successfully!', category='success')
#                 login_user(user, remember=True)
#                 return redirect(url_for('home2'))
#             else:
#                 flash('Incorrect password, try again.', category='error')
#         else:
#             flash('Email does not exist.', category='error')
    
#     return render_template("login.html")


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():

#     if request.method == 'POST':

#         email = request.form['newEmail']
#         first_name = request.form['newName']
#         username = request.form['newUsername']
#         # password = request.form['newPassword']
#         password=generate_password_hash(request.form['newPassword'],method='pbkdf2:sha1')
#         # password = bcrypt.generate_password_hash(request.form['newPassword']).decode('utf-8')
#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email already exists.', category='error')
#             return render_template("signup.html")
#         if len(email) < 4:
#             flash('Email must be bigger than 4.', category='error')
#         elif len(first_name) < 2:
#             flash('Name must be bigger than 2.', category='error')
#         elif len(username) < 2 :
#             flash('Username must be bigger than 2.', category='error')
#         elif len(password) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             new_user = User(email=email, first_name=first_name, password=password, username=username, videos_made=0)
#             db.session.add(new_user)
#             db.session.commit()
#             login_user(new_user, remember=True)
#             # flash('Account created!', category='success')
#             return redirect(url_for('home2'))


#     return render_template("signup.html")


# @app.route('/home2', methods=['GET', 'POST'])
# @login_required
# def home2(user=None):
#     user=current_user
#     return render_template("home2.html", user=user)


# @app.route('/slideshow', methods=['GET', 'POST'])
# def slideshow(user=None):
#     user=current_user
#     return render_template("slideshow.html", user=user)

# @app.route('/dropphoto', methods=['GET', 'POST'])
# def dropphoto(user=None):
#     user=current_user
#     return render_template("dropphoto.html", user=user)


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('home'))


# @login_manager.unauthorized_handler
# def unauthorized_callback():
#     # flash('Please log in to access this page.', category='error')
#     return redirect(url_for('login'))


# if __name__ == '__main__':
#     create_tables() 
#     app.run(debug=True, port=8000)



from flask import Flask, render_template, request, flash, redirect, url_for, session, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone
from moviepy.editor import ImageClip, concatenate_videoclips, VideoClip, ImageSequenceClip
import os
from PIL import Image
from io import BytesIO
import tempfile
import numpy as np
import cv2

def img_to_nparray(img):
    # Assuming 'img' is the image data stored in the database
    # Convert the image data to a NumPy array
    nparr = np.frombuffer(img.img, np.uint8)
    # Decode the array to get the image
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return frame


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql6686138:UxB2cCvVu7@sql6.freemysqlhosting.net/sql6686138'

app.config.update(
    # UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    DROPZONE_MAX_FILE_SIZE=1024,  # set max size limit to a large number, here is 1024 MB
    DROPZONE_TIMEOUT=5 * 60 * 1000  # set upload timeout to a large number, here is 5 minutes
)

dropzone = Dropzone(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql6689529:v91Yk9RIwG@sql6.freemysqlhosting.net/sql6689529'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '3306'


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'home'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    username = db.Column(db.String(150))
    videos_made = db.Column(db.Integer)
    img = db.relationship('Img')

    def __repr__(self):
        return '<User %r>' % self.username


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # img = db.Column(db.Text,  nullable=False)
    img=db.Column(db.LargeBinary(length=(2**32)-1))
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))


def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.get(user_id)
        if user:
            login_user(user, remember=True)
            return redirect(url_for('home2'))
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            session['user_id'] = user.id
            return redirect(url_for('home2'))
        else:
            flash('Incorrect email or password. Please try again.', category='error')
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['newEmail']
        first_name = request.form['newName']
        username = request.form['newUsername']
        password = generate_password_hash(request.form['newPassword'], method='pbkdf2:sha1')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
            return render_template("signup.html")
        if len(email) < 4:
            flash('Email must be bigger than 4.', category='error')
        elif len(first_name) < 2:
            flash('Name must be bigger than 2.', category='error')
        elif len(username) < 2 :
            flash('Username must be bigger than 2.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=password, username=username, videos_made=0)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            session['user_id'] = new_user.id 
            return redirect(url_for('home2'))
    return render_template("signup.html")

@app.route('/home2', methods=['GET', 'POST'])
@login_required
def home2(user=None):
    user = current_user
    return render_template("home2.html", user=user)

@app.route('/slideshow', methods=['GET', 'POST'])
def slideshow(user=None):
    user = current_user
    user = User.query.options(db.joinedload(User.img)).filter_by(id=user.id).first()
    if request.method=="POST":
        selected_imgs=request.form.getlist("selected_images[]")
        img = Img.query.filter_by(id=selected_imgs[0]).first()
        durations=request.form.getlist("duration")
        durations = [x for x in durations if x.strip()]
        result = [[selected_imgs[i], durations[i]] for i in range(len(durations))]
        print(img.img)
        selected_images=[]
        for i in selected_imgs:
            img = Img.query.filter_by(id=i).first()
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                temp_file.write(img.img)
                selected_images.append(temp_file.name)
        fixed_image_size = (1920, 1080)  # Fixed dimensions for all images
        resized_images = []
        for image_path in selected_images:
            try:
                image = Image.open(image_path)
                resized_image = image.resize(fixed_image_size)
                resized_image_path = tempfile.NamedTemporaryFile(delete=False, suffix='.png').name
                resized_image.save(resized_image_path)
                resized_images.append(resized_image_path)
            except Exception as e:
                print(f"Error processing image: {str(e)}")
        if resized_images:
            # Create image sequence clip
            image_duration = 1  # Example duration of each image in seconds
            image_clip = ImageSequenceClip(resized_images, durations=[image_duration] * len(resized_images), fps=1)

            # Export the final video
            image_clip.write_videofile('output.mp4', fps=1)
        else:
            print("No valid images found.")
        # for i,j in result:
            
        
        
    return render_template("slideshow.html", user=user)

@app.route('/dropphoto', methods=['GET', 'POST'])
def dropphoto(user=None):
    user = current_user
    print(request.method)
    # if request.method == "POST":    

    #     if 'file' not in request.files:
    #         return 'No file part'
        
    #     files = request.files.getlist('file')
    #     for pic in files:
    #         filename = secure_filename(pic.filename)
    #         mimetype = pic.mimetype
    #         if filename == "":
    #             continue
    #         img = Img(img=pic.read(), name=filename, mimetype=mimetype, user_id=user.id)
    #         db.session.add(img)
    #         db.session.commit()
    if request.method == "POST":
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)

        files = request.files.getlist('file')
        for pic in files:
            # Validate the file type if necessary
            if pic.filename == '':
                flash('No selected file', category='error')
                continue
            if pic:
                # Read the file content
                file_content = pic.read()
                # Check if the file content is empty
                if len(file_content) == 0:
                    flash('Empty file uploaded', category='error')
                    continue
                # Store the image in the database
                img = Img(img=file_content, name=secure_filename(pic.filename), mimetype=pic.mimetype, user_id=user.id)
                db.session.add(img)
                db.session.commit()
                flash('File uploaded successfully', category='success')




    return render_template("dropphoto.html", user=user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Please log in to access this page.', category='error')
    return redirect(url_for('login'))


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    create_tables()

    app.run(debug=True, port=8000)




