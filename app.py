from flask import Flask, render_template, request
import yagmail
import utils
app= Flask(__name__)

@app.route('/')
def hola_mundo():
   return render_template('index.html',titulo='Inicio de Sesión')

@app.route('/login',methods=['POST','GET'])
def login():
    usuarioAdmin= 'admin'
    contrasenaAdmin= '0000'
    #try:
    if request.method == 'POST':
        usuario=request.form['usuario'] #sacar los campos del form
        contrasena=request.form['contrasena']
        if usuario==usuarioAdmin:
            #if contrasena==contrasenaAdmin:
            return render_template('portal.html',header='CAFETERÍA BRIOCHE')
    return render_template('index.html',titulo='Inicio de Sesión')

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
                return 'revisa tu correo='+email
            else:
                return 'Error Correo no cumple con lo exigido'                      
        else:
            return 'Error faltan datos para validar'
 
    except:
        return render_template('recuperarContrasena.html')

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
                if utils.isEmailValid(email):
                    if utils.isUsernameValid(usuario):
                            if utils.isPasswordValid(clave):
                                yag=yagmail.SMTP('danielrendon@uninorte.edu.co', 'Desde14151617') 
                                yag.send(to=email,subject='Validar Cuenta',
                                contents='Bienvenido usa este link para activar tu cuenta')  
                                return 'revisa tu correo='+email
                            else:
                                return 'Error Clave no cumple con lo exigido'    
                    else:
                        return 'Error usuario no cumple con lo exigido'
                else:
                    return 'Error Correo no cumple con lo exigido'
            if request.form['submit'] == 'Cancelar':
                return render_template('portal.html',header='CAFETERÍA BRIOCHE')
        else:
            return 'Error faltan datos para validar'
    
    except:
        return render_template('crearsuarioCajero.html')
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