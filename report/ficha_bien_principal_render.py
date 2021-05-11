# -*- coding= utf-8 -*-

from odoo import api, fields, models
from odoo.tools import float_round
from odoo.exceptions import ValidationError

class FchaBienPrincipalRender(models.AbstractModel):
    _name = "report.bienes.ficha_bien_principal_render"
    
    #def m_observacion(self, observa):
    #    if observa == False:
    #        return ''
    #    else:   
    
    #        observa = str(observa)
    #        if len(observa) > 150:
    #            observa = observa[0:145] + "[...]"        
    #        return observa


    #def f_costo(self, costo):
    #    costo_f = "{0:.7f}".format(costo)
    #    return costo_f


        
    @api.model
    def _get_report_values(self, docids, data):
        """in this function can access the data returned from the button
        click function"""
        
        #date_init = data['date_init']
        #model_id = '' 

        #value = []

        #query = """SELECT *
        #                FROM escuela_estudiante as ee """
 
        #if date_init:
        #    query = query . "WHERE ee.fecha_pago <= '" + date_init 


        #value.append(model_id)
        #self._cr.execute(query, value)
        #record = self._cr.dictfetchall()
        
        bienes = self.env['bienes'].browse(data.get('active_ids'))
    #    docargs = {}
       
        
        

        today = fields.Datetime.now()
        
        fecha = today.strftime('%d/%m/%Y')
        return {
            'docs': bienes, 
            #'sede':data["sede"],
            #'oficina':data["oficina"],
            #'nro_bienes':data["nro_bienes"],
            'date_today': fecha,
            #'m_observacion': self.m_observacion,
            #'f_costo': self.f_costo,
            #'tot_costo': data["tot_costo"],
        }
        
        
        
        
        
    #def render_html(self, docids, data=None):
    #    data = data if data is not None else {}
    #    estudiantes = self.env['escuela_estudiante'].browse(data.get('active_ids'))
    #    docargs = {}
        #    'doc_ids' : data_get('ids', data.get('active_ids')),
        #    'doc_model' : 'escuela.estudiante',
        #    'docs' : estudiantes,
        #    'data' : dict(
        #        data
        #    ),
        #}
    #    return self.env['ir.actions.report'].render('escuela.estudiante_listado_template',docargs)
        
          
