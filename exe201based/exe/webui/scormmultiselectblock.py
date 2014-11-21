# ===========================================================================
# eXe 
# Copyright 2004-2006, University of Auckland
# Copyright 2006-2007 eXe Project, New Zealand Tertiary Education Commission
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================
"""
MultiSelectBlock can render and process MultiSelectIdevices as XHTML
"""

import logging
from exe.webui.block        import Block
from exe.webui              import common
from exe.webui.element      import ScormSelectquestionElement,TextAreaElement

log = logging.getLogger(__name__)


# ===========================================================================
class ScormMultiSelectBlock(Block):
    """
    ScormMultiSelectBlock can render and process MultiSelectIdevices as XHTML
    """
    def __init__(self, parent, idevice):
        """
        Initialize a new Block object
        """
        Block.__init__(self, parent, idevice)
        self.idevice           = idevice
        self.questionElements  = []

        for question in idevice.questions:
            self.questionElements.append(ScormSelectquestionElement(question))


    def process(self, request):
        """
        Process the request arguments from the web server
        """
        Block.process(self, request)
        
            
        if ("addQuestion"+self.id) in request.args: 
            self.idevice.addQuestion()
            self.idevice.edit = True

        for element in self.questionElements:
            element.process(request)

        if "title"+self.id in request.args:
            self.idevice.title = request.args["title"+self.id][0]
            

    def renderEdit(self, style):
        """
        Returns an XHTML string with the form element for editing this block
        """
        html  = "<div class=\"iDevice\">\n"
        html += common.textInput("title"+self.id, self.idevice.title)
        html += u"<br/><br/>\n"
        

        for element in self.questionElements:
            html += element.renderEdit() 
            
        #value = _("Add another Question")    
        #html += "<br/>" 
        #html += common.submitButton("addQuestion"+self.id, value)
        
        html += "<br/><br/>" + self.renderEditButtons()
        html += "</div>\n"


        return html

    def renderPreview(self, style):
        """
        Returns an XHTML string for previewing this block
        """
        html  = u"<div class=\"iDevice "
        html += u"emphasis"+unicode(self.idevice.emphasis)+"\" "
        html += u"ondblclick=\"submitLink('edit',"+self.id+", 0);\">\n"
        html += u'<img alt="" class="iDevice_icon" '
        html += u"src=\"/style/"+style+"/icon_"+self.idevice.icon
        html += ".gif\" />\n"
        html += u"<span class=\"iDeviceTitle\">"       
        html += self.idevice.title+"</span>\n"
        html += u'<div class="iDevice_inner">\n'

        for element in self.questionElements:
            html += element.renderPreview() + "<br/>"
        
        html += u"</div>\n"
        html += self.renderViewButtons()
        html += u"</div>\n"
        return html
    
    
    def renderView(self, style):
        """
        Returns an XHTML string for viewing this block
        """
        html  = u'<div class="iDevice '
        html += u'emphasis'+unicode(self.idevice.emphasis)+'">\n'
        html += u'<img alt="" class="iDevice_icon" '
        html += u'src="icon_'+self.idevice.icon+'.gif" />\n'
        html += u'<span class="iDeviceTitle">'
        html += self.idevice.title+'</span>\n'
        html += u'<div class="iDevice_inner">\n'
        for element in self.questionElements:
            html += element.renderView()

        html += "</div></div>\n"

        return html
    


from exe.engine.scormmultiselectidevice import ScormMultiSelectIdevice
from exe.webui.blockfactory        import g_blockFactory
g_blockFactory.registerBlockType(ScormMultiSelectBlock, ScormMultiSelectIdevice)  


# ===========================================================================
