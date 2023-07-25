from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms import URLField, EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError


class SignupForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    signup = SubmitField('Submit')


class SignInForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Submit')


class AddForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    barcode = StringField('Barcode', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])
    image = URLField('Image URL', validators=[DataRequired()])
    description = TextAreaField('Description')
    category = SelectField('Category', choices=('Shoes', 'Hats', 'Clothes'))
    submit = SubmitField('submit')

    def validate_barcode(barcode):
        product = Product.query.filter_by(barcode=barcode.data).first()
        if product:
            raise ValidationError('Barcode already exists!')


class SearchForm(FlaskForm):
    search = StringField("search", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddToCart(FlaskForm):
    addToCart = SubmitField('Add')


class RemoveFromCart(FlaskForm):
    remove = SubmitField()

