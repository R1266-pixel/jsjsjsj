from flask import Flask, render_template, request, session, redirect, url_for
import db

app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        numero_contacto = request.form["numero_contacto"]
        usuario = db.Cliente.LOGIN(correo, numero_contacto)
        if usuario:
            session["correo"] = usuario["CORREO"]
            session["role"] = usuario["ROLE"]
            if usuario["ROLE"] == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("cliente_dashboard"))
        return "Credenciales incorrectas"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        numero = request.form["numero"]
        direccion = {
            "cp": request.form["cp"],
            "cuidad": request.form["cuidad"],
            "calle": request.form["calle"],
            "numero": request.form["numero_depto"]
        }
        cliente = db.Cliente(nombre, numero, correo, direccion)
        cliente.CREATE()
        return redirect(url_for("index"))
    return render_template("registrar.html")

@app.route("/recuperar", methods=["GET", "POST"])
def recuperar():
    if request.method == "POST":
        correo = request.form["correo"]
        # Recupera la contraseña del usuario desde la base de datos
        with db.Database() as cur:
            cur.execute("SELECT * FROM cliente WHERE CORREO = %s", (correo,))
            usuario = cur.fetchone()
        if usuario:
            return f"Tu contraseña es: {usuario['contraseña']}"  # Muestra la contraseña (no recomendado en producción)
        return "Correo no encontrado."
    return render_template("recuperar.html")

@app.route("/cliente", methods=["GET"])
def cliente():
    clientes = db.Cliente.READ_ALL()  # Recupera los datos de los clientes
    return render_template("cliente.html", clientes=clientes)




@app.route("/producto", methods=["GET", "POST"])
def producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        color = request.form["color"]
        categoria = request.form["categoria"]
        producto = db.Producto(precio, color, nombre, categoria)
        producto.CREATE()
        return redirect(url_for("producto"))
    productos = db.Producto.READ_ALL()
    return render_template("producto.html", productos=productos)

@app.route("/eliminar_producto/<int:producto_id>", methods=["POST"])
def eliminar_producto(producto_id):
    print(f"Eliminando producto con ID: {producto_id}")  # Depuración
    db.Producto.DELETE(producto_id)
    return redirect(url_for("producto"))



@app.route("/ventas", methods=["GET", "POST"])
def ventas():
    if request.method == "POST":
        cliente_id = request.form["cliente_id"]
        producto_id = request.form["producto_id"]
        cantidad = request.form["cantidad"]
        venta = db.Ventas(cliente_id, producto_id, cantidad)
        venta.CREATE()
        return redirect(url_for("ventas"))
    ventas = db.Ventas.READ_ALL()
    return render_template("ventas.html", ventas=ventas)

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/cliente_dashboard")
def cliente_dashboard():
    return render_template("cliente_dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
