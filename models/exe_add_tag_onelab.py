from odoo import models, fields, api
from datetime import date, timedelta

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # ONELAB - Seguridad y certificaciones
    onelab_electric_safety = fields.Selection([
        ('yes', 'Sí'),
        ('no', 'No'),
    ], string='Seguridad Eléctrica')
    onelab_cas_code = fields.Char(string='CAS')
    onelab_gtin = fields.Char(string='GTIN')

    # SENASA
    onelab_senasa_cert_number = fields.Char(string='Certificado SENASA')
    onelab_senasa_expiration = fields.Date(string='Vencimiento SENASA')

    # SIMELA
    onelab_simela = fields.Selection([
        ('yes', 'Sí'),
        ('no', 'No'),
    ], string='SIMELA')

    # ANMAT
    onelab_anmat_entity_type = fields.Char(string='Tipo de entidad ANMAT')
    onelab_anmat_cert_number = fields.Char(string='Número de certificado ANMAT')
    onelab_anmat_validity = fields.Date(string='Vigencia ANMAT')
    onelab_anmat_attachment = fields.Binary(string='Adjunto certificado ANMAT')
    onelab_anmat_attachment_filename = fields.Char(string='Nombre del archivo ANMAT')

    # RENPRE
    onelab_renpre_required = fields.Selection([
        ('yes', 'Sí'),
        ('no', 'No'),
    ], string='¿Requiere RENPRE?')
    onelab_renpre_type = fields.Selection([
        ('lista_i', 'LISTA I'),
        ('lista_ii', 'LISTA II'),
        ('lista_iii', 'LISTA III'),
    ], string='Tipo RENPRE')

    # Vencimiento mínimo aceptado
    onelab_min_expiry_days = fields.Integer(string='Vencimiento mínimo aceptado (días)')



    @api.onchange('onelab_senasa_expiration', 'onelab_min_expiry_days')
    def _onchange_senasa_expiry_warning(self):
        for record in self:
            if record.onelab_senasa_expiration and record.onelab_min_expiry_days:
                threshold = date.today() + timedelta(days=record.onelab_min_expiry_days)
                if record.onelab_senasa_expiration <= threshold:
                    return {
                        'warning': {
                            'title': 'Alerta de vencimiento SENASA',
                            'message': '⚠️ El certificado SENASA está próximo a vencer según el mínimo aceptado.',
                        }
                    }
