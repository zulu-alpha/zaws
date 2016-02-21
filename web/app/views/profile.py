from flask import render_template, request, flash, redirect, url_for

from .. import app, flask_login
from ..util.permission import owns_steam_id_page

from ..models.users import User

from ..forms.profile import ArmaName, TSID


@app.route('/profile/<steam_id>')
@flask_login.login_required
def profile(steam_id):
    """The profile page of the given user by steam ID.

    :param steam_id: The steam ID of the user in question
    :return: render_template() or redirect()
    """
    user = User.by_steam_id(steam_id)
    is_owner = user.id == flask_login.current_user.id
    return render_template('profile/view.html', user=user, is_owner=is_owner)


@app.route('/profile/<steam_id>/update/arma-name', methods=['GET', 'POST'])
@flask_login.login_required
@owns_steam_id_page()
def update_arma_name(steam_id):
    """Updates the Arma name of the given user by steam id.

    :param steam_id: The steam ID of the user in question
    :return: render_template() or redirect()
    """
    user = User.by_steam_id(steam_id)

    form = ArmaName()

    # Add user id to form to allow for validation
    if request.method == 'POST':
        form.exclude_id.data = user.id
    if form.validate_on_submit():
        if user.update_arma_name(form.arma_name.data):
            flash('Arma name successfully changed!', 'success')
        else:
            flash('Arma name failed to update for some reason!', 'danger')
        return redirect(url_for('profile', steam_id=steam_id))

    return render_template('profile/update_name.html', user=user, form=form)


@app.route('/profile/<steam_id>/update/ts-id', methods=['GET', 'POST'])
@flask_login.login_required
@owns_steam_id_page()
def update_ts_id(steam_id):
    """Updates the Arma name of the given user by steam id.

    :param steam_id: The steam ID of the user in question
    :return: render_template() or redirect()
    """
    user = User.by_steam_id(steam_id)

    form = TSID()

    # Add user id to form to allow for validation
    if form.validate_on_submit():
        if user.add_ts_id(form.ts_id.data):
            flash('TeamSpeak ID successfully added!', 'success')
        else:
            flash('TeamSpeak ID failed to be added for some reason!', 'danger')
        return redirect(url_for('profile', steam_id=steam_id))

    return render_template('profile/update_ts_id.html', user=user, form=form)
