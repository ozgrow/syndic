# -*- coding: utf-8 -*-
'''
diacamma.condominium views package: general assemblies (agenda)

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

from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from lucterios.framework.xferadvance import XferListEditor, XferAddEditor, XferShowEditor, XferDelete, \
    TITLE_ADD, TITLE_MODIFY, TITLE_DELETE, TITLE_EDIT, TITLE_CREATE, TITLE_PRINT, TITLE_OK, TITLE_CANCEL
from lucterios.framework.xfergraphic import XferContainerAcknowledge
from lucterios.framework.xfercomponents import XferCompSelect, XferCompCheckList, XferCompImage
from lucterios.framework.tools import ActionsManage, MenuManage, WrapAction, FORMTYPE_NOMODAL, CLOSE_NO, CLOSE_YES, \
    SELECT_SINGLE, SELECT_MULTI
from lucterios.framework.error import LucteriosException, IMPORTANT
from lucterios.CORE.xferprint import XferPrintReporting

from diacamma.condominium.models import Assembly, AgendaItem

MenuManage.add_sub("condominium.assembly", "condominium", short_icon='mdi:mdi-account-group-outline', caption=_("General assemblies"),
                   desc=_("Preparation of general assemblies"), pos=15)


def in_assembly(xfer):
    return isinstance(xfer.item, Assembly)


def assembly_in_building(xfer):
    return in_assembly(xfer) and (xfer.item.status == Assembly.STATUS_BUILDING)


def can_edit_item(xfer, gridname=''):
    return (not in_assembly(xfer)) or assembly_in_building(xfer)


@MenuManage.describ('condominium.change_assembly', FORMTYPE_NOMODAL, 'condominium.assembly', _('Manage of general assemblies'))
class AssemblyList(XferListEditor):
    short_icon = "mdi:mdi-account-group-outline"
    model = Assembly
    field_id = 'assembly'
    caption = _("General assemblies")


@ActionsManage.affect_grid(TITLE_CREATE, short_icon='mdi:mdi-pencil-plus')
@ActionsManage.affect_show(TITLE_MODIFY, short_icon='mdi:mdi-pencil-outline', close=CLOSE_YES, condition=lambda xfer: xfer.item.status == Assembly.STATUS_BUILDING)
@MenuManage.describ('condominium.add_assembly')
class AssemblyAddModify(XferAddEditor):
    short_icon = "mdi:mdi-account-group-outline"
    model = Assembly
    field_id = 'assembly'
    caption_add = _("Add general assembly")
    caption_modify = _("Modify general assembly")
    redirect_to_show = 'Show'


@ActionsManage.affect_grid(TITLE_EDIT, short_icon='mdi:mdi-text-box-outline', unique=SELECT_SINGLE)
@MenuManage.describ('condominium.change_assembly')
class AssemblyShow(XferShowEditor):
    short_icon = "mdi:mdi-account-group-outline"
    model = Assembly
    field_id = 'assembly'
    caption = _("Show general assembly")


@ActionsManage.affect_grid(TITLE_DELETE, short_icon='mdi:mdi-delete-outline', unique=SELECT_MULTI)
@MenuManage.describ('condominium.delete_assembly')
class AssemblyDel(XferDelete):
    short_icon = "mdi:mdi-account-group-outline"
    model = Assembly
    field_id = 'assembly'
    caption = _("Delete general assembly")

    def fillresponse(self):
        for item in self.items:
            if item.status != Assembly.STATUS_BUILDING:
                raise LucteriosException(IMPORTANT, _('Only a general assembly in building can be deleted!'))
        XferDelete.fillresponse(self)


@ActionsManage.affect_grid(TITLE_PRINT, short_icon='mdi:mdi-printer-outline', unique=SELECT_SINGLE)
@ActionsManage.affect_show(TITLE_PRINT, short_icon='mdi:mdi-printer-outline', close=CLOSE_NO)
@MenuManage.describ('condominium.change_assembly')
class AssemblyPrint(XferPrintReporting):
    short_icon = "mdi:mdi-account-group-outline"
    model = Assembly
    field_id = 'assembly'
    caption = _("Print agenda")

    def items_callback(self):
        return self.items

    def get_print_name(self):
        return "%s - %s" % (_('agenda'), self.items[0]) if len(self.items) == 1 else str(self.caption)


@MenuManage.describ('condominium.change_assembly', FORMTYPE_NOMODAL, 'condominium.assembly', _('Agenda items waiting for a general assembly'))
class AgendaItemList(XferListEditor):
    short_icon = "mdi:mdi-format-list-numbered"
    model = AgendaItem
    field_id = 'agendaitem'
    caption = _("Pending agenda items")

    def fillresponse_header(self):
        self.filter = Q(assembly__isnull=True)

    def fillresponse(self):
        XferListEditor.fillresponse(self)
        self.get_components(self.field_id).delete_header('num')


@ActionsManage.affect_grid(TITLE_ADD, short_icon='mdi:mdi-pencil-plus-outline', condition=can_edit_item)
@ActionsManage.affect_grid(TITLE_MODIFY, short_icon='mdi:mdi-pencil-outline', unique=SELECT_SINGLE, condition=can_edit_item)
@MenuManage.describ('condominium.add_assembly')
class AgendaItemAddModify(XferAddEditor):
    short_icon = "mdi:mdi-format-list-numbered"
    model = AgendaItem
    field_id = 'agendaitem'
    caption_add = _("Add agenda item")
    caption_modify = _("Modify agenda item")


@ActionsManage.affect_grid(TITLE_EDIT, short_icon='mdi:mdi-text-box-outline', unique=SELECT_SINGLE)
@MenuManage.describ('condominium.change_assembly')
class AgendaItemShow(XferShowEditor):
    short_icon = "mdi:mdi-format-list-numbered"
    model = AgendaItem
    field_id = 'agendaitem'
    caption = _("Show agenda item")


@ActionsManage.affect_grid(TITLE_DELETE, short_icon='mdi:mdi-delete-outline', unique=SELECT_MULTI, condition=can_edit_item)
@MenuManage.describ('condominium.delete_assembly')
class AgendaItemDel(XferDelete):
    short_icon = "mdi:mdi-format-list-numbered"
    model = AgendaItem
    field_id = 'agendaitem'
    caption = _("Delete agenda item")

    def fillresponse(self):
        assemblies = {item.assembly for item in self.items if item.assembly is not None}
        XferDelete.fillresponse(self)
        for assembly in assemblies:
            assembly.renumber()


@ActionsManage.affect_grid(_('Up'), short_icon='mdi:mdi-arrow-up-bold-outline', unique=SELECT_SINGLE, condition=lambda xfer, gridname='': assembly_in_building(xfer))
@MenuManage.describ('condominium.add_assembly')
class AgendaItemUp(XferContainerAcknowledge):
    short_icon = "mdi:mdi-format-list-numbered"
    model = AgendaItem
    field_id = 'agendaitem'
    caption = _("Up agenda item")

    def fillresponse(self):
        self.item.up_order()


@ActionsManage.affect_grid(_('Down'), short_icon='mdi:mdi-arrow-down-bold-outline', unique=SELECT_SINGLE, condition=lambda xfer, gridname='': assembly_in_building(xfer))
@MenuManage.describ('condominium.add_assembly')
class AgendaItemDown(XferContainerAcknowledge):
    short_icon = "mdi:mdi-format-list-numbered"
    model = AgendaItem
    field_id = 'agendaitem'
    caption = _("Down agenda item")

    def fillresponse(self):
        self.item.down_order()


@ActionsManage.affect_grid(_('Withdraw'), short_icon='mdi:mdi-tray-arrow-up', unique=SELECT_MULTI, condition=lambda xfer, gridname='': assembly_in_building(xfer))
@MenuManage.describ('condominium.add_assembly')
class AgendaItemWithdraw(XferContainerAcknowledge):
    short_icon = "mdi:mdi-format-list-numbered"
    model = AgendaItem
    field_id = 'agendaitem'
    caption = _("Withdraw agenda item")

    def fillresponse(self):
        if self.confirme(_('Do you want to withdraw these agenda items? They will wait for another general assembly.')):
            for item in self.items:
                item.detach()


@ActionsManage.affect_grid(_('Add pending items'), short_icon='mdi:mdi-tray-arrow-down', condition=lambda xfer, gridname='': assembly_in_building(xfer) and AgendaItem.objects.filter(assembly__isnull=True).exists())
@MenuManage.describ('condominium.add_assembly')
class AssemblyAddPendingItems(XferContainerAcknowledge):
    short_icon = "mdi:mdi-format-list-numbered"
    model = Assembly
    field_id = 'assembly'
    caption = _("Add pending agenda items")

    def fillresponse(self, pending_items=()):
        if self.getparam('SAVE') is None:
            dlg = self.create_custom(model=AgendaItem)
            img = XferCompImage('img')
            img.set_value(self.short_icon, '#')
            img.set_location(0, 0)
            dlg.add_component(img)
            sel = XferCompCheckList('pending_items')
            sel.set_select_query(AgendaItem.objects.filter(assembly__isnull=True))
            sel.set_location(1, 0)
            sel.description = _('pending agenda items')
            dlg.add_component(sel)
            dlg.add_action(self.return_action(TITLE_OK, short_icon='mdi:mdi-check'), params={"SAVE": "YES"})
            dlg.add_action(WrapAction(TITLE_CANCEL, short_icon='mdi:mdi-cancel'))
        else:
            for item in AgendaItem.objects.filter(id__in=pending_items, assembly__isnull=True).order_by('id'):
                item.attach(self.item)


@ActionsManage.affect_grid(_('Add from template'), short_icon='mdi:mdi-text-box-plus-outline', condition=can_edit_item)
@MenuManage.describ('condominium.add_assembly')
class AgendaItemAddFromTemplate(XferContainerAcknowledge):
    short_icon = "mdi:mdi-format-list-numbered"
    model = AgendaItem
    field_id = 'agendaitem'
    caption = _("Add agenda items from template")

    def fillresponse(self, templates=(), assembly=0):
        if self.getparam('SAVE') is None:
            dlg = self.create_custom(model=AgendaItem)
            img = XferCompImage('img')
            img.set_value(self.short_icon, '#')
            img.set_location(0, 0)
            dlg.add_component(img)
            sel = XferCompCheckList('templates')
            sel.set_select([(index, "%s (%s)" % (title, dict(AgendaItem.LIST_MAJORITIES)[majority] if majority is not None else _('information (no vote)')))
                            for index, (title, _text, _kind, majority) in enumerate(AgendaItem.get_templates())])
            sel.set_location(1, 0)
            sel.description = _('templates')
            dlg.add_component(sel)
            dlg.add_action(self.return_action(TITLE_OK, short_icon='mdi:mdi-check'), params={"SAVE": "YES"})
            dlg.add_action(WrapAction(TITLE_CANCEL, short_icon='mdi:mdi-cancel'))
        else:
            target = Assembly.objects.get(id=assembly) if assembly != 0 else None
            AgendaItem.create_from_templates(templates, target)


@ActionsManage.affect_grid(_('Add to assembly'), short_icon='mdi:mdi-tray-arrow-down', unique=SELECT_MULTI, condition=lambda xfer, gridname='': (not in_assembly(xfer)) and Assembly.objects.filter(status=Assembly.STATUS_BUILDING).exists())
@MenuManage.describ('condominium.add_assembly')
class AgendaItemAttach(XferContainerAcknowledge):
    short_icon = "mdi:mdi-format-list-numbered"
    model = AgendaItem
    field_id = 'agendaitem'
    caption = _("Add to general assembly")

    def fillresponse(self, target_assembly=0):
        if self.getparam('SAVE') is None:
            dlg = self.create_custom(model=AgendaItem)
            img = XferCompImage('img')
            img.set_value(self.short_icon, '#')
            img.set_location(0, 0)
            dlg.add_component(img)
            sel = XferCompSelect('target_assembly')
            sel.set_needed(True)
            sel.set_select_query(Assembly.objects.filter(status=Assembly.STATUS_BUILDING))
            sel.set_location(1, 0)
            sel.description = _('general assembly')
            dlg.add_component(sel)
            dlg.add_action(self.return_action(TITLE_OK, short_icon='mdi:mdi-check'), params={"SAVE": "YES"})
            dlg.add_action(WrapAction(TITLE_CANCEL, short_icon='mdi:mdi-cancel'))
        else:
            assembly = Assembly.objects.get(id=target_assembly)
            for item in self.items:
                if item.assembly is None:
                    item.attach(assembly)
