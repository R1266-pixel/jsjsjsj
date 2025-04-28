from flask import Blueprint,render_template,request,redirect,url_for
from db import Cliente


cliente=Blueprint("cliente",__name__)

@cliente.route("/")
def ver_clientes():
    lista=Cliente.READ_ALL()
    return render_template("cliente.html", lista=lista)



@cliente.route("/<int:id>")
def ver_cliente(id):
    lista=Cliente.READ_ONE(id)
    return render_template("cliente.html",lista=lista)

@cliente.route("/agregar")
def agregar_cliente():
    return render_template("agregar_cliente.html")

@cliente.route("/agregar",methods=["POST"]) 
def agregar_cliente_post():
    nombre=request.form["nombre"]
    numero=request.form["numero"]
    correo=request.form["correo"]
    cp=request.form["cp"]
    cuidad=request.form["cuidad"]
    calle=request.form["calle"]
    numero_depto=request.form["numero_depto"]
    direccion={"cp":cp,"cuidad":cuidad,"calle":calle,"numero":numero_depto}
    cliente=Cliente(nombre,numero,correo,direccion)
    cliente.CREATE()
    return redirect(url_for("cliente.ver_clientes"))

@cliente.route("/editar/<int:id>")
def editar_cliente(id):
    lista=Cliente.READ_ONE(id)
    return render_template("editar_cliente.html",lista=lista)


@cliente.route("/editar/<int:id>",methods=["POST"])
def editar_cliente_post(id):
    nombre=request.form["nombre"]
    numero=request.form["numero"]
    correo=request.form["correo"]
    cp=request.form["cp"]
    cuidad=request.form["cuidad"]
    calle=request.form["calle"]
    numero_calle=request.form["numero_calle"]
    direccion={"cp":cp,"cuidad":cuidad,"calle":calle,"numero":numero_calle}
    cliente=Cliente(nombre,numero,correo,direccion)
    cliente.UPDATE(id)
    return render_template("editar_cliente.html")

@cliente.route("/eliminar/<int:id>")
def eliminar_cliente(id):
    Cliente.DELETE(id)
    return render_template("cliente.html")

