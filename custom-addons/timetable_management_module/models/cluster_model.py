from odoo import models, fields


class ClusterModel(models.Model):
    _name = "cluster_model"
    _description = "Cluster Model"

    name = fields.Char(string="Cluster")
