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
            input.setAttribute("type", "submit");
            input.setAttribute("class", "agregar");
            input.setAttribute("style", "background-image: url('/static/imagenes_productos/" + resps[i][6]+"');height: 150px;\
            width: 100%;margin: 0;background-size: cover;\
            font-size: x-large;\
            padding:0;\
            padding-top:60%;\
            text-align:center;color:white;margin-right:5px;\
            border: 1px solid black;");
            input.setAttribute("form","cc")
            input.setAttribute("value",resps[i][2].toUpperCase())
            input.setAttribute("id", resps[i][0]);
            input.setAttribute("onclick", "agreraProductoFactura(this.id)");
            div.appendChild(input)
        }
        div1.appendChild(div);

    }
    };
    xhttp.open("POST", "/buscarProducto?nombre=" + nombre, false);
    xhttp.send();
    
}

function agreraProductoFactura(id){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        resp= JSON.parse(this.responseText);
    }
    };
    xhttp.open("POST", "/buscarId?id=" + id, false);
    xhttp.send();

    aux=document.getElementById("input-"+id);
    if (aux == null){
        console.log(resp);
        form=document.getElementById("verFactura");
        div =document.createElement('div');
        div.setAttribute("id", "div-"+resp[0]);
        div.setAttribute("class", "lista_producto_factura prodcutoFactura");
        label=document.createElement('label');
        label.setAttribute("class", "label-list");
        label.innerHTML = resp[2].toUpperCase();
        label.setAttribute("style","width: max-content;")
        div.appendChild(label);
        input=document.createElement('input');
        input.setAttribute("type", "number");
        input.setAttribute("name", "cantidad-"+resp[0]);
        input.setAttribute("id", "input-"+resp[0]);
        input.setAttribute("onchange", "calcuarSubtotal(this)");
        input.value=1;
        div.appendChild(input);
        label=document.createElement('label');
        label.setAttribute("class", "label-list");
        label.setAttribute("id", "unit-"+resp[0]);
        label.innerHTML=resp[4];
        div.appendChild(label);
        label=document.createElement('label');
        label.setAttribute("class", "label-list");
        label.setAttribute("id", "subtotal-"+resp[0]);
        label.innerHTML=resp[4];
        div.appendChild(label);
        button=document.createElement('button');
        button.setAttribute("form", "cc");
        button.setAttribute("onclick", "eliminarProducto(this)");
        button.setAttribute("id","button-"+resp[0]);
        button.innerHTML="-";
        div.appendChild(button);
        form.appendChild(div);
    } else {
        aux.value++;
        calcuarSubtotal(aux);
    }
    ocultarTotal();
}

function ocultarTotal(){
    divs = document.getElementsByClassName("prodcutoFactura")
    if (divs.length>0){
        document.getElementById("total").style.display="inline-block";
    } else {
        document.getElementById("total").style.display="none";
    }
}

function eliminarProducto(element){
    parent= element.parentElement;
    parent.remove();
    ocultarTotal();
}

function calcuarSubtotal(element){
    id= element.id.split("-")[1];
    elementSet = document.getElementById("subtotal-"+id);
    if (parseInt(element.value)<=0){
        elementSet.innerHTML=parseFloat(document.getElementById("unit-"+id).innerHTML);
        element.value=1;
    } elif: {
        elementSet.innerHTML= parseInt(element.value)*parseFloat(document.getElementById("unit-"+id).innerHTML);
    }
}

function filtroFecha(){
    element = document.getElementById("tipoFecha");
    element.parent.style()
    if (element.value == "rango"){
        document.getElementById("filtroRango").style.display="grid";
    } else {
        document.getElementById("filtroRango").style.display="none";
    }

}