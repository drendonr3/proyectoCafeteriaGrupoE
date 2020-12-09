from flask import Flask, render_template, request,flash,redirect,session
import yagmail
import utils
import os
from usuarios import usuarios
app= Flask(__name__)
app.secret_key=os.urandom(24)
@app.route('/')
def index():
    return render_template('index.html',titulo='Inicio de Sesión')
    
@app.route('/cerrarSesion')
def cerrarSesion():
    session.clear()
    return redirect('/')

@app.route('/login',methods=['POST','GET'])
def login():
    #try:
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
                for diccionario in usuarios:
                    if diccionario['usuario']==usuario and contrasena==diccionario['contrasena']:
                        session.clear()
                        session["user"] = usuario
                        session["auth"] = 1
                        session["type"] = diccionario['tipo']
                        return render_template('portal.html',header='CAFETERÍA BRIOCHE')
                flash('Usuario o Contraseña Incorrecto')
                flash('baduser---'+usuario)
                return redirect('/')
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
def crearUsuarioCajero():
    return render_template('crearUsuarioCajero.html',titulo='Crear Usuario',header='CAFETERÍA BRIOCHE')

@app.route('/enviarCorreoNuevo', methods=['GET', 'POST'])
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
            return render_template('crearUsuarioCajero.html')
    
    except:
        return render_template('crearUsuarioCajero.html')
@app.route('/gestionarProducto',methods=['GET', 'POST'])
def gestionarProducto():
    return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')

@app.route('/accionGestionarProducto',methods=['GET', 'POST'])
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
def eliminarModificar():
    return render_template('eliminarModificar.html',titulo='Eliminar y/o Modificar Producto',header='ELIMINAR/MODIFICAR PRODUCTO')

@app.route('/acctionEliminarModificar',methods=['GET', 'POST'])
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
def informeVentas():
    return render_template('informeVentas.html',titulo='Informe Ventas',header='INFORME VENTAS')

@app.route('/accionInformeVentas',methods=['GET', 'POST'])
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
def gestionarFacturas():
    return render_template('gestionarVentas.html',titulo='Gestionar Facturas',header='GESTIONAR FACTURAS')

@app.route('/accionGestionarFacturas',methods=['GET', 'POST'])
def accionGestionarFacturas():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Nueva Factura':
                return render_template('nuevaFactura.html',titulo='Nueva Factura',header='NUEVA FACTURA')

            if request.form['submit'] == 'Cancelar':
                return render_template('portal.html',header='CAFETERÍA BRIOCHE')
        else:
            return 'Error faltan datos para validar'
    
    except:
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

@app.route('/nuevaFactura',methods=['GET', 'POST'])
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
def verFactura():
    return render_template('verFactura.html',titulo='Ver Factura',header='VER FACTURA')