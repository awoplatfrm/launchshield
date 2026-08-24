from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.users import User, db
from app.models.flags import FeatureFlag
from app.models.tenants import Tenant
from sqlalchemy import select
from typing import cast
from app.form import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    current_usr = cast(User, current_user)
    if current_usr.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        company_name = form.company_name.data
        email = form.email.data
        password = form.password.data

        stmt = select(User).where(User.email == email)
        existing_user = db.session.execute(stmt).scalar_one_or_none()
        if existing_user:
            flash("email already registered.", "danger")
            return render_template("auth/register.html", form=form)

        new_tenant = Tenant(name=company_name)
        db.session.add(new_tenant)
        db.session.flush()

        hashed_pd = generate_password_hash(password, method="scrypt")
        new_user = User(
            email=email, password_hash=hashed_pd, tenant_id=new_tenant.id, is_admin=True
        )
        db.session.add(new_user)

        db.session.commit()
        login_user(new_user)
        flash("registration successful", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
# REMOVED @login_required here!
def login():
    current_usr = cast(User, current_user)
    if current_usr.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        stmt = select(User).where(User.email == email)
        existing_user = db.session.execute(stmt).scalar_one_or_none()

        if not existing_user or not check_password_hash(
            existing_user.password_hash, password
        ):
            flash("invalid email or password", "danger")
            # Render template on failure so form errors display
            return render_template("auth/login.html", form=form)

        login_user(existing_user)
        return redirect(url_for("dashboard.index"))

    # FIX: Render template on GET request instead of redirecting
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("you have been logged out.", "info")
    return redirect(url_for("auth.login"))
