# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import timedelta

#Importaciones:
# models: Contiene las clases base de Odoo, como models.Model, que usamos para crear modelos.
# fields: Proporciona los tipos de campos que podemos usar en los modelos (como Char, Boolean, Many2one, etc.).
# api: Contiene decoradores y métodos útiles para definir lógica de negocio, como @api.depends, @api.onchange.


class video_club_pelicula(models.Model):    #Define un modelo llamado video_club_pelicula. Hereda de models.Model,
                                            # lo que permite que esta clase interactúe con la base de datos de Odoo.
    _name = 'video_club.pelicula'            # Nombre tecnico del modelo
    _description = 'Gestion de películas'    # Descripcion breve del modelo

    #Definicion de los campos del modelo
    name = fields.Char(string="Título",required=True, help="Introduce el título de la película")
                    # fields.Char: Es un campo de texto (cadena).
                    # string="Título": Define la etiqueta que se muestra en la interfaz de usuario.
                    # required=True: Hace que este campo sea obligatorio.
                    # help="Introduce el título de la película": Proporciona un mensaje de ayuda que aparece al pasar el ratón sobre el campo.

    director = fields.Char(string="Director",required=True, help="Introduce el director")
    color = fields.Boolean(string="Color", default=True)
    duracion = fields.Integer(string="Duración (minutos)")
    industria = fields.Selection([('0','Hollywood'),('1','Europea'),('2','Bollywood'),('3','Otras')],default="1",string="Industria")
                    #fields.Selection: Permite seleccionar un valor de una lista de opciones.
                    # [('0', 'Hollywood'), ...]: Define las opciones disponibles como pares clave-valor.
                    # default="1": Establece el valor predeterminado como “Europea”.
                    # string="Industria": Etiqueta visible en la UI.
    fecha = fields.Date(string="Fecha estreno España")
    sinopsis = fields.Text(string="Sinopsis")
    imagen_portada = fields.Binary(string="Imagen portada", attachment=True)

#   Muchas peliculas pueden pertenecer a un genero. No se indica el campo por lo que por defecto cogerá name
    genero = fields.Many2one("video_club.genero",string="Género",required=True)
                #fields.Many2one: Relación “muchos a uno”.
                # "video_club.genero": Relaciona este modelo con el modelo video_club.genero.
                # string="Género": Etiqueta visible.
                # required=True: Hace que este campo sea obligatorio.

    estado = fields.Selection([('disponible', 'Disponible'),('alquilada', 'Alquilada'),('no_disponible', 'No disponible')], string="Estado", default="disponible")

class video_club_genero(models.Model):          #Define un modelo llamado video_club_genero
    _name = 'video_club.genero'                  # Nombre tecnico del modelo
    _description = 'Género cinematográfico'      # Descripcion breve del modelo

    #Definicion de los campos del modelo
    name = fields.Char(string= "Género",required=True, help="Introduce el género cinematográfico")  #campo para el nombre del genero
    comentario = fields.Text(string="Comentarios")

#   Cada Género puede contener varias películas. En el caso One2many hay que especificar el campo de relación
    pelicula = fields.One2many("video_club.pelicula","genero",string="Películas")
                    #fields.One2many: Relación “uno a muchos”.
                    # "video_club.pelicula": Modelo relacionado (películas).
                    # "genero": Campo Many2one del modelo video_club.pelicula que establece la relación.
                    # Esto permite listar todas las películas asociadas a un género en su vista.

class Alquiler(models.Model):
    _name = 'video_club.alquiler'
    _description = 'Registro de alquileres de películas'

    pelicula_id = fields.Many2one('video_club.pelicula', string="Titulo", required=True)
    usuario_id = fields.Many2one('res.partner', string="Cliente", required=True)
    fecha_inicio = fields.Date(string="Fecha de inicio", required=True, default=fields.Date.today)

    @api.depends('fecha_inicio')
    def _compute_fecha_fin(self):
        """ Calcula automáticamente la fecha de fin como fecha_inicio + 3 días """
        for record in self:
            if record.fecha_inicio:
                record.fecha_fin = record.fecha_inicio + timedelta(days=2)
            else:
                record.fecha_fin = False

    fecha_fin = fields.Date(string="Fecha de Fin", compute="_compute_fecha_fin", store=True)
    estado_alquiler = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('devuelto', 'Devuelto'),
        ('retrasado', 'Retrasado'),
        ('devuelto_r','Devuelto retrasado')
    ], string="Estado")

    def name_get(self):
        """Personaliza el nombre mostrado en la UI"""
        result = []
        for record in self:
            name = f"{record.pelicula_id.name}" if record.pelicula_id else "Alquiler"
            result.append((record.id, name))
        return result


    def alquilar_pelicula(self):
        """ Método para alquilar una película """
        for record in self:
            if record.pelicula_id.estado != 'disponible':
                raise exceptions.UserError("La película seleccionada no está disponible para alquiler.")

            record.pelicula_id.estado = 'alquilada'  # Cambia el estado de la película
            record.estado_alquiler = 'pendiente'  # Estado del alquiler

    def devolver_pelicula(self):
        """ Método para devolver una película """
        for record in self:
            if record.estado_alquiler =='retrasado':
                record.estado_alquiler = 'devuelto_r' # Marca la película como devuelta con retraso
            else:
                record.estado_alquiler = 'devuelto'  # Marca el alquiler como devuelto

            record.pelicula_id.estado = 'disponible'  # Marca la película como disponible nuevamente


    def verificar_retraso(self):
        """Método para verificar si el alquiler está retrasado"""
        for record in self.search([('estado_alquiler', '=', 'pendiente')]):
            if record.fecha_fin and record.fecha_fin < fields.Date.today():
                record.estado_alquiler = 'retrasado'