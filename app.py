from flask import Flask, render_template, request,flash,redirect,session
import yagmail
import utils
import os
from db import *
import functools
app= Flask(__name__)
app.secret_key=os.urandom(24)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'user_id' in session :
            return redirect('/')
        return view()
    return wrapped_view

def login_admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'user_id' in session :
            return redirect('/')
        if not session['type']=='admin':
            return redirect('/')
        return view()
    return wrapped_view
@app.route('/')
def index():    
    if not 'user_id' in session :
        return render_template('index.html',titulo='Inicio de Sesión')
    if not 'user' in session :
        return render_template('index.html',titulo='Inicio de Sesión')
    return render_template('portal.html',header='CAFETERÍA BRIOCHE')
    
@app.route('/cerrarSesion')
def cerrarSesion():
    session["user"] = None
    session["user_id"] = None
    session["auth"] = None
    session["type"] = None
    session.clear()
    return redirect('/')

@app.route('/login',methods=['POST','GET'])
def login():
    try:
        if request.method == 'POST':
            usuario=request.form['usuario'] #sacar los campos del form
            contrasena=request.form['contrasena']
            if usuario=="":
                flash('Campo de Usuario Vacío')
                return redirect('/')
            else:
                if contrasena=="":
                    flash('Campo de Contraseña Vacío')
                    flash('baduser---'+usuario)
                    return redirect('/')
                else:
                    db= Db('db/cafeteriaBriocheDb.db')
                    conexion = db.get_db('db/cafeteriaBriocheDb.db') # abre la conexion
                    cur=conexion.cursor()
                    cur.execute("SELECT * FROM usuarios INNER JOIN tipos_usuario ON usuarios.tipo=tipos_usuario.id WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
                    reg=cur.fetchone()
                    if  reg is None:
                        error = 'Usuario o contraseña inválidos'
                        flash('Usuario o Contraseña Incorrecto')
                        flash('baduser---'+usuario)
                        db.close_db()
                        return redirect('/')
                    print(reg)
                    session.clear()
                    session["user"] = reg[1]
                    session["user_id"] = reg[0]
                    session["auth"] = 1
                    session["type"] = reg[6]
                    db.close_db()
                    return render_template('portal.html',header='CAFETERÍA BRIOCHE')
        else:
            return redirect('/')
    except Exception as inst:
        return redirect('/')
    


@app.route('/recurperarContrasena',methods=['POST','GET'])
def recurperarContrasena():
    return render_template('recuperarContrasena.html',titulo='Recuperar Contraseña')

@app.route('/enviarCorreoRecuperacion', methods=['GET', 'POST'])
def enviarCorreoRecuperacion():
    try:
        if request.method == 'POST':
            email=request.form['correo']
            if utils.isEmailValid(email):
                yag=yagmail.SMTP('danielrendon@uninorte.edu.co', 'Desde14151617') 
                yag.send(to=email,subject='Recuperar Contraseña',
                contents='Usa este link para recuperar tu contraseña')  
                flash('success')
                return redirect('/recurperarContrasena') 
            else:
                flash('Ingrese una Dirección de Correo Válida')
                return redirect('/recurperarContrasena')                  
        else:
            return render_template('recuperarContrasena.html',titulo='Recuperar Contraseña')
 
    except:
        return render_template('recuperarContrasena.html',titulo='Recuperar Contraseña')

@app.route('/crearUsuarioCajero', methods=['GET', 'POST'])
@login_admin_required
def crearUsuarioCajero():
    return render_template('crearUsuarioCajero.html',titulo='Crear Usuario',header='CAFETERÍA BRIOCHE')

@app.route('/enviarCorreoNuevo', methods=['GET', 'POST'])
@login_admin_required
def enviarCorreoNuevo():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Crear':
                usuario=request.form['usuario'] #sacar los campos del form
                clave=request.form['contrasena']
                email=request.form['correo']
                if utils.isUsernameValid(usuario):
                    if utils.isEmailValid(email):
                        if utils.isPasswordValid(clave):
                            db= Db('db/cafeteriaBriocheDb.db')
                            conexion = db.get_db('db/cafeteriaBriocheDb.db') # abre la conexion
                            cur=conexion.cursor()
                            cur.execute("SELECT * FROM usuarios WHERE usuario ='"+usuario + "'")
                            reg=cur.fetchone()
                            if  reg is not None:
                                flash('Ya Existe Este Usuario')
                                flash('baduser---'+usuario+'---'+email)
                                db.close_db()
                                return redirect('/crearUsuarioCajero')
                                
                            cur=conexion.cursor()
                            cur.execute("SELECT * FROM usuarios WHERE correo ='" + email + "'")
                            reg=cur.fetchone()
                            if  reg is not None:
                                flash('Ya Existe Este Correo')
                                flash('baduser---'+usuario+'---'+email)
                                db.close_db()
                                return redirect('/crearUsuarioCajero')
                            db.close_db()
                            db= Db('db/cafeteriaBriocheDb.db')
                            conexion = db.get_db('db/cafeteriaBriocheDb.db') # abre la conexion
                            cur=conexion.cursor()
                            cur.execute('INSERT INTO usuarios (usuario, correo, contrasena,tipo) VALUES (?,?,?,?)',(usuario, email, clave,1))
                            conexion.commit()
                            db.close_db()
                            yag=yagmail.SMTP('danielrendon@uninorte.edu.co', 'Desde14151617') 
                            yag.send(to=email,subject='Validar Cuenta',
                            contents='Bienvenido usa este link para activar tu cuenta')
                            flash('success')
                            return redirect('/crearUsuarioCajero') 
                        else:
                            flash('La Contraseña no Cumple con lo Exigido')
                            flash('baduser---'+usuario+'---'+email)
                            return redirect('/crearUsuarioCajero') 
                    else:
                        flash('El Correo no Cumple con lo Exigido')
                        flash('baduser---'+usuario+'---'+email)
                        return redirect('/crearUsuarioCajero') 
                else:
                    flash('El Usuario no Cumple con lo Exigido')
                    flash('baduser---'+usuario+'---'+email)
                    return redirect('/crearUsuarioCajero') 
            if request.form['submit'] == 'Cancelar':
                return render_template('portal.html',header='CAFETERÍA BRIOCHE')
        else:
            return crearUsuarioCajero()
    
    except:
        return crearUsuarioCajero

@app.route('/gestionarProducto',methods=['GET', 'POST'])
@login_required
def gestionarProducto():
    return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')

@app.route('/accionGestionarProducto',methods=['GET', 'POST'])
@login_required
def accionGestionarProducto():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Nuevo Producto':
                return render_template('nuevoProducto.html',titulo='Nuevo Producto',header='NUEVO PRODUCTO')
               
            if request.form['submit'] == 'Cancelar':
                return render_template('portal.html',header='CAFETERÍA BRIOCHE')
        else:
            return 'Error faltan datos para validar'
    
    except:
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

@app.route('/crearProducto',methods=['GET', 'POST'])
@login_required
def crearProducto():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Crear':
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
               
            if request.form['submit'] == 'Cancelar':
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
        else:
            return 'Error faltan datos para validar'
    
    except:
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

@app.route('/eliminarModificar',methods=['GET', 'POST'])
@login_required
def eliminarModificar():
    return render_template('eliminarModificar.html',titulo='Eliminar y/o Modificar Producto',header='ELIMINAR/MODIFICAR PRODUCTO')

@app.route('/acctionEliminarModificar',methods=['GET', 'POST'])
@login_required
def acctionEliminarModificar():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Modificar':
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
               
            if request.form['submit'] == 'Eliminar':
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
            
            if request.form['submit'] == 'Cancelar':
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
        else:
            return 'Error faltan datos para validar'
    
    except:
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')



@app.route('/informeVentas',methods=['GET', 'POST'])
@login_admin_required
def informeVentas():
    return render_template('informeVentas.html',titulo='Informe Ventas',header='INFORME VENTAS')

@app.route('/accionInformeVentas',methods=['GET', 'POST'])
@login_admin_required
def accionInformeVentas():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Recalcular':
                return render_template('informeVentas.html',titulo='Informe Ventas',header='INFORME VENTAS')

            if request.form['submit'] == 'Generar':
                return render_template('portal.html',header='CAFETERÍA BRIOCHE')
            
            if request.form['submit'] == 'Cancelar':
                return render_template('portal.html',header='CAFETERÍA BRIOCHE')
            
        else:
            return 'Error faltan datos para validar'
    
    except:
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

@app.route('/gestionarFacturas',methods=['GET', 'POST'])
@login_required
def gestionarFacturas():
    return render_template('gestionarVentas.html',titulo='Gestionar Facturas',header='GESTIONAR FACTURAS')

@app.route('/accionGestionarFacturas',methods=['GET', 'POST'])
@login_required
def accionGestionarFacturas():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Nueva Factura':
                return render_template('nuevaFactura.html',titulo='Nueva Factura',header='NUEVA FACTURA')

            if request.form['submit'] == 'Cancelar':
                return render_template('portal.html',header='CAFETERÍA BRIOCHE')
        else:
            return render_template('portal.html',header='CAFETERÍA BRIOCHE')
    
    except:
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

@app.route('/nuevaFactura',methods=['GET', 'POST'])
@login_required
def nuevaFactura():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Total':
                return render_template('total.html',titulo='Total Factura',header='TOTAL FACTURA')

            if request.form['submit'] == 'Cancelar':
                return render_template('gestionarVentas.html',titulo='Gestionar Facturas',header='GESTIONAR FACTURAS')
        else:
            return 'Error faltan datos para validar'
    
    except:
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

@app.route('/total',methods=['GET', 'POST'])
@login_required
def total():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Generar':
                return render_template('gestionarVentas.html',titulo='Gestionar Facturas',header='GESTIONAR FACTURAS')

            if request.form['submit'] == 'Cancelar':
                return render_template('nuevaFactura.html',titulo='Nueva Factura',header='NUEVA FACTURA')
        else:
            return 'Error faltan datos para validar'
    
    except:
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

@app.route('/verFactura',methods=['GET', 'POST'])
@login_required
def verFactura():
    return render_template('verFactura.html',titulo='Ver Factura',header='VER FACTURA')