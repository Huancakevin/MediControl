from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Cita, Medico, Paciente

bp_citas = Blueprint("citas", __name__, url_prefix="/citas")


@bp_citas.route("/")
def list_citas():
    citas = Cita.query.order_by(Cita.fecha, Cita.hora).all()
    return render_template("consultas/consultas.html", citas=citas)


@bp_citas.route("/crear", methods=["GET", "POST"])
def create_cita():
    medicos = Medico.query.order_by(Medico.nombre).all()
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    if request.method == "POST":
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")
        medico_id = request.form.get("medico_id")
        paciente_id = request.form.get("paciente_id")
        if not fecha or not hora or not medico_id or not paciente_id:
            flash("Debe completar todos los campos de la consulta.", "danger")
        else:
            cita = Cita(
                fecha=datetime.strptime(fecha, "%Y-%m-%d").date(),
                hora=datetime.strptime(hora, "%H:%M").time(),
                medico_id=int(medico_id),
                paciente_id=int(paciente_id),
            )
            db.session.add(cita)
            db.session.commit()
            flash("Consulta creada correctamente.", "success")
            return redirect(url_for("citas.list_citas"))
    return render_template("consultas/consulta_form.html", cita=None, medicos=medicos, pacientes=pacientes)


@bp_citas.route("/<int:cita_id>/editar", methods=["GET", "POST"])
def edit_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    medicos = Medico.query.order_by(Medico.nombre).all()
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    if request.method == "POST":
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")
        medico_id = request.form.get("medico_id")
        paciente_id = request.form.get("paciente_id")
        if not fecha or not hora or not medico_id or not paciente_id:
            flash("Debe completar todos los campos de la consulta.", "danger")
        else:
            cita.fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            cita.hora = datetime.strptime(hora, "%H:%M").time()
            cita.medico_id = int(medico_id)
            cita.paciente_id = int(paciente_id)
            db.session.commit()
            flash("Consulta actualizada.", "success")
            return redirect(url_for("citas.list_citas"))
    return render_template(
        "consultas/consulta_form.html",
        cita=cita,
        medicos=medicos,
        pacientes=pacientes,
    )


@bp_citas.route("/<int:cita_id>/eliminar", methods=["POST"])
def delete_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    db.session.delete(cita)
    db.session.commit()
    flash("Consulta eliminada.", "warning")
    return redirect(url_for("citas.list_citas"))
