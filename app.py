import os
from flask import *
from flask_migrate import Migrate
from flask_sqlalchemy import *
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = Flask
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_NAME = os.getenv('DB_NAME', 'postgres')
database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
app.config['SECRET_KEY'] = "F465656546666"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Brand(db.Model):
    __tablename__ = "brand"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    img = Column(String)
    cars = db.relationship('Cars', backref="brand", order_by="Cars.id")


class Cars(db.Model):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    img = Column(String)
    price = Column(String)
    brand_id = Column(Integer, ForeignKey('brand.id'))


def online_user():
    get = None
    if "username" in session:
        user = User.query.filter(User.username == session["username"]).first()
        get = user
    return get


@app.route('/brand', methods=['POST', 'GET'])
def brand():
    user = online_user()
    if request.method == 'POST':
        name = request.form.get("name")
        photo = request.files["photo"]
        photo_url = ""
        if photo:
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + 'static/img/' + photo_file
            app.config['UPLOAD_FOLDER'] = 'static/img'
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        add = Brand(name=name, img=photo_url)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("brand"))
    brands = Brand.query.all()
    return render_template('basic.html', brends=brands, user=user)


@app.route('/brand_edit/<int:brand_id>', methods=["POST", "GET"])
def brand_edit(brand_id):
    brand = Brand.query.filter(Brand.id == brand_id).first()
    if request.method == "POST":
        name = request.form.get("name")
        photo7 = request.files["photo7"]
        photo_url = ""
        if photo7:
            print(photo7.filename)
            photo_file = secure_filename(photo7.filename)
            photo_url = '/' + 'static/img/' + photo_file
            app.config['UPLOAD_FOLDER'] = 'static/img'
            photo7.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        Brand.query.filter(Brand.id == brand_id).update({
            "name": name,
            "img": photo_url
        })
        db.session.commit()
        return redirect(url_for("brand_edit", brand_id=brand_id))
    return render_template("brand_edit.html", brand=brand)


@app.route('/brand_delete/<int:brand_id>')
def brand_delete(brand_id):
    bran = Brand.query.filter(Brand.id == brand_id).first()
    db.session.delete(bran)
    db.session.commit()
    return redirect(url_for("brand"))


@app.route('/add_car', methods=['POST', 'GET'])
def add_car():
    if request.method == "POST":
        brand_id = request.form.get("brand_id")
        name = request.form.get("name7")
        price = request.form.get("price")
        photo = request.files["img"]
        photo_url = ""
        if photo:
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + 'static/img/' + photo_file
            app.config['UPLOAD_FOLDER'] = 'static/img'
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        add = Cars(name=name, brand_id=brand_id, img=photo_url, price=price)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("brand"))
    cars_brand = Brand.query.all()
    return render_template("basic.html", cars_brand=cars_brand)


@app.route('/brands_car/<int:brand_id>')
def brands_car(brand_id):
    brands = Brand.query.all()
    brandes = Brand.query.filter(Brand.id == brand_id).first()
    user = online_user()
    return render_template("brandes_car.html", brandes=brandes, brands=brands, user=user)


@app.route('/delete/<int:cars_id>')
def delete(cars_id):
    cars = Cars.query.filter(Cars.id == cars_id).delete()
    db.session.commit()
    return redirect(url_for("brand", car_id=cars))


@app.route('/model')
def models():
    return render_template("avto.html")


@app.route('/dealers')
def dealers():
    return render_template("dealers.html")


@app.route('/ cars77')
def cars77():
    return render_template("cars77.html")


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    product_name = Column(String)
    product_price = Column(Integer)
    product_img = Column(String)

    def order(self):
        db.session.add(self)
        db.session.commit()


@app.route('/add_product/<int:cars_id>/<int:brands_id>', methods=["POST", "GET"])
def add_product(cars_id, brands_id):
    product = Cars.query.filter(Cars.id == cars_id).first()
    user = online_user()
    add = Product(product_id=product.id, product_name=product.name, product_price=product.price, user_id=user.id,
                  product_img=product.img)
    db.session.add(add)
    db.session.commit()

    return redirect(url_for("brands_car", brand_id=brands_id))


@app.route('/korzina', methods=["POST", "GET"])
def korzinka():
    user = online_user()
    cares = Product.query.filter(Product.user_id == user.id).all()
    overall = 0
    for pro in cares:
        overall += pro.product_price
    return render_template("korzinka.html", cares=cares, user=user, overall=overall)


@app.route('/ add_delete/<int:cars_id>')
def add_delete(cars_id):
    deli = Product.query.filter(Product.product_id == cars_id).first()
    db.session.delete(deli)
    db.session.commit()
    return redirect(url_for("korzinka"))


@app.route('/kor_del')
def kor_del():
    user = online_user()
    Product.query.filter(Product.user_id == user.id).delete()
    db.session.commit()
    return render_template("korzinka.html")


@app.route('/car_edit/<int:cars_id>', methods=["POST", "GET"])
def car_edit(cars_id):
    car = Cars.query.filter(Cars.id == cars_id).first()
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        photo8 = request.files["photo8"]
        photo_url = ""
        if photo8:
            print(photo8.filename)
            photo_file = secure_filename(photo8.filename)
            photo_url = '/' + 'static/img/' + photo_file
            app.config['UPLOAD_FOLDER'] = 'static/img'
            photo8.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        Cars.query.filter(Cars.id == cars_id).update({
            "name": name,
            "price": price,
            "img": photo_url
        })
        db.session.commit()
        return redirect(url_for("car_edit", cars_id=cars_id))
    return render_template("car_edit.html", car=car)


@app.route('/by', methods=["POST", "GET"])
def by():
    return render_template("brandes_car.html")


@app.route('/kobinet')
def kobinet():
    user = online_user()

    return render_template("kabinet.html", user=user)


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String)
    surname = Column(String)
    name = Column(String)
    img = Column(String)
    route = Column(String)
    password = Column(String)

    def ad(self):
        db.session.delete(self)
        db.session.commit()


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        surname = request.form.get("surname")
        password = request.form.get("password")
        photo = request.files["photo"]
        hashed = generate_password_hash(password=password, method='scrypt')
        photo_url = ""
        if photo:
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + 'static/img/' + photo_file
            app.config['UPLOAD_FOLDER'] = 'static/img'
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        add = User(username=username, name=name, surname=surname, password=hashed, img=photo_url)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html")


@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter(User.username == username).first()
        if user:
            if check_password_hash(user.password, password):
                session["username"] = user.username
                return redirect(url_for("models"))
            else:
                return redirect(url_for("login"))
    return render_template("login.html")


@app.route('/delete_login/<int:user_id>', methods=["POST", "GET"])
def delete_login(user_id):
    user = online_user()
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect(url_for("register"))


@app.route('/user_edit/<int:user_id>', methods=["POST", "GET"])
def user_edit(user_id):
    user = online_user()
    if request.method == "POST":
        name1 = request.form.get("name")
        surname2 = request.form.get("surname")
        photo = request.files["photo77"]
        photo_url3 = ""
        if photo:
            photo_file = secure_filename(photo.filename)
            photo_url3 = '/' + 'static/img/' + photo_file
            app.config['UPLOAD_FOLDER'] = 'static/img'
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        User.query.filter(User.id == user_id).update({
            "name": name1,
            "surname": surname2,
            "img": photo_url3
        })
        db.session.commit()
        return redirect(url_for("user_edit", user_id=user_id))
    return render_template("edit_acount.html", user=user)


@app.route('/hello_world', methods=['POST', 'GET'])
def hello_world():
    return render_template("basic.html")


if __name__ == '__main__':
    app.run()
