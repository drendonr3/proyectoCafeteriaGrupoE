function validarCamposCrearUsuario(){
    var usuario = document.getElementById("usuario").value;
    var correo = document.getElementById("correo").value;
    var contrasena = document.getElementById("contrasena").value;

    
    if(correo=="")
    {
        alert("Debe Ingresar un Correo");
        document.getElementById("correo").focus();//pone el cursor
        return false;
    }
    if (usuario=="" || usuario.length <6)
    {
        alert("El usuario debe tener mínimo 6 caracteres");
        document.getElementById("usuario").focus();//pone el cursor
        return false;
    }
    if (contrasena =="")
    {
        alert("Debe Ingresar una Contraseña");
        document.getElementById("contrasena").focus();//pone el cursor
        return false;
    }

   return true;
}

function agregarCategoria(){
    if (document.getElementById('categoria').value==='agregar'){
        var categoria = prompt("Nombre de la Categoría", "");
        if (categoria != null){
            if (categoria!=''){
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    resp= JSON.parse(this.responseText);
                    if (resp['status']==="OK"){
                            select=document.getElementById('categoria')
                            var opt = document.createElement('option');
                            opt.value = categoria;
                            opt.innerHTML = categoria;
                            select.appendChild(opt);
                            select.value=categoria;
                            alert("Categoría Agregada");
                        } else if (resp['status']==="EXIST"){
                            select=document.getElementById('categoria')
                            select.value=categoria;
                            alert("Categoría ya Existe");
                        } else{
                            alert("No Se Agregó la Categoría");
                        }
                    }
                };
                xhttp.open("POST", "/agregarCategoria?nombre=" + categoria, true);
                xhttp.send();

                
            } else {
                alert("No Se Agregó la Categoría");
            }
        }
    }
}

function validateImage(){
    var file = document.getElementById("fileImagen");
    var name = file.files[0].name;
    var ext = name.split('.')[1];
    ext = ext.toLowerCase();
	switch (ext) {
        case 'jpg':
        case 'jpeg':
        case 'png':break;
        default:
            alert('El Archivo Debe Ser Una Imagen\nVuelva a Seleccionarlo');
            file.value="";
            image.style.display="none"
            return;
    }
    var image=document.getElementById("imagen_producto");

    //image.style.display="grid";
    //image.src=file.files[0].webkitRelativePath;
    
}

function validateEliminar(){
    submit=document.getElementById("eliminar")
    return true
}


function buscarProducto(){
    nombre= document.getElementById("nombre").value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        resps= JSON.parse(this.responseText);
        div1=document.getElementById("lista")
        div = document.createElement('div');
        div.setAttribute("class", "lista_poductos_factura");
        div1.removeChild(div1.lastChild);
        for (i=0;i<Object.keys(resps).length;i++){
            console.log(resps)
            input=document.createElement('input');
            input.setAttribute("type", "image");
            input.setAttribute("class", "agregar");
            input.setAttribute("src", "/static/imagenes_productos/" + resps[i][6]);
            input.setAttribute("id", resps[i][0]);
            input.setAttribute("onclick", "agreraProductoFactura(this.id)");
            div.appendChild(input)
            input=document.createElement('input');
            input.setAttribute("type", "hidden");
            input.setAttribute("name", "imagen");
            input.setAttribute("value",resps[i][0])
            div.appendChild(input)
        }
        div1.appendChild(div);
    }
    };
    xhttp.open("POST", "/buscarProducto?nombre=" + nombre, true);
    xhttp.send();
    
}

function agreraProductoFactura(id){
    /*var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        resps= JSON.parse(this.responseText);
        form=document.getElementById("verFactura")
        /*<div class="lista_producto_factura"><label class="label-list">Empanada</label><input type="text" value="4"></input><label class="label-list">4500</label><input type="button" value="Eliminar"></div>
        for (i=0;i<Object.keys(resps).length;i++){
            divinput=document.createElement('input');
            input.setAttribute("type", "image");
            input.setAttribute("class", "agregar");
            input.setAttribute("src", "/static/imagenes_productos/" + resps[i][6]);
            input.setAttribute("id", resps[i][0]);
            input.setAttribute("onclick", "agreraProductoFactura(this.id)");
            div.appendChild(input)
            input=document.createElement('input');
            input.setAttribute("type", "hidden");
            input.setAttribute("name", "imagen");
            input.setAttribute("value",resps[i][0])
            div.appendChild(input)
            
        }
        div1.appendChild(div);
    }
    };
    xhttp.open("POST", "/buscarProductoId?id=" + id, true);
    xhttp.send();
*/
}