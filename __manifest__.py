# -*- coding: utf-8 -*-

{
        'name': "Inventario de Bienes Publicos",
        'version' : "1.0",
        'author' : "Gheylert A. Gil",
        'website' : "",
        'category' : "Inventario De Bienes",
        
        'description': """
                 Inventario Bienes Publicos
         """,
        'depends' : ['base','catalogo','sudebip','bienes'],
        'data' : ['security/groups.xml',

        'security/ir.model.access.csv',

        'views/inventario_bienes_view.xml',
        'views/inventario_resultado_bien_view.xml',
        
        'report/bien_encabezado_inventario_template.xml',
        'report/ficha_bienes_inventariados_template.xml',
        'report/resultado_bienes_inventario_template.xml',

        #'wizard/ficha_bien_oficina_reporte_wizard.xml',
        #'wizard/listado_bien_grupo_reporte_wizard.xml',
        #'wizard/listado_bien_clasificacion_marca_reporte_wizard.xml',
        #'wizard/listado_bienes_sedes_reporte_wizard.xml'
        #'views/views.xml',
        #'report/report.xml',
        #'report/inventario_bienes_template.xml',

        
        #'report/action_report_personalizado_estudiante.xml',        

        
        ], 
#

      
        
        'installable': True,
        'auto_install': False
        
} 
