from odoo import models, fields, api
from datetime import date, timedelta

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # ONELAB - Seguridad y certificaciones
    onelab_electric_safety = fields.Boolean(string='Seguridad Eléctrica')
    onelab_cas_code = fields.Char(string='CAS')
    onelab_gtin = fields.Char(string='GTIN')

    # SENASA
    onelab_senasa_cert_number = fields.Char(string='Certificado SENASA')
    onelab_senasa_expiration = fields.Date(string='Vencimiento SENASA')
    onelab_senasa_alert = fields.Boolean(string='Alerta de vencimiento SENASA', compute='_compute_senasa_alert', store=True)

    # SIMELA
    onelab_simela = fields.Boolean(string='SIMELA')

    # ANMAT
    onelab_anmat_entity_type = fields.Char(string='Tipo de entidad ANMAT')
    onelab_anmat_cert_number = fields.Char(string='Número de certificado ANMAT')
    onelab_anmat_validity = fields.Date(string='Vigencia ANMAT')
    onelab_anmat_attachment = fields.Binary(string='Adjunto certificado ANMAT')
    onelab_anmat_attachment_filename = fields.Char(string='Nombre del archivo ANMAT')

    # RENPRE
    onelab_renpre_required = fields.Boolean(string='¿Requiere RENPRE?')
    onelab_renpre_type = fields.Selection([
        ('lista_i', 'LISTA I'),
        ('lista_ii', 'LISTA II'),
        ('lista_iii', 'LISTA III'),
    ], string='Tipo RENPRE')

    # Vencimiento mínimo aceptado
    onelab_min_expiry_days = fields.Integer(string='Vencimiento mínimo aceptado (días)')

    @api.depends('onelab_senasa_expiration')
    def _compute_senasa_alert(self):
        for record in self:
            if record.onelab_senasa_expiration:
                record.onelab_senasa_alert = record.onelab_senasa_expiration <= date.today() + timedelta(days=30)
            else:
                record.onelab_senasa_alert = False
