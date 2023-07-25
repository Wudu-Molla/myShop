from flask import render_template, request, redirect, url_for, flash
from . import app, db
from flask_login import login_required
from .models import Product, Users, Cart
from .forms import SignupForm, AddForm, SignInForm, AddToCart
from .forms import RemoveFromCart
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = AddToCart()
    if form.validate_on_submit():
        item_id = request.args.get('item')
        items = Product.query.filter_by(id=item_id).first()
        if items:
            inCart = Cart.query.filter_by(barcode=items.barcode).first()
            if inCart is None:
                db.session.add(Cart(title=items.title,
                                    barcode=items.barcode,
                                    description=items.description,
                                    price=items.price,
                                    size=items.size,
                                    image_url=items.image_url,
                                    ))
                db.session.commit()

    data = Product.query.all()
    return render_template('home.html', data=data, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                flash('Login successfully', category='success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password ' + user.email)
        else:
            flash('Invalid username', category='danger')
            redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if not user:
            if form.password.data == form.confirm_password.data:
                password_hash: str = generate_password_hash(form.password.data)
                db.session.add(Users(email=form.email.data, password=password_hash))
                db.session.commit()
                flash("Successfully created")
                redirect(url_for('login'))
            else:
                flash('Passwords are not matching')
        else:
            flash('User already exists')
            redirect(url_for('signup'))
    return render_template('signup.html', form=form)


@app.route('/add_product/', methods=['GET', 'POST'])
def add_product():
    db.create_all()
    form = AddForm()
    if form.validate_on_submit():
        db.session.add(Product(title=form.title.data,
                               price=form.price.data,
                               barcode=form.barcode.data,
                               size=form.size.data,
                               image_url=form.image.data,
                               description=form.description.data))
        db.session.commit()

    form.title.data = ''
    form.price.data = ''
    form.barcode.data = ''
    form.size.data = ''
    form.image.data = ''
    form.description.data = ''
    flash('Added successfully')

    return render_template('add_product.html', form=form)


@app.route('/item', methods=['GET', 'POST'])
def item():
    barcode = request.args.get('search', '')
    items = Product.query.filter_by(barcode=barcode).all()
    cart_id = request.args.get('item')
    item_by_id = Product.query.filter_by(id=cart_id)
    return render_template('item.html', items=items, cart_items=item_by_id)


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    form = RemoveFromCart()
    if form.validate_on_submit():
        remove_id = request.args.get('remove')
        item_to_remove = Cart.query.get(remove_id)
        db.session.delete(item_to_remove)
        db.session.commit()
    items = Cart.query.all()
    return render_template('cart.html', items=items, form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404

