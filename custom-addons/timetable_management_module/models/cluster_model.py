from odoo import models, fields


class ClusterModel(models.Model):
    _name = "cluster_model"

    name = fields.Char(string="Cluster")
