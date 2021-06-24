# -*- coding= utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression




#from Datetime import Date, Datetime,timedelta
##############from odoo.addons.jasper_reports import jasper_report
#from odoo import pooler
#from Datetime import  Datetime
from time import time

from datetime import date
from datetime import datetime

formatter_string = "%d-%m-%y" 
#from tools.translate import_
#from odoo import tools
#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")
#Importamos la libreria logger
import logging, csv, operator
#Definimos la Variable Global
_logger = logging.getLogger(__name__)


class inventario_resultado_bien(models.Model):
    """Registra los bienes del inventario"""
    _name = 'inventario_resultado_bien'
    _rec_name = 'nombre'
    
    nombre = fields.Char('Descripción', help='Registra la Descripción del resultado', required=True)
    
    _sql_constraints = [('nombre', 'unique(nombre)', 'La descripción del Resultado, debe ser Unico!')]


class inventario_resumen(models.Model):
    """Resumen del inventario"""
    _name = 'inventario_resumen'
    #_rec_name = 'nombre'

    inventario_bienes_id = fields.Many2one('inventario_bienes','Inventario', required=True)
    bienes_id = fields.Many2one('bienes','Bien', required=True)                                       
    inventario_resultado_bien_id = fields.Many2one('inventario_resultado_bien', 'Resultado Inventario Bien ', required=True)
    descripcion_resultado = fields.Text(string = "Descripción Resultado")
    bien_nro_resumen = fields.Char('Nro Bien')
    bien_nombre_resumen = fields.Text('Descripción Bien')
    oficina_id_resumen = fields.Many2one('oficinas', 'Oficina Inventario')




class inventario_bienes_detalle(models.Model):
    """Registra los bienes del inventario"""
    _name = 'inventario_bienes_detalle'
    _rec_name = 'bienes_id'
    _order = 'inventario_bienes_id, bien_nro'


    inventario_bienes_id = fields.Many2one('inventario_bienes','Inventario', required=True, 
                                           help='Id del Inventario')
    bienes_id = fields.Many2one('bienes','Bien', required=True, 
                                           help='Registre el Bien Inventariado')
                                           
                                       
    estatus_bien = fields.Selection([('1','Correcto'),('2','Incorrecto')],'Estatus del Bien Inventariado', required=True,
                                           help='Estadus del Bien Inventario')
    inventario_resultado_bien_id = fields.Many2one('inventario_resultado_bien', 'Resultado Inventario Bien ', required=True, 
                                           help='Registra la Condición de Inventario del Bien')
    descripcion_resultado = fields.Text(string = "Descripción Resultado")
    bien_nro = fields.Char('Nro Bien', size=20)
    bien_nombre = fields.Text('Descripción Bien')
    
    _sql_constraints = [('inventario_bienes_detalle_ids', 'unique(inventario_bienes_id, bienes_id)', 'El Bien Inventariado, debe ser Unico!')]  
                                                                                   
    @api.model
    def create(self, value):
        rec = super(inventario_bienes_detalle, self).create(value)
        return rec
    
                                                                                      
    @api.onchange('bienes_id')
    def generar_bien(self):
        if self.bienes_id:
            oficina_id = self.inventario_bienes_id.inventario_oficinas_id.id
            domain_bien = [('bienes_numbien','=',self.bienes_id.bienes_numbien)]
            recordset_bien= self.env['bienes'].search(domain_bien)
            nro_bien = len(recordset_bien)
            if nro_bien > 0:
                for registro_bien in recordset_bien:
                    ofic_actual = registro_bien.bienes_oficinas_id.id
                    sw_mensaje = 0
                    if registro_bien.tipo_estatus_inventario_id.id == 4:
                        self.estatus_bien = '2'
                        self.inventario_resultado_bien_id = 2
                        self.descripcion_resultado = 'BIEN NO ESTA INVENTARIADO'
                        sw_mensaje = 1
                        
                    if registro_bien.tipo_estatus_inventario_id.id == 3:
                        self.estatus_bien ='2'
                        self.inventario_resultado_bien_id = 4
                        self.descripcion_resultado = 'BIEN DESINCORPORADO'
                        sw_mensaje = 1
                        
                        
                    if sw_mensaje == 0:
                        if ofic_actual == oficina_id:        
                            self.estatus_bien = '1'
                            self.inventario_resultado_bien_id = 1
                        else:
                            oficina_nombre = registro_bien.bienes_oficinas_id.oficinas_nombre
                            self.estatus_bien = '2'    
                            self.inventario_resultado_bien_id = 3
                            self.descripcion_resultado = 'PERTENECIENTE A [' + oficina_nombre + ']'
                    self.bien_nro =    registro_bien.bienes_numbien
                    self.bien_nombre = registro_bien.bienes_nombre
                    
                            
    
    


  
class inventario_bienes(models.Model):
    """Inventario De Bienes"""
    _name = 'inventario_bienes'
    #_rec_name = 'bienes_numbien'
    #_order = 'bienes_numbien'  

    #def fecha_actual(self):
    #    today = fields.Datetime.now()
    #    fecha = today.strftime('%d/%m/%Y')        
    #    return fecha     


    def fecha_actual(self):
        today = fields.Datetime.now()
        fecha = today.strftime('%d/%m/%Y')        
        return fecha    



    inventario_fecha = fields.Date('Fecha Inicio Inventario', required=True,
                                  help='Fecha Inicio Inventario de la Oficina')
    inventario_regiones_id  = fields.Many2one('regiones',string= 'Regiones de Ubicación de la Sede', default=1,
                                              required=True, help='Regiones de Ubicación de la Sede')                                  
    inventario_sedes_id = fields.Many2one('sedes',string='Sedes del Organismo', required=True,
                          domain="[('regiones_id','=',inventario_regiones_id)]", help='Seleccionar Sede')
    inventario_oficinas_id = fields.Many2one('oficinas', 'Oficina', domain="[('sedes_id','=',inventario_sedes_id)]",
                                             required=True, help='Registra la Oficina donde se realiza en Inventario')
    inventario_responsable_uso_id = fields.Many2one('personas', 'Responsable de Uso', domain="[('personas_oficinas_id','=',inventario_oficinas_id)]", 
                                                     required=True, help='Registra el Responsable de la Oficina')
    inventario_estado = fields.Selection([('1','En Proceso'),('2','Culminado')],'Estado Inventario', 
                                           help='Estado del Inventario')
    inventario_observacion =   fields.Text('Observaciones Del Inventario', help='Registra Observaciones Del Inventario')
 
    
    inventario_bienes_detalle_ids = fields.One2many('inventario_bienes_detalle','inventario_bienes_id', string="Inventario Bien", deleted="cascade",
                          help='Registra los BienesBien', required=True)
    inventario_resumen_ids  = fields.One2many('inventario_resumen','inventario_bienes_id', string="Resumen", deleted="cascade")                         
    sw_inventario = fields.Integer('Sw Inventario', help='Sw Inventario', default=0)
    active = fields.Boolean ('Activo', default=True, help='Si esta Activo el otro lo icluira en la vista')

    _defaults = { 
        'active' : True,
        }
        
    @api.model
    def create(self, value):
        rec = super(inventario_bienes, self).create(value)
        rec['inventario_estado'] = '1'
        rec['sw_inventario'] = 1
        return rec
        

    @api.onchange('inventario_sedes_id')
    def onchange_inventario_sedes(self):
        self.inventario_oficinas_id = ''
        
     
    @api.onchange('inventario_oficinas_id')
    def onchange_inventario_oficinas_id(self):
        self.inventario_responsable_uso_id = ''
       
        

    def resumen_inventario(self):
        oficina_id = self.inventario_oficinas_id.id
        domain_bienes = [('bienes_oficinas_id','=',oficina_id),('tipo_estatus_inventario_id','in',(1,2)),('active','=',True)]
        recordset_bienes = self.env['bienes'].search(domain_bienes)
        nro_bien = len(recordset_bienes)
        
        bienes = ''
        sw_estatus_resumen = 0  #Si el inventario es correcto es cero(0), si existe alguna anomalia es uno(1)
        for registro_bien in recordset_bienes:
            sw_bien = 0
            for bienes_inventariado in self.inventario_bienes_detalle_ids:
                if bienes_inventariado.bienes_id.id == registro_bien.id:
                    sw_bien = 1
                    break
            if sw_bien == 0:
                sw_estatus_resumen = 1
                values = {'inventario_bienes_id':self.id,
                          'bienes_id':registro_bien.id,
                          'inventario_resultado_bien_id': 5,
                          'descripcion_resultado' : 'BIEN FALTANTE',
                          'bien_nro_resumen' : registro_bien.bienes_numbien,
                          'bien_nombre_resumen' : registro_bien.bienes_nombre,
                          'oficina_id_resumen': registro_bien.bienes_oficinas_id.id,
                         } 
                self.env['inventario_resumen'].create(values)
                
                
        for bienes_inventariado_anomalia in self.inventario_bienes_detalle_ids:
            if bienes_inventariado_anomalia.estatus_bien == '2':
                sw_estatus_resumen = 1
                values = {'inventario_bienes_id':self.id,
                          'bienes_id':bienes_inventariado_anomalia.bienes_id.id,
                          'inventario_resultado_bien_id': bienes_inventariado_anomalia.inventario_resultado_bien_id.id,
                          'descripcion_resultado' : bienes_inventariado_anomalia.descripcion_resultado,
                          'bien_nro_resumen' : bienes_inventariado_anomalia.bien_nro,
                          'bien_nombre_resumen' : bienes_inventariado_anomalia.bien_nombre,
                          'oficina_id_resumen': self.inventario_oficinas_id.id,
                         } 
                self.env['inventario_resumen'].create(values)

        domain_resumen = [('id','=',self.id)]
        recordset_resumen = self.env['inventario_bienes'].search(domain_resumen)
        
        for regis in recordset_resumen:
            regis.write({'sw_inventario':2,
                         'inventario_estado':'2'})                    
                         

        return True
