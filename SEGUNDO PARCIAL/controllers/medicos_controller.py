from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Medico

bp_medicos = Blueprint("medicos", __name__, url_prefix="/medicos")


@bp_medicos.route("/")
def list_medicos():
    medicos = Medico.query.order_by(Medico.nombre).all()
    return render_template("medicos/medicos.html", medicos=medicos)


@bp_medicos.route("/crear", methods=["GET", "POST"])
def create_medico():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        especialidad = request.form.get("especialidad", "").strip()
        if not nombre or not especialidad:
            flash("Debe completar nombre y especialidad.", "danger")
        else:
            medico = Medico(nombre=nombre, especialidad=especialidad)
            db.session.add(medico)
            db.session.commit()
            flash("Médico creado correctamente.", "success")
            return redirect(url_for("medicos.list_medicos"))
    return render_template("medicos/medico_form.html", medico=None)


@bp_medicos.route("/<int:medico_id>/editar", methods=["GET", "POST"])
def edit_medico(medico_id):
    medico = Medico.query.get_or_404(medico_id)
    if request.method == "POST":
        medico.nombre = request.form.get("nombre", medico.nombre).strip()
        medico.especialidad = request.form.get("especialidad", medico.especialidad).strip()
        if not medico.nombre or not medico.especialidad:
            flash("Debe completar nombre y especialidad.", "danger")
        else:
            db.session.commit()
            flash("Médico actualizado.", "success")
            return redirect(url_for("medicos.list_medicos"))
    return render_template("medicos/medico_form.html", medico=medico)


@bp_medicos.route("/<int:medico_id>/eliminar", methods=["POST"])
def delete_medico(medico_id):
    medico = Medico.query.get_or_404(medico_id)
    db.session.delete(medico)
    db.session.commit()
    flash("Médico eliminado.", "warning")
    return redirect(url_for("medicos.list_medicos"))
