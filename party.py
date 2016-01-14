# This file is part commission_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields, ModelSQL
from trytond.pool import PoolMeta

__all__ = ['Party', 'PartyAgent', 'Invoice', 'Sale', 'Opportunity']
__metaclass__ = PoolMeta


class Party:
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
    __name__ = 'sale.sale'

    @fields.depends('agent', 'party')
    def on_change_party(self):
        changes = super(Sale, self).on_change_party()
        if self.party and self.party.agents and not self.agent:
            if len(self.party.agents) == 1:
                changes['agent'] = self.party.agents[0].id
                changes['agent.rec_name'] = self.party.agents[0].rec_name
        return changes


class Opportunity:
    __name__ = 'sale.opportunity'

    def _get_sale_opportunity(self):
        sale = super(Opportunity, self)._get_sale_opportunity()
        if self.party and self.party.agents:
            if len(self.party.agents) == 1: 
                sale.agent = self.party.agents[0]
                if hasattr(sale, 'on_change_agent'):
                    for k, v in sale.on_change_agent().iteritems():
                        setattr(sale, k, v)
        return sale


class Invoice:
    __name__ = 'account.invoice'

    @fields.depends('agent', 'party')
    def on_change_party(self):
        changes = super(Invoice, self).on_change_party()
        if self.party and self.party.agents and not self.agent:
            if len(self.party.agents) == 1:
                changes['agent'] = self.party.agents[0].id
                changes['agent.rec_name'] = self.party.agents[0].rec_name
        return changes
