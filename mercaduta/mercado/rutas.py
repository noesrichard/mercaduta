from flask import Blueprint,render_template, session, url_for, redirect,request
from mercaduta.auth.utils import login_required
from mercaduta.clases.oferta import Oferta
from mercaduta.clases.solicitud import Solicitud
from mercaduta.clases.calificacion import Calificacion
from mercaduta.clases.categoria import Categoria

mercado = Blueprint("mercado",__name__,template_folder='templates',
                static_folder='static',static_url_path="/%s"%__name__)


@mercado.route("/")
@login_required
def inicio(): 
    return render_template("inicio.html")



@mercado.route("/mercado/<categoria>")
@login_required
def mostrar_productos(categoria): 
    ofertas = Oferta().listar_ofertas(categoria)
    return render_template("productos.html",ofertas=ofertas)

@mercado.route("/mercado/todos")
@login_required
def mostrar_todos_productos(): 
    ofertas = Oferta().listar_todas_ofertas()
    return render_template("productos.html",ofertas=ofertas)

@mercado.route("/mercado/descripcion/<id_oferta>")
@login_required
def descripcion(id_oferta): 
    oferta = Oferta().seleccionar_oferta(id_oferta)
    calificaciones = Calificacion().segun_vendedor(id_oferta)
    return render_template("descripcion.html",oferta = oferta, calificaciones = calificaciones)


@mercado.route("/comunicate")
@login_required
def comunicate(): 
    return render_template("comunicate.html")


@mercado.route("/crear-oferta",methods = ["GET","POST"]) 
@login_required
def crear_oferta(): 
    if request.method == "POST": 
        oferta = Oferta()
        oferta.set_titulo(request.form['titulo'])
        oferta.set_precio(request.form['precio'])
        oferta.set_categoria(request.form['categoria'])
        oferta.set_condicion(request.form['condicion'])
        oferta.set_descripcion(request.form['des'])
        oferta.set_fecha()
        oferta.set_usuario(session['email'])
        if oferta.subir(): 
            return redirect(url_for('mercado.inicio'))
        return "Tu oferta no se pudo subir, comprueba que hayas ingresado bien la informacion" 
    return render_template("crear_oferta.html", categorias = Categoria().listar_categorias())


@mercado.route("/solicitudes") 
@login_required
def solicitudes():
    solicitud = Solicitud()

    solicitud.set_email_solicitante(session['email'])

    solicitudes = solicitud.listar_solicitudes()
    print(solicitudes)
    info_solicitudes = solicitud.listar_solicitudes_enviadas()
    print(info_solicitudes)
    return render_template("solicitudes.html", solicitudes = solicitudes, info_solicitudes = info_solicitudes)


@mercado.route("/solicitar-datos-<id_oferta>")
@login_required
def solicitar_datos(id_oferta): 
    solicitud = Solicitud()
    solicitud.set_email_solicitante(session['email'])
    solicitud.set_id_oferta(id_oferta)
    if not solicitud.existe(): 
        solicitud.guardar()
        return render_template("solicitar_datos.html")
    return "Ya solicitaste estos datos" 

@mercado.route("/aceptar-solicitud-<id_solicitud>")
@login_required
def aceptar_solicitud(id_solicitud): 
    Solicitud().aceptar(id_solicitud)
    return redirect(url_for('mercado.solicitudes'))

@mercado.route("/calificar-<vendedor>-<oferta>", methods = ['GET', 'POST'])
@login_required
def calificar_vendedor(vendedor,oferta): 
    
    calificacion = Calificacion()
    calificacion.set_comprador(session['email'])
    calificacion.set_vendedor(vendedor)
    calificacion.set_oferta(oferta)
    if request.method == "POST" and not calificacion.existe(): 
        
        calificacion.set_valor(request.form['valor'])
        calificacion.set_descripcion(request.form['des'])
        
        calificacion.imprimir()
        calificacion.guardar()
        return redirect(url_for('mercado.inicio'))
    return render_template('calificar.html',vendedor = vendedor, oferta = oferta)


@mercado.route("/eliminar-solicitud-<id_solicitud>")
@login_required
def eliminar_solicitud(id_solicitud): 
    Solicitud().eliminar_solicitud(id_solicitud)
    return redirect(url_for('mercado.solicitudes'))
