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



    # @api.onchange('onelab_senasa_expiration', 'onelab_min_expiry_days')
    # def _onchange_senasa_expiry_warning(self):
    #     for record in self:
    #         if record.onelab_senasa_expiration and record.onelab_min_expiry_days:
    #             threshold = date.today() + timedelta(days=record.onelab_min_expiry_days)
    #             if record.onelab_senasa_expiration <= threshold:
    #                 return {
    #                     'warning': {
    #                         'title': 'Alerta de vencimiento SENASA',
    #                         'message': '⚠️ El certificado SENASA está próximo a vencer según el mínimo aceptado.',
    #                     }
    #                 }
    @api.onchange('onelab_senasa_expiration')
    def _onchange_senasa_expiry_warning(self):
        for record in self:
            if record.onelab_senasa_expiration:
                threshold = date.today() + timedelta(days=45)
                if record.onelab_senasa_expiration <= threshold:
                    formatted_date = record.onelab_senasa_expiration.strftime('%d/%m/%Y')

                    cert_number = record.onelab_senasa_cert_number or 'sin numero registrado'
                    return {
                        'warning': {
                            'title': 'Alerta de vencimiento SENASA',
                            'message': f'⚠️ El certificado SENASA {cert_number}está próximo a vencer (menos de 45 días). Vencimiento: {formatted_date} '
                        }
                    }
#verificacion de fecha en ventas

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_senasa_expiry(self):
        for line in self:
            product = line.product_id.product_tmpl_id
            if product.onelab_senasa_expiration:
                threshold = date.today() + timedelta(days=45)
                if product.onelab_senasa_expiration <= threshold:
                    formatted_date = product.onelab_senasa_expiration.strftime('%d/%m/%Y')
                    cert_number = product.onelab_senasa_cert_number or 'sin número registrado'
                    return {
                        'warning': {
                            'title': 'Alerta de vencimiento SENASA',
                            'message': f'⚠️ El certificado SENASA {cert_number} está próximo a vencer (menos de 45 días). Vencimiento: {formatted_date}'
                        }
                    }


#verificacion en compras
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def _onchange_product_senasa_expiry(self):
        for line in self:
            product = line.product_id.product_tmpl_id
            if product.onelab_senasa_expiration:
                threshold = date.today() + timedelta(days=45)
                if product.onelab_senasa_expiration <= threshold:
                    formatted_date = product.onelab_senasa_expiration.strftime('%d/%m/%Y')
                    cert_number = product.onelab_senasa_cert_number or 'sin número registrado'
                    return {
                        'warning': {
                            'title': 'Alerta de vencimiento SENASA',
                            'message': f'⚠️ El certificado SENASA {cert_number} está próximo a vencer (menos de 45 días). Vencimiento: {formatted_date}'
                        }
                    }