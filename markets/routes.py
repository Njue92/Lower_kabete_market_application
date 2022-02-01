from markets import app
from flask import render_template, redirect, url_for, flash, request
from markets.models import Item, User, Vendor, City, Stock
from markets.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, Form, StockForm
from markets import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home():  # put application's code here
    return render_template('home.html')


@app.route('/market', methods=['POST', 'GET'])
@login_required
def market():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        # purchase item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for Ksh. {p_item_object.price}",
                      category='success')

            else:
                flash(f"Sorry! You don;t have enough money to purchase {p_item_object.name}", category='danger')
        # selling Item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"You have returned {s_item_object.name} for Ksh. {s_item_object.price}",
                      category='success')
            else:
                flash(f"Sorry! something went wrong in returning {s_item_object.name}", category='danger')

        return redirect(url_for('market'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items,
                               selling_form=selling_form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        attempted_user = User.query.filter_by(username=login_form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=login_form.password.data):
            login_user(attempted_user)
            flash(f'Success! Welcome {attempted_user.username}', category='success')
            return redirect(url_for('market'))
        else:
            flash('Username and password are not a much! Please try again', category='danger')

    if login_form.errors != {}:
        for err_msg in login_form.errors.values():
            print(f'Trouble in login: {err_msg}')

    return render_template('login.html', login_form=login_form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are logged in as {user_to_create.username}!', category='success')
        return redirect(url_for('market'))

    if form.errors != {}:  # if there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error in creating the account: {err_msg} ', category='danger')
    return render_template('register.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category='info')
    return redirect(url_for('home'))


@app.route('/vendor', methods=['POST', 'GET'])
def vendor():
    form = Form()
    form.city.choices = [(city.id, city.name) for city in City.query.filter_by(state='GC').all()]
    if request.method == 'POST':
        if form.validate_on_submit():
            vendor_to_add = Vendor(name=form.name.data,
                                   phone=form.phone.data,
                                   city=form.city.data,
                                   type=form.type.data)
            db.session.add(vendor_to_add)
            db.session.commit()
            flash(f'Your business {vendor_to_add.name} has been added to Business in Lower Kabete', category='success')
        return redirect(url_for('item'))

    return render_template('vendor.html', form=form)


@app.route('/item', methods=['POST', 'GET'])
def item():
    add_form = StockForm()
    all_items = Stock.query.all()
    # add_item = StockForm(request.form.get('add_item'))
    # if request.method == 'POST':
    # if add_form.validate_on_submit():
    #     add_it = Stock(name=add_form.name.data, price=add_form.price.data, barcode=add_form.barcode.data,
    #                    description=add_form.description.data)
    #     db.session.add(add_it)
    #     db.session.commit()
    #     flash(f'Item {add_it.name} added successfully!')
    # if request.method == 'GET':
    if add_form.validate_on_submit():
        item_to_add = Stock(name=add_form.name.data,price=add_form.price.data,barcode=add_form.barcode.data,password=add_form.barcode.data,description=add_form.description.data)
        db.session.add(item_to_add)
        db.session.commit()
        flash(f'Item {item_to_add.name} added to inventory!', category='success')
        return redirect(url_for('home'))
    return render_template('item.html', add_form=add_form, all_items=all_items)
