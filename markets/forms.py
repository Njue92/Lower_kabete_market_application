from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, length
from markets.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email')

    # def validate_password(self, password_to_check):
    #     password = User.query.filter_by(password=password_to_check).first()
    #     if password:
    #         raise ValidationError('Username already exists! Please try a different username')

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')


class VendorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    location = SelectField('location', choices=[('GA','Gacio'),('KNG','Kingeroo'),('wg','Wangige')])
    exact_location = SelectField('Exact location', choices=[])
    # phone = StringField(label='Mobile number', validators=[DataRequired()])
    # item = StringField(label='Item name', validators=[DataRequired()])
    # price = StringField(label='Price', validators=[DataRequired()])
    # barcode = StringField(label= 'Barcode')
    # description = StringField(label='Description')
    submit = SubmitField(label='Submit')


class Form(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    phone = IntegerField(label='Mobile number', validators=[DataRequired()])
    state = SelectField(label='Location of business', choices=[('KE','Kingeroo'),('GA','Gacio'), ('WA', 'Wangige')])
    type = SelectField (label='Type of business', choices=['Fast food','Electronics shop', 'Clothing', 'Butchery'])
    city = SelectField('city', choices=[])


class StockForm(FlaskForm):
    name = StringField(label='Item', validators=[DataRequired()])
    price = IntegerField(label='Price (Ksh.)', validators=[DataRequired()])
    barcode = StringField(label='Barcode',validators=[DataRequired()])
    description = TextAreaField(label='Description')
    submit = SubmitField(label='Add item to inventory')


class PutItemForm(FlaskForm):
    submit = SubmitField(label='Add Item to Market')