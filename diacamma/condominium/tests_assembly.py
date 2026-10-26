# -*- coding: utf-8 -*-
'''
diacamma.condominium tests package: general assemblies (agenda)

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2026 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import unicode_literals

from lucterios.framework.test import LucteriosTest
from lucterios.CORE.models import PrintModel

from diacamma.accounting.test_tools import initial_thirds_fr, default_compta_fr, default_costaccounting
from diacamma.payoff.test_tools import default_bankaccount_fr
from diacamma.condominium.test_tools import default_setowner_fr
from diacamma.condominium.models import Assembly, AgendaItem
from diacamma.condominium.views_assembly import AssemblyList, AssemblyAddModify, AssemblyShow, AssemblyDel, AssemblyPrint, \
    AgendaItemList, AgendaItemAddModify, AgendaItemShow, AgendaItemDel, AgendaItemUp, AgendaItemDown, AgendaItemWithdraw, \
    AssemblyAddPendingItems, AgendaItemAttach, AgendaItemAddFromTemplate


class AssemblyAgendaTest(LucteriosTest):

    def setUp(self):
        initial_thirds_fr()
        LucteriosTest.setUp(self)
        default_compta_fr(with12=False)
        default_costaccounting()
        default_bankaccount_fr()
        default_setowner_fr()

    def _add_pending_item(self, title, **params):
        params.update({'SAVE': 'YES', 'title': title, 'text': 'text of %s' % title})
        self.factory.xfer = AgendaItemAddModify()
        self.calljson('/diacamma.condominium/agendaItemAddModify', params, False)
        self.assert_observer('core.acknowledge', 'diacamma.condominium', 'agendaItemAddModify')

    def _add_assembly(self):
        self.factory.xfer = AssemblyAddModify()
        self.calljson('/diacamma.condominium/assemblyAddModify', {'SAVE': 'YES', 'date': '2027-06-15', 'hour': '18:30', 'place': 'salle commune', 'type_assembly': 0}, False)
        self.assert_observer('core.acknowledge', 'diacamma.condominium', 'assemblyAddModify')
        return Assembly.objects.order_by('-id').first()

    def _check_agenda(self, assembly_id, titles):
        self.factory.xfer = AssemblyShow()
        self.calljson('/diacamma.condominium/assemblyShow', {'assembly': assembly_id}, False)
        self.assert_observer('core.custom', 'diacamma.condominium', 'assemblyShow')
        self.assert_count_equal('agendaitem', len(titles))
        for index, title in enumerate(titles):
            self.assert_json_equal('', 'agendaitem/@%d/num' % index, index + 1)
            self.assert_json_equal('', 'agendaitem/@%d/title' % index, title)

    def test_pending_items(self):
        self.factory.xfer = AgendaItemList()
        self.calljson('/diacamma.condominium/agendaItemList', {}, False)
        self.assert_observer('core.custom', 'diacamma.condominium', 'agendaItemList')
        self.assert_count_equal('agendaitem', 0)

        self.factory.xfer = AgendaItemAddModify()
        self.calljson('/diacamma.condominium/agendaItemAddModify', {}, False)
        self.assert_observer('core.custom', 'diacamma.condominium', 'agendaItemAddModify')
        self.assert_json_equal('SELECT', 'kind', '0')
        self.assert_json_equal('SELECT', 'majority', '0')
        self.assert_json_equal('SELECT', 'requested_by', '0')

        self._add_pending_item('Fonds de travaux', majority=1)
        self._add_pending_item('Présentation du DTG', kind=1, majority=1)
        self._add_pending_item('Remplacement de la porte', requested_by=2, request_date='2026-11-02')

        self.factory.xfer = AgendaItemList()
        self.calljson('/diacamma.condominium/agendaItemList', {}, False)
        self.assert_count_equal('agendaitem', 3)
        self.assert_json_equal('', 'agendaitem/@0/title', 'Fonds de travaux')
        self.assert_json_equal('', 'agendaitem/@0/majority', 1)
        self.assert_json_equal('', 'agendaitem/@1/kind', 1)
        self.assert_json_equal('', 'agendaitem/@1/majority', None)
        self.assert_json_equal('', 'agendaitem/@2/requested_by', 'Dalton William')

        information = AgendaItem.objects.get(title='Présentation du DTG')
        self.assertEqual(information.majority, None)
        self.assertEqual(information.assembly, None)
        self.assertEqual(information.num, None)

        self.factory.xfer = AgendaItemShow()
        self.calljson('/diacamma.condominium/agendaItemShow', {'agendaitem': information.id}, False)
        self.assert_observer('core.custom', 'diacamma.condominium', 'agendaItemShow')
        self.assertFalse('majority' in self.json_data.keys())

    def test_assembly_with_opening_items(self):
        self.factory.xfer = AssemblyList()
        self.calljson('/diacamma.condominium/assemblyList', {}, False)
        self.assert_observer('core.custom', 'diacamma.condominium', 'assemblyList')
        self.assert_count_equal('assembly', 0)

        assembly = self._add_assembly()
        self.assertEqual(assembly.status, Assembly.STATUS_BUILDING)
        self._check_agenda(assembly.id, ['Président de séance', 'Scrutateur(s)', 'Secrétaire de séance'])

        self.factory.xfer = AssemblyAddModify()
        self.calljson('/diacamma.condominium/assemblyAddModify', {'SAVE': 'YES', 'assembly': assembly.id, 'place': 'chez le syndic'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.condominium', 'assemblyAddModify')
        self._check_agenda(assembly.id, ['Président de séance', 'Scrutateur(s)', 'Secrétaire de séance'])

        self.factory.xfer = AssemblyList()
        self.calljson('/diacamma.condominium/assemblyList', {}, False)
        self.assert_count_equal('assembly', 1)
        self.assert_json_equal('', 'assembly/@0/place', 'chez le syndic')

    def test_attach_order_withdraw(self):
        self._add_pending_item('Fonds de travaux')
        self._add_pending_item('Plan pluriannuel de travaux')
        self._add_pending_item('Durée du mandat du syndic')
        assembly = self._add_assembly()
        fund, plan, mandate = AgendaItem.objects.filter(assembly__isnull=True).order_by('id')

        self.factory.xfer = AgendaItemAttach()
        self.calljson('/diacamma.condominium/agendaItemAttach', {'agendaitem': '%d;%d' % (fund.id, plan.id)}, False)
        self.assert_observer('core.custom', 'diacamma.condominium', 'agendaItemAttach')
        self.assert_select_equal('target_assembly', 1)

        self.factory.xfer = AgendaItemAttach()
        self.calljson('/diacamma.condominium/agendaItemAttach', {'agendaitem': '%d;%d' % (fund.id, plan.id), 'SAVE': 'YES', 'target_assembly': assembly.id}, False)
        self.assert_observer('core.acknowledge', 'diacamma.condominium', 'agendaItemAttach')
        self._check_agenda(assembly.id, ['Président de séance', 'Scrutateur(s)', 'Secrétaire de séance', 'Fonds de travaux', 'Plan pluriannuel de travaux'])

        self.factory.xfer = AssemblyAddPendingItems()
        self.calljson('/diacamma.condominium/assemblyAddPendingItems', {'assembly': assembly.id, 'SAVE': 'YES', 'pending_items': str(mandate.id)}, False)
        self.assert_observer('core.acknowledge', 'diacamma.condominium', 'assemblyAddPendingItems')
        self._check_agenda(assembly.id, ['Président de séance', 'Scrutateur(s)', 'Secrétaire de séance', 'Fonds de travaux', 'Plan pluriannuel de travaux', 'Durée du mandat du syndic'])

        self.factory.xfer = AgendaItemUp()
        self.calljson('/diacamma.condominium/agendaItemUp', {'agendaitem': mandate.id}, False)
        self.assert_observer('core.acknowledge', 'diacamma.condominium', 'agendaItemUp')
        self.factory.xfer = AgendaItemUp()
        self.calljson('/diacamma.condominium/agendaItemUp', {'agendaitem': mandate.id}, False)
        self._check_agenda(assembly.id, ['Président de séance', 'Scrutateur(s)', 'Secrétaire de séance', 'Durée du mandat du syndic', 'Fonds de travaux', 'Plan pluriannuel de travaux'])

        self.factory.xfer = AgendaItemDown()
        self.calljson('/diacamma.condominium/agendaItemDown', {'agendaitem': plan.id}, False)
        self.assert_observer('core.acknowledge', 'diacamma.condominium', 'agendaItemDown')
        self._check_agenda(assembly.id, ['Président de séance', 'Scrutateur(s)', 'Secrétaire de séance', 'Durée du mandat du syndic', 'Fonds de travaux', 'Plan pluriannuel de travaux'])

        self.factory.xfer = AgendaItemWithdraw()
        self.calljson('/diacamma.condominium/agendaItemWithdraw', {'agendaitem': mandate.id, 'CONFIRME': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.condominium', 'agendaItemWithdraw')
        self._check_agenda(assembly.id, ['Président de séance', 'Scrutateur(s)', 'Secrétaire de séance', 'Fonds de travaux', 'Plan pluriannuel de travaux'])

        self.factory.xfer = AgendaItemList()
        self.calljson('/diacamma.condominium/agendaItemList', {}, False)
        self.assert_count_equal('agendaitem', 1)
        self.assert_json_equal('', 'agendaitem/@0/title', 'Durée du mandat du syndic')

    def test_add_item_in_assembly_and_delete(self):
        assembly = self._add_assembly()
        self._add_pending_item('Budget prévisionnel', assembly=assembly.id)
        self._check_agenda(assembly.id, ['Président de séance', 'Scrutateur(s)', 'Secrétaire de séance', 'Budget prévisionnel'])

        scrutineer = AgendaItem.objects.get(assembly=assembly, num=2)
        self.factory.xfer = AgendaItemDel()
        self.calljson('/diacamma.condominium/agendaItemDel', {'agendaitem': scrutineer.id, 'CONFIRME': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.condominium', 'agendaItemDel')
        self._check_agenda(assembly.id, ['Président de séance', 'Secrétaire de séance', 'Budget prévisionnel'])

        self._add_pending_item('Point en attente')
        self.factory.xfer = AssemblyDel()
        self.calljson('/diacamma.condominium/assemblyDel', {'assembly': assembly.id, 'CONFIRME': 'YES'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.condominium', 'assemblyDel')
        self.assertEqual(Assembly.objects.count(), 0)
        self.assertEqual(list(AgendaItem.objects.values_list('title', flat=True)), ['Point en attente'])

    def test_templates(self):
        self.factory.xfer = AgendaItemAddFromTemplate()
        self.calljson('/diacamma.condominium/agendaItemAddFromTemplate', {}, False)
        self.assert_observer('core.custom', 'diacamma.condominium', 'agendaItemAddFromTemplate')
        self.assert_select_equal('templates', len(AgendaItem.get_templates()), checked=True)

        self.factory.xfer = AgendaItemAddFromTemplate()
        self.calljson('/diacamma.condominium/agendaItemAddFromTemplate', {'SAVE': 'YES', 'templates': '2;10'}, False)
        self.assert_observer('core.acknowledge', 'diacamma.condominium', 'agendaItemAddFromTemplate')
        self.factory.xfer = AgendaItemList()
        self.calljson('/diacamma.condominium/agendaItemList', {}, False)
        self.assert_count_equal('agendaitem', 2)
        self.assert_json_equal('', 'agendaitem/@0/title', 'Désignation du syndic')
        self.assert_json_equal('', 'agendaitem/@0/majority', AgendaItem.MAJORITY_ART25)
        self.assert_json_equal('', 'agendaitem/@1/kind', AgendaItem.KIND_INFORMATION)
        self.assert_json_equal('', 'agendaitem/@1/majority', None)

        assembly = self._add_assembly()
        self.factory.xfer = AgendaItemAddFromTemplate()
        self.calljson('/diacamma.condominium/agendaItemAddFromTemplate', {'SAVE': 'YES', 'templates': '0;1', 'assembly': assembly.id}, False)
        self._check_agenda(assembly.id, ['Président de séance', 'Scrutateur(s)', 'Secrétaire de séance', 'Approbation des comptes', 'Budget prévisionnel'])

        self.factory.xfer = AgendaItemAddModify()
        self.calljson('/diacamma.condominium/agendaItemAddModify', {}, False)
        self.assertEqual(self.json_comp['majority_help']['component'], 'LABELFORM')

    def test_print_agenda(self):
        assembly = self._add_assembly()
        self._add_pending_item('Fonds de travaux', assembly=assembly.id, majority=1)
        print_model = PrintModel.objects.get(modelname=Assembly.get_long_name())
        self.factory.xfer = AssemblyPrint()
        self.calljson('/diacamma.condominium/assemblyPrint', {'assembly': assembly.id, 'PRINT_MODE': 3, 'MODEL': print_model.id}, False)
        self.assert_observer('core.print', 'diacamma.condominium', 'assemblyPrint')
        self.save_pdf()
