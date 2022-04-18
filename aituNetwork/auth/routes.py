from flask import request, render_template, flash

from aituNetwork.auth import auth
from utils import api


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')

    # All fields expected as filled
    barcode = int(request.form.get('barcode'))
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    password = request.form.get('password')
    password_confirm = request.form.get('password-confirm')

    if check_passwords(password, password_confirm):
        result = register_user(barcode, first_name, last_name, password)
        if result:
            return 'main page'

    return render_template('sign_up.html', barcode=int(barcode), first_name=first_name,
                           last_name=last_name, password=password, password_confirm=password_confirm)


@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign_in.html')
        
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        barcode = int(request.form.get('barcode'))
        password = request.form.get('password')
        
        if None in [barcode, password]:
            flash('Not all data was given')
        
        response = api.login(barcode=barcode, password=password)
        print(response)
        
        if response['status'] == 'error':
            flash(response['error'])
        else:
            return 'main page' # placeholder


def check_passwords(password: str, password_confirm: str) -> bool:
    is_ok = True
    if len(password) < 8:
        is_ok = False
        flash('Password length should be more than 7 characters')

    if password != password_confirm:
        is_ok = False
        flash('Passwords does not match')

    return is_ok


# if function returns true: users is registered
# Otherwise, users is not registered
def register_user(barcode: int, first_name: str, last_name: str, password: str) -> bool:
    response = api.find_user_by_barcode(barcode)
    print(response)
    # It means that user is found
    # In that case, we can't register a new user
    if response['status'] == 'ok':
        flash('User with this barcode already registered')
        return False

    # During sending request to an API some error raised
    if response['error'] == 'API error':
        flash('Can\'t connect to API')
        return False
    # User with this barcode is not found
    # In that case, we can register a new user
    if response['error'] == 'User with such barcode not found.':
        api.add_user(barcode, first_name, last_name, password)
        return True
