""" Simple example to show that aspect_ratio for ZoomTool is not working

    HOW TO:
        1) Run ZoomTool_AspectRatio.py
        2) Zoom by creating a box with the left click
            a) the overlay must be square since aspect_ratio is 1
            b) make sur the mouse is far from the ending corner of the overlay when unclicking
        3) Zoom out by scrolling and see how the aspect ratio has changed!
        
    FIX: Comment line 330 of file better_selecting_zoom.py in chaco directory
"""

#-------------------------------------------------------------------------------
# Force Qt4 since issue with wx when clicking the window close button
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
#-------------------------------------------------------------------------------
from enable.api import ComponentEditor
from chaco.api import Plot, ArrayPlotData
from chaco.tools.api import ZoomTool, PanTool
from traits.api import HasTraits, Instance
from traitsui.api import View, UItem, Item, Group

#-------------------------------------------------------------------------------
class TestPlot(HasTraits):

    plot = Instance(Plot)
    plotdata = Instance(ArrayPlotData)

    view = View(
                UItem('plot', editor=ComponentEditor(), resizable=True, width = .8, height = .8,),
                resizable=True, width=.6, height=.8,
                )

    #---------------------------------------------------------------------------
    def _plotdata_default(self):
        self.plotdata = ArrayPlotData()
        self.plotdata.set_data("x1", [0, 1, 1, 0])
        self.plotdata.set_data("y1", [0, 0, 1, 1])
        self.plotdata.set_data("x2", [1, 2, 2, 1])
        self.plotdata.set_data("y2", [0, 0, 1, 1])
        self.plotdata.set_data("x3", [0, 1, 1, 0])
        self.plotdata.set_data("y3", [1, 1, 2, 2])
        self.plotdata.set_data("x4", [1, 2, 2, 1])
        self.plotdata.set_data("y4", [1, 1, 2, 2])
        return self.plotdata

    #---------------------------------------------------------------------------
    def _plot_default(self):

        self.plot = Plot(self.plotdata)
        self.plot.plot( ("x1", "y1"), type='polygon', face_color='auto' )
        self.plot.plot( ("x2", "y2"), type='polygon', face_color='auto'  )
        self.plot.plot( ("x3", "y3"), type='polygon', face_color='auto'  )
        self.plot.plot( ("x4", "y4"), type='polygon', face_color='auto'  )
        self.plot.aspect_ratio =  1.0

        # Add Pan & ZoomTool
        zoom = ZoomTool(self.plot, tool_mode="box",always_on=True,
                        zoom_factor=1.08, aspect_ratio=1.0)

        self.plot.overlays.append(zoom)
        return self.plot


#-------------------------------------------------------------------------------
if __name__ == '__main__':
    tst = TestPlot()
    tst.configure_traits()
