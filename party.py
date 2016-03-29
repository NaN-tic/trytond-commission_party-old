# This file is part commission_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields, ModelSQL
from trytond.pool import PoolMeta

__all__ = ['Party', 'PartyAgent', 'Invoice', 'Sale', 'Opportunity']


class Party:
    __metaclass__ = PoolMeta
    __name__ = 'party.party'
    agents = fields.Many2Many('party-commission.agent',
            'party', 'agent', 'Agents',
            help='Agents where this party will be related.')


class PartyAgent(ModelSQL):
    'Party - Commission Agent'
    __name__ = 'party-commission.agent'
    _table = 'party_commission_agent'
    party = fields.Many2One('party.party', 'Party',
        ondelete='CASCADE', select=True, required=True)
    agent = fields.Many2One('commission.agent', 'Agent', ondelete='RESTRICT',
        select=True, required=True)


class Sale:
    __metaclass__ = PoolMeta
    __name__ = 'sale.sale'

    @fields.depends('agent', 'party')
    def on_change_party(self):
        self.agent = None
        super(Sale, self).on_change_party()
        if self.party and self.party.agents and not self.agent:
            if len(self.party.agents) == 1:
                self.agent = self.party.agents[0]


class Opportunity:
    __metaclass__ = PoolMeta
    __name__ = 'sale.opportunity'

    def _get_sale_opportunity(self):
        sale = super(Opportunity, self)._get_sale_opportunity()
        if self.party and self.party.agents:
            if len(self.party.agents) == 1:
                sale.agent = self.party.agents[0]
                sale.on_change_agent()
        return sale


class Invoice:
    __metaclass__ = PoolMeta
    __name__ = 'account.invoice'

    @fields.depends('agent', 'party')
    def on_change_party(self):
        self.agent = None
        super(Invoice, self).on_change_party()
        if self.party and self.party.agents and not self.agent:
            if len(self.party.agents) == 1:
                self.agent = self.party.agents[0]
