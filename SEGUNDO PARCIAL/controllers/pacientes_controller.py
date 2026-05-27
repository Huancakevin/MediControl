from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Paciente

bp_pacientes = Blueprint("pacientes", __name__, url_prefix="/pacientes")


@bp_pacientes.route("/")
def list_pacientes():
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    return render_template("pacientes/pacientes.html", pacientes=pacientes)


@bp_pacientes.route("/crear", methods=["GET", "POST"])
def create_paciente():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if not nombre or not telefono:
            flash("Debe completar nombre y teléfono.", "danger")
        else:
            paciente = Paciente(nombre=nombre, telefono=telefono)
            db.session.add(paciente)
            db.session.commit()
            flash("Paciente creado correctamente.", "success")
            return redirect(url_for("pacientes.list_pacientes"))
    return render_template("pacientes/paciente_form.html", paciente=None)


@bp_pacientes.route("/<int:paciente_id>/editar", methods=["GET", "POST"])
def edit_paciente(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    if request.method == "POST":
        paciente.nombre = request.form.get("nombre", paciente.nombre).strip()
        paciente.telefono = request.form.get("telefono", paciente.telefono).strip()
        if not paciente.nombre or not paciente.telefono:
            flash("Debe completar nombre y teléfono.", "danger")
        else:
            db.session.commit()
            flash("Paciente actualizado.", "success")
            return redirect(url_for("pacientes.list_pacientes"))
    return render_template("pacientes/paciente_form.html", paciente=paciente)


@bp_pacientes.route("/<int:paciente_id>/eliminar", methods=["POST"])
def delete_paciente(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    db.session.delete(paciente)
    db.session.commit()
    flash("Paciente eliminado.", "warning")
    return redirect(url_for("pacientes.list_pacientes"))
