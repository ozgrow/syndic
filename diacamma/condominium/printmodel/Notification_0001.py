# -*- coding: utf-8 -*-
'''
Printmodel django module for condominium

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

from diacamma.condominium.models import Notification

name = _("notice of meeting")
kind = 2
modelname = Notification.get_long_name()
value = """
<model hmargin="10.0" vmargin="10.0" page_width="210.0" page_height="297.0">
<header extent="25.0">
<text height="10.0" width="120.0" top="0.0" left="70.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="20" font_family="sans-serif" font_weight="" font_size="20">
{[b]}#OUR_DETAIL.name{[/b]}
</text>
<text height="10.0" width="120.0" top="10.0" left="70.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="8" font_family="sans-serif" font_weight="" font_size="8">
{[italic]}
#OUR_DETAIL.address - #OUR_DETAIL.postal_code #OUR_DETAIL.city - #OUR_DETAIL.tel1 #OUR_DETAIL.tel2 #OUR_DETAIL.email{[br/]}#OUR_DETAIL.identify_number
{[/italic]}
</text>
<image height="25.0" width="30.0" top="0.0" left="10.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2">
#OUR_DETAIL.image
</image>
</header>
<bottom extent="10.0">
</bottom>
<body>
<text height="20.0" width="100.0" top="0.0" left="90.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
{[b]}#owner.third.contact.str{[/b]}{[br/]}#owner.third.contact.address{[br/]}#owner.third.contact.postal_code #owner.third.contact.city
</text>
<text height="10.0" width="190.0" top="25.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="15" font_family="sans-serif" font_weight="" font_size="15">
{[b]}%(title)s{[/b]}
</text>
<text height="20.0" width="190.0" top="37.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
%(intro)s{[br/]}
{[b]}%(type)s :{[/b]} #assembly.type_assembly{[br/]}
{[b]}%(date)s :{[/b]} #assembly.date #assembly.hour{[br/]}
{[b]}%(place)s :{[/b]} #assembly.place
</text>
<text height="8.0" width="190.0" top="60.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
{[b]}%(agenda)s{[/b]}
</text>
<table height="20.0" width="190.0" top="68.0" left="0.0" padding="1.0" spacing="0.1" border_color="black" border_style="" border_width="0.2">
    <columns width="12.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(num)s{[/b]}
    </columns>
    <columns width="128.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(item)s{[/b]}
    </columns>
    <columns width="50.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">
    {[b]}%(majority)s{[/b]}
    </columns>
    <rows data="agendaitem_set">
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="9" font_family="sans-serif" font_weight="" font_size="9">
#num
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="9" font_family="sans-serif" font_weight="" font_size="9">
{[b]}#title{[/b]}{[br/]}#text
        </cell>
        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="8" font_family="sans-serif" font_weight="" font_size="8">
#kind{[br/]}#majority
        </cell>
    </rows>
</table>
<text height="8.0" width="190.0" top="95.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
{[b]}%(attachments)s{[/b]}
</text>
<text height="5.0" width="185.0" top="103.0" left="5.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="10" font_family="sans-serif" font_weight="" font_size="10" data="assemblyattachment_set">
- #title
</text>
<text height="25.0" width="190.0" top="110.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="10" font_family="sans-serif" font_weight="" font_size="10">
%(postal_vote)s{[br/]}{[br/]}
{[i]}%(postal_request)s{[/i]}
</text>
<text height="15.0" width="80.0" top="140.0" left="110.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="11" font_family="sans-serif" font_weight="" font_size="11">
%(syndic)s
</text>
</body>
</model>""" % {'title': _('Notice of the general assembly'),
               'intro': _('Dear owner, you are convened to the general assembly of the co-owners, which will be held:'),
               'type': _('type of assembly'), 'date': _('date'), 'place': _('place'),
               'agenda': _('Agenda'), 'num': _('N°'), 'item': _('agenda item'), 'majority': _('majority'),
               'attachments': _('Attached documents'),
               'postal_vote': _('If you cannot attend, you may be represented by a proxy, or vote by post with the attached form: '
                                'the form must reach the syndic at least 3 full days before the general assembly.'),
               'postal_request': _('You may ask at any time, by any means giving a certain date, to receive the notices of meeting, '
                                   'the minutes and the calls for funds by post (article 64-2 of the decree of 17 March 1967).'),
               'syndic': _('The syndic')}
mode = 0
