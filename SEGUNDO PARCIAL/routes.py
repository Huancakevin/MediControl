from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from app import db
from models import Medico, Paciente, Cita


def init_routes(app):
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/medicos")
    def list_medicos():
        medicos = Medico.query.order_by(Medico.nombre).all()
        return render_template("medicos.html", medicos=medicos)

    @app.route("/medicos/crear", methods=["GET", "POST"])
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
                return redirect(url_for("list_medicos"))
        return render_template("medico_form.html", medico=None)

    @app.route("/medicos/<int:medico_id>/editar", methods=["GET", "POST"])
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
                return redirect(url_for("list_medicos"))
        return render_template("medico_form.html", medico=medico)

    @app.route("/medicos/<int:medico_id>/eliminar", methods=["POST"])
    def delete_medico(medico_id):
        medico = Medico.query.get_or_404(medico_id)
        db.session.delete(medico)
        db.session.commit()
        flash("Médico eliminado.", "warning")
        return redirect(url_for("list_medicos"))

    @app.route("/pacientes")
    def list_pacientes():
        pacientes = Paciente.query.order_by(Paciente.nombre).all()
        return render_template("pacientes.html", pacientes=pacientes)

    @app.route("/pacientes/crear", methods=["GET", "POST"])
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
                return redirect(url_for("list_pacientes"))
        return render_template("paciente_form.html", paciente=None)

    @app.route("/pacientes/<int:paciente_id>/editar", methods=["GET", "POST"])
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
                return redirect(url_for("list_pacientes"))
        return render_template("paciente_form.html", paciente=paciente)

    @app.route("/pacientes/<int:paciente_id>/eliminar", methods=["POST"])
    def delete_paciente(paciente_id):
        paciente = Paciente.query.get_or_404(paciente_id)
        db.session.delete(paciente)
        db.session.commit()
        flash("Paciente eliminado.", "warning")
        return redirect(url_for("list_pacientes"))

    @app.route("/citas")
    def list_citas():
        citas = Cita.query.order_by(Cita.fecha, Cita.hora).all()
        return render_template("citas.html", citas=citas)

    @app.route("/citas/crear", methods=["GET", "POST"])
    def create_cita():
        medicos = Medico.query.order_by(Medico.nombre).all()
        pacientes = Paciente.query.order_by(Paciente.nombre).all()
        if request.method == "POST":
            fecha = request.form.get("fecha")
            hora = request.form.get("hora")
            medico_id = request.form.get("medico_id")
            paciente_id = request.form.get("paciente_id")
            if not fecha or not hora or not medico_id or not paciente_id:
                flash("Debe completar todos los campos de la cita.", "danger")
            else:
                cita = Cita(
                    fecha=datetime.strptime(fecha, "%Y-%m-%d").date(),
                    hora=datetime.strptime(hora, "%H:%M").time(),
                    medico_id=int(medico_id),
                    paciente_id=int(paciente_id),
                )
                db.session.add(cita)
                db.session.commit()
                flash("Cita creada correctamente.", "success")
                return redirect(url_for("list_citas"))
        return render_template("cita_form.html", cita=None, medicos=medicos, pacientes=pacientes)

    @app.route("/citas/<int:cita_id>/editar", methods=["GET", "POST"])
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
                flash("Debe completar todos los campos de la cita.", "danger")
            else:
                cita.fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
                cita.hora = datetime.strptime(hora, "%H:%M").time()
                cita.medico_id = int(medico_id)
                cita.paciente_id = int(paciente_id)
                db.session.commit()
                flash("Cita actualizada.", "success")
                return redirect(url_for("list_citas"))
        return render_template(
            "cita_form.html",
            cita=cita,
            medicos=medicos,
            pacientes=pacientes,
        )

    @app.route("/citas/<int:cita_id>/eliminar", methods=["POST"])
    def delete_cita(cita_id):
        cita = Cita.query.get_or_404(cita_id)
        db.session.delete(cita)
        db.session.commit()
        flash("Cita eliminada.", "warning")
        return redirect(url_for("list_citas"))
