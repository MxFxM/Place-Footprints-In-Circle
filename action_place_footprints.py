import pcbnew
import math
import os
import sys
import wx

if __name__ == '__main__':
    import circlesettings
else:
    from . import circlesettings

def reference(footprint):
        return int(footprint.GetReference()[1:])

class InitialDialog(circlesettings.MyDialog1):
    # hack for new wxFormBuilder generating code incompatible with old wxPython
    # noinspection PyMethodOverriding
    def SetSizeHints(self, sz1, sz2):
        # DO NOTHING
        pass

    def __init__(self, parent):
        circlesettings.MyDialog1.__init__(self, parent)

class PlaceFootprintsInCircle(pcbnew.ActionPlugin):
    """
    A script to replicate layout
    How to use:
    - move to GAL
    - select footprint of layout to replicate
    - call the plugin
    - enter pivot step and confirm pivot footprint
    """

    def defaults(self):
        self.name = "Place footprints in a circle"
        self.category = "Modify Drawing PCB"
        self.description = "Place footprints along a predefined circle with given radius"
        self.icon_file_name = os.path.join(
                os.path.dirname(__file__), 'array-place_footprints.svg.png')

    def Run(self):
        # load board
        board = pcbnew.GetBoard()

        # get user units
        if pcbnew.GetUserUnits() == 1:
            user_units = 'mm'
        else:
            user_units = 'in'
        
        SCALE = 1000000.0
        
        # go to the project folder - so that log will be in proper place
        os.chdir(os.path.dirname(os.path.abspath(board.GetFileName())))
        
        selected_footprints = [x for x in pcbnew.GetBoard().GetFootprints() if x.IsSelected()]
        selected_names = []
        for mod in selected_footprints:
            selected_names.append(f"{mod.GetReference()}")
        
        selected_footprints.sort(key=reference)
        
        _pcbnew_frame = [x for x in wx.GetTopLevelWindows() if 'pcb' in x.GetTitle().lower()][0]
        
        with InitialDialog(_pcbnew_frame) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                if user_units == 'mm':
                    radius = float(dlg.m_textCtrl1.GetValue())
                else:
                    radius = float(dlg.m_textCtrl1.GetValue())/25.4
                offsetrotation = float(dlg.m_textCtrl2.GetValue()) / 360 * 2 * math.pi
                spacing = 2 * math.pi / len(selected_footprints)
                rotation = spacing
                for index, footprint in enumerate(selected_footprints):
                    angle = spacing * index
                    x = math.cos(angle) * radius * SCALE
                    y = math.sin(angle) * radius * SCALE
                    position = [int(x), int(y)]
                    footprint.SetPosition(pcbnew.wxPoint(*position))
                    footprint.SetOrientationDegrees(180 - (angle + offsetrotation) / (2 * math.pi) * 360)
                
                pcbnew.Refresh()
            else:
                # cancel
                pcbnew.Refresh()