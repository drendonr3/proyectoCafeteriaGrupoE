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