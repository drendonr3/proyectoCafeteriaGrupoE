from flask import Flask, render_template, request
import yagmail
import utils
app= Flask(__name__)

@app.route('/')
def hola_mundo():
   return render_template('index.html')

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
            return render_template('portal.html')
    return render_template('index.html')
    #except:
     #   return render_template('index.html')


@app.route('/recurperarContrasena',methods=['POST','GET'])
def recurperarContrasena():
    return render_template('recuperarContrasena.html')

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
    return render_template('crearUsuarioCajero.html')

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
                return render_template('portal.html')
        else:
            return 'Error faltan datos para validar'
    
    except:
        return render_template('crearsuarioCajero.html')
@app.route('/gestionarProducto',methods=['GET', 'POST'])
def gestionarProducto():
    return render_template('gestionarProducto.html')

@app.route('/accionGestionarProducto',methods=['GET', 'POST'])
def accionGestionarProducto():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Nuevo Producto':
                return render_template('nuevoProducto.html')
               
            if request.form['submit'] == 'Cancelar':
                return render_template('portal.html')
        else:
            return 'Error faltan datos para validar'
    
    except:
        return render_template('portal.html')

@app.route('/crearProducto',methods=['GET', 'POST'])
def crearProducto():
    #ssss
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Crear':
                return render_template('gestionarProducto.html')
               
            if request.form['submit'] == 'Cancelar':
                return render_template('gestionarProducto.html')
        else:
            return 'Error faltan datos para validar'
    
    except:
        return render_template('portal.html')

