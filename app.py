from flask import Flask, render_template, request,flash,redirect,session,url_for,make_response
import yagmail
import utils
import os
from db import *
import functools
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import pdfkit

app= Flask(__name__)
app.secret_key=os.urandom(24)
#app.run( host='127.0.0.1', port =443, ssl_context=('micertificado.pem', 'llaveprivada.pem'))
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
        if not 'user_id' in session:
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
                    db= Db()
                    cur=db.conexion.cursor()
                    cur.execute("SELECT * FROM usuarios INNER JOIN tipos_usuario ON usuarios.tipo=tipos_usuario.id WHERE usuario = ?", (usuario,))
                    reg=cur.fetchone()
                    if  reg is None or not check_password_hash(reg[2],contrasena):
                        error = 'Usuario o contraseña inválidos'
                        flash('Usuario o Contraseña Incorrecto')
                        flash('baduser---'+usuario)
                        db.close_db()
                        return redirect('/')
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
                            db= Db()
                            print(-5)
                            cur=db.conexion.cursor()
                            print(-4)
                            cur.execute("SELECT * FROM usuarios WHERE usuario =?",(usuario,))
                            reg=cur.fetchone()
                            print(-3)
                            if  reg is not None:
                                flash('Ya Existe Este Usuario')
                                flash('baduser---'+usuario+'---'+email)
                                db.close_db()
                                return redirect('/crearUsuarioCajero')
                            db= Db()
                            print(-2)
                            cur=db.conexion.cursor()
                            print(-1)
                            cur.execute("SELECT * FROM usuarios WHERE correo =?", (email,))
                            reg=cur.fetchone()
                            if  reg is not None:
                                flash('Ya Existe Este Correo')
                                flash('baduser---'+usuario+'---'+email)
                                db.close_db()
                                return redirect('/crearUsuarioCajero')
                            db.close_db()
                            db= Db()
                            cur=db.conexion.cursor()
                            print(0)
                            hashedClave= generate_password_hash(clave)
                            print(1)
                            cur.execute('INSERT INTO usuarios (usuario, correo, contrasena,tipo) VALUES (?,?,?,?)',(usuario, email, hashedClave,1))
                            print(2)
                            db.conexion.commit()
                            print(3)
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
            return render_template('crearUsuarioCajero.html',titulo='Crear Usuario',header='CAFETERÍA BRIOCHE')
    
    except:
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

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
                db= Db()
                cur=db.conexion.cursor()
                cur.execute("SELECT nombre FROM categorias")
                reg=cur.fetchall()
                if reg is None:
                    return render_template('nuevoProducto.html',titulo='Nuevo Producto',header='NUEVO PRODUCTO',categorias=None)
                    db.close_db()
                db.close_db()
                return render_template('nuevoProducto.html',titulo='Nuevo Producto',header='NUEVO PRODUCTO',categorias=reg)
            if request.form['submit'] == 'Cancelar':
                return render_template('portal.html',header='CAFETERÍA BRIOCHE')
            if request.form['submit'] == 'Buscar':
                db= Db()
                cur=db.conexion.cursor()
                nombre=request.form['nombreProducto']
                if nombre=="":
                    cur.execute("SELECT * FROM productos")
                else:
                    cur.execute("SELECT * FROM productos WHERE nombre like ?",('%'+nombre+'%',))
                reg=cur.fetchall()
                db.close_db()
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS',productos=reg)
        else:
           gestionarProducto()
    
    except:
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

@app.route('/crearProducto',methods=['GET', 'POST'])
def crearProducto():
    try:
        if request.method=='POST':
            if request.form['submit'] == 'Crear':
                print(-10)
                referencia=request.form['referencia']
                print(-9)
                nombre=request.form['nombre']
                precio=request.form['precio']
                categoria=request.form['categoria']
                cantidad=request.form['cantidad']
                print(-8)
                file = request.files['file']
                print(0)
                fileName=file.filename
                if referencia=="" or nombre=="" or precio=="" or categoria=="" or  cantidad=="" or fileName=="":
                    flash('Favor Llenar Todos Los Campos')
                    #flash('llenar---'+referencia+'---'+nombre+'---'+precio+'---'+categoria+'---'+cantidad)
                    db= Db()
                    cur=db.conexion.cursor()
                    cur.execute("SELECT nombre FROM categorias")
                    reg=cur.fetchall()
                    if reg is None:
                        return render_template('nuevoProducto.html',titulo='Nuevo Producto',header='NUEVO PRODUCTO',categorias=None)
                        db.close_db()
                    db.close_db()
                    return render_template('nuevoProducto.html',titulo='Nuevo Producto',header='NUEVO PRODUCTO',categorias=reg)
                db= Db()
                print(-5)
                cur=db.conexion.cursor()
                print(-4)
                cur.execute("SELECT * FROM productos WHERE referencia =?",(referencia,))
                reg=cur.fetchone()
                print(-3)
                if  reg is not None:
                    flash('Ya Existe Un Producto Con Esta Referencia')
                    db.close_db()
                    db= Db()
                    cur=db.conexion.cursor()
                    cur.execute("SELECT nombre FROM categorias")
                    reg=cur.fetchall()
                    if reg is None:
                        return render_template('nuevoProducto.html',titulo='Nuevo Producto',header='NUEVO PRODUCTO',categorias=None)
                        db.close_db()
                    db.close_db()
                    return render_template('nuevoProducto.html',titulo='Nuevo Producto',header='NUEVO PRODUCTO',categorias=reg)
                db.close_db()
                newName=referencia
                ext=fileName.split('.')
                ext=ext[len(ext)-1]
                fileName=newName+"." +ext
                fileName = secure_filename(fileName)
                db= Db()
                cur=db.conexion.cursor()
                cur.execute("SELECT id FROM categorias WHERE nombre=?",(categoria,))
                reg=cur.fetchone()
                numCategoria= reg[0]
                db.close_db()
                print(0)
                db= Db()
                print(1)
                cur=db.conexion.cursor()
                print(2)
                cur.execute('INSERT INTO productos (referencia, nombre, precio,categoria_id,cantidad_stock,nombre_foto) VALUES (?,?,?,?,?,?)',(referencia, nombre,precio,numCategoria,cantidad,fileName))
                print(3)
                db.conexion.commit()
                print(4)
                db.close_db()
                print(5)
                flash('success')
                db= Db()
                cur=db.conexion.cursor()
                cur.execute("SELECT nombre FROM categorias")
                reg=cur.fetchall()
                if reg is None:
                    return render_template('nuevoProducto.html',titulo='Nuevo Producto',header='NUEVO PRODUCTO',categorias=None)
                    db.close_db()
                db.close_db()
                print(fileName)
                urlBase=os.path.join(os.path.abspath("static"),'imagenes_productos')
                print(urlBase)
                file.save(os.path.join(urlBase,fileName))
                return render_template('nuevoProducto.html',titulo='Nuevo Producto',header='NUEVO PRODUCTO',categorias=reg)
            if request.form['submit'] == 'Cancelar':
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
        else:
            render_template('nuevoProducto.html',titulo='Nuevo Producto',header='NUEVO PRODUCTO',categorias=reg)
    except Error:
        print(Error)
        return redirect('/')

@app.route('/eliminarModificar',methods=['GET', 'POST'])
@login_required
def eliminarModificar():
    print(-1)
    try:
        print(-2)
        if request.method=='POST':
            print(-3)
            ids = request.form['imagen']
            print(ids)
            db= Db()
            cur=db.conexion.cursor()
            cur.execute("SELECT * FROM productos INNER JOIN categorias ON productos.categoria_id=categorias.id WHERE productos.id=?",(ids,))
            print(1)
            reg=cur.fetchone()
            if reg is None:
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
                db.close_db()
            db.close_db()
            producto=reg
            print(reg)
            db= Db()
            print(2)
            cur=db.conexion.cursor()
            print(3)
            cur.execute("SELECT nombre FROM categorias")
            print(4)
            reg=cur.fetchall()
            print(5)
            if reg is None:
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
                db.close_db()
                print(6)
            print(7)
            db.close_db()
            print(8)
            return render_template('eliminarModificar.html',titulo='Eliminar y/o Modificar Producto',header='ELIMINAR/MODIFICAR PRODUCTO',producto=producto,categorias=reg)

        else:
            return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
    except:
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

@app.route('/acctionEliminarModificar',methods=['GET', 'POST'])
@login_required
def acctionEliminarModificar():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Modificar':
                print(-10)
                referencia=request.form['referencia']
                print(-9)
                nombre=request.form['nombre']
                precio=request.form['precio']
                categoria=request.form['categoria']
                cantidad=request.form['cantidad']
                ids = request.form['id']
                print(-8)
                file = request.files['file']
                newName=referencia
                fileName=file.filename
                print(fileName)
                db= Db()
                cur=db.conexion.cursor()
                cur.execute("SELECT id FROM categorias WHERE nombre=?",(categoria,))
                reg=cur.fetchone()
                numCategoria= reg[0]
                db.close_db()
                if fileName!="":
                    ext=fileName.split('.')
                    ext=ext[len(ext)-1]
                    fileName=newName+"." +ext
                    fileName = secure_filename(fileName)
                    print(fileName)
                    urlBase=os.path.join(os.path.abspath("static"),'imagenes_productos')
                    print(urlBase)
                    file.save(os.path.join(urlBase,fileName))
                    print(9)
                    db= Db()
                    cur=db.conexion.cursor()
                    print(0)
                    cur.execute('UPDATE productos SET nombre=?,precio=?,categoria_id=?,cantidad_stock=?,nombre_foto=? WHERE id=?',(nombre, precio, numCategoria,cantidad,fileName,ids))
                    print(2)
                    db.conexion.commit()
                    print(3)
                    db.close_db()
                else:
                    db= Db()
                    cur=db.conexion.cursor()
                    print(0)
                    cur.execute('UPDATE productos SET nombre=?,precio=?,categoria_id=?,cantidad_stock=? WHERE id=?',(nombre, precio, numCategoria,cantidad,ids))
                    print(2)
                    db.conexion.commit()
                    print(3)
                    db.close_db()
                flash("success")
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
               
            if request.form['submit'] == 'Eliminar':
                ids = request.form['id']
                db= Db()
                cur=db.conexion.cursor()
                print(0)
                cur.execute('DELETE from productos WHERE id=?',(ids,))
                print(2)
                db.conexion.commit()
                print(3)
                db.close_db()
                flash("elimidado")
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
                
            if request.form['submit'] == 'Cancelar':
                return render_template('gestionarProducto.html',titulo='Gestionar Productos',header='GESTIONAR PRODUCTOS')
        else:
            return 'Error faltan datos para validar'
    
    except Error:
        print(Error)
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
                print( request.form.to_dict())
                entrada = request.form.to_dict()
                total=0
                for element in entrada:
                    if "cantidad" in element:
                        ids = int(element.split("-")[1])
                        print(0)
                        db= Db()
                        cur=db.conexion.cursor()
                        print(-1)
                        cur.execute("SELECT precio FROM productos WHERE id=?",(ids,))
                        print(-2)
                        reg=cur.fetchone()
                        db.close_db()
                        print(reg[0])
                        total+= int(entrada[element])*float(reg[0])
                print(1)
                fecha1=datetime.now()
                print(2)
                db= Db()
                cur=db.conexion.cursor()
                cur.execute("INSERT INTO ventas (fecha,valor_total,usuario_id) VALUES (?,?,?)",(fecha1, total,session["user_id"]))
                db.conexion.commit()
                db.close_db()
                print(3)
                db= Db()
                cur=db.conexion.cursor()
                cur.execute("SELECT max(id) FROM ventas WHERE usuario_id=?",(session["user_id"],))
                reg=cur.fetchone()
                db.close_db()
                ids = reg[0]
                print(4)
                return render_template('total.html',titulo='Total Factura',header='TOTAL FACTURA',ids=ids,total=total,fecha=fecha1,entrada=entrada)

            if request.form['submit'] == 'Cancelar':
                return render_template('gestionarVentas.html',titulo='Gestionar Facturas',header='GESTIONAR FACTURAS')
        else:
            return 'Error faltan datos para validar'
    
    except Error:
        print(Error)
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

@app.route('/total',methods=['GET', 'POST'])
@login_required
def total():
    try:
        if request.method == 'POST':
            if request.form['submit'] == 'Generar':
                id_delete=request.form["id_delete"]
                print(request.form["entrada"])
                entrada=request.form["entrada"]
                detalle=[]
                aux1=entrada.split(",")
                total=0
                for aux in aux1:
                    if "cantidad" in aux:
                        print(aux)
                        id_agregar=int(aux.split(":")[0].split("-")[1].replace("'",""))
                        cantidad = int(aux.split(":")[1].replace("'",""))
                        print(id_agregar)
                        print(cantidad)
                        db= Db()
                        cur=db.conexion.cursor()
                        print(-1)
                        cur.execute("SELECT precio,nombre FROM productos WHERE id=?",(id_agregar,))
                        print(-2)
                        reg=cur.fetchone()
                        db.close_db()
                        precio_total_producto= reg[0]*cantidad
                        total+=precio_total_producto
                        db= Db()
                        cur=db.conexion.cursor()
                        print(-3)
                        cur.execute("INSERT INTO detalle_ventas (venta_id,producto_id,cantidad,precio_total_producto) VALUES (?,?,?,?)",(id_delete, id_agregar,cantidad,precio_total_producto))
                        print(-4)
                        db.conexion.commit()
                        db.close_db()
                        detalle.append({"nombre":reg[1],"cantidad":cantidad,"subtotal":precio_total_producto,"idProducto":id_agregar,"precio":reg[0]})
                db= Db()
                cur=db.conexion.cursor()
                print(-1)
                cur.execute("SELECT fecha FROM ventas WHERE id=?",(id_delete,))
                print(-2)
                reg=cur.fetchone()
                db.close_db()
                options = {
                            'page-size': 'Letter',
                            'margin-top': '0.75in',
                            'margin-right': '0.75in',
                            'margin-bottom': '0.75in',
                            'margin-left': '0.75in',
                            'encoding': "UTF-8",
                            'custom-header' : [
                                ('Accept-Encoding', 'gzip')
                            ],
                            'cookie': [
                                ('cookie-name1', 'cookie-value1'),
                                ('cookie-name2', 'cookie-value2'),
                            ],
                            'no-outline': None
                        }
                render=render_template("pdf_template.html",idFactura=id_delete,fecha=reg[0],detalle=detalle,total=total,usuario=session["user"])

                pdf=pdfkit.from_string(render,False,options=options)
                response=make_response(pdf)
                response.headers["Content-Type"]="aplication/pdf"
                response.headers["Content-Disposition"]="inline;filename=factura.pdf"
                return response
            if request.form['submit'] == 'Cancelar':
                id_delete=request.form["id_delete"]
                db= Db()
                cur=db.conexion.cursor()
                print(id_delete)
                cur.execute('DELETE from ventas WHERE id=? AND usuario_id=?',(id_delete,session["user_id"],))
                print(2)
                db.conexion.commit()
                print(3)
                db.close_db()
                return render_template('nuevaFactura.html',titulo='Nueva Factura',header='NUEVA FACTURA')
        else:
            return 'Error faltan datos para validar'
    
    except Error:
        print(Error)
        return render_template('portal.html',header='CAFETERÍA BRIOCHE')

@app.route('/verFactura',methods=['GET', 'POST'])
@login_required
def verFactura():
    return render_template('verFactura.html',titulo='Ver Factura',header='VER FACTURA')

@app.route('/agregarCategoria',methods=['GET', 'POST'])
def agregarCategoria():
    try:
        nombre = request.args.get('nombre')
        db= Db()
        cur=db.conexion.cursor()
        cur.execute("SELECT * FROM categorias WHERE nombre = ?",(nombre,))
        reg=cur.fetchone()
        if  reg is not None:
            db.close_db()
            return ({'status':'EXIST'})
        db.close_db()
        db= Db()
        cur=db.conexion.cursor()
        cur.execute("INSERT INTO categorias (nombre) VALUES (?)",(nombre,))
        db.conexion.commit()
        db.close_db()
        return  ({'status':'OK'})
    except:
        return  ({'status':'FALSE'})

@app.route('/buscarProducto',methods=['GET', 'POST'])
def buscarProducto():
    try:
        if request.method == 'POST':
            nombre = request.args.get('nombre')
            db= Db()
            cur=db.conexion.cursor()
            if nombre=="":
                cur.execute("SELECT * FROM productos")
            else:
                cur.execute("SELECT * FROM productos WHERE nombre like ?",('%'+nombre+'%',))
            reg=cur.fetchall()
            db.close_db()
            print(reg)
            return  dict(zip(range(len(reg)), reg))  
    except:
        print(Error)
        return  ({'status':'FALSE'})

@app.route('/buscarId',methods=['GET', 'POST'])
def buscarProductoId():
    try:
        if request.method == 'POST':
            ids = request.args.get('id')
            db= Db()
            cur=db.conexion.cursor()
            cur.execute("SELECT * FROM productos WHERE id=?",(ids,))
            reg=cur.fetchone()
            db.close_db()
            print(reg)
            return  dict(zip(range(len(reg)), reg))  
    except:
        print(Error)
        return  ({'status':'FALSE'})