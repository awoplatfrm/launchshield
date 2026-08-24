from flask_login import login_required, current_user
from typing import cast
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.form import CreateFlagForm, ToggleFlagForm
from app.models.users import User
from app.models.tenants import db
from app.models.flags import FeatureFlag
from sqlalchemy import select

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def index():
    create_form = CreateFlagForm()
    toggle_form = ToggleFlagForm()
    user = cast(User, current_user)
    if create_form.validate_on_submit():
        flag_key = create_form.key.data.lower().strip()
        existing = db.session.execute(
            select(FeatureFlag).where(
                FeatureFlag.tenant_id == user.tenant_id, FeatureFlag.key == flag_key
            )
        ).scalar_one_or_none()

        if existing:
            flash(f"Flag key {flag_key} already exist", "danger ")
        else:
            new_flag_key = FeatureFlag(
                name=create_form.name.data,
                description=create_form.description.data,
                key=create_form.key.data,
                is_enabled=create_form.is_enabled.data,
                tenant_id=user.tenant_id,
            )
            db.session.add(new_flag_key)
            db.session.commit()
            flash(f"Flag key {flag_key} created.", "success")
        return redirect(url_for("dashboard.index"))
    flag = (
        db.session.execute(
            select(FeatureFlag)
            .where(FeatureFlag.tenant_id == user.tenant_id)
            .order_by(FeatureFlag.created_at.desc())
        )
        .scalars()
        .all()
    )

    return render_template(
        "dashboard/index.html",
        flag=flag,
        create_form=create_form,
        toggle_form=toggle_form,
    )


@dashboard_bp.route("flags/<int:flag_id>/toggle", methods=["POST"])
@login_required
def flag_toggle(flag_id: int):
    toggle_form = ToggleFlagForm()
    user = cast(User, current_user)

    if toggle_form.validate_on_submit():

        flag = db.session.execute(
            select(FeatureFlag).where(
                FeatureFlag.id == flag_id, FeatureFlag.tenant_id == user.tenant_id
            )
        ).scalar_one_or_none()
        if not flag:
            flash("flag not found or unauthorized", "danger")
            return redirect(url_for("dashboard.index"))
        flag.is_enabled = not flag.is_enabled
        db.session.commit()

        status = "enabled" if flag.is_enabled else "disabled"
        flash(f"flag {flag_id} is now {status}", "info")
    return redirect(url_for("dashboard.index"))
