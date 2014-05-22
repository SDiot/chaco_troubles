""" Simple example to show that I have a problem with padding

    HOW TO:
        1) Run Plot_PaddingTrouple.py
        2) Click on Replot ===> the padding is not taken into account while it
                                is enforced in plot_please... Why??

    FIX: Use an OverlayPlotContainer to contain the plot!
"""

#-------------------------------------------------------------------------------
# Force Qt4 since issue with wx when clicking the window close button
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
#-------------------------------------------------------------------------------
from enable.api import ComponentEditor
from chaco.api import Plot, ArrayPlotData
from chaco.tools.api import ZoomTool, PanTool
from traits.api import HasTraits, Instance, Button, Bool
from traitsui.api import View, UItem, Item, HGroup, VGroup

#-------------------------------------------------------------------------------
class TestPlot(HasTraits):

    plot = Instance(Plot)
    plotdata = Instance(ArrayPlotData)

    # Button to reset the view to the nice original plot
    replot = Button(label='Replot')

    view = View(
                VGroup(
                    UItem('plot', editor=ComponentEditor(), resizable=True, width = .8, height = .8,),
                    HGroup(
                        Item("replot", label="Reset View", show_label=False),
                        ),
                    ),
                resizable=True, width=.6, height=.8,
                )

    #---------------------------------------------------------------------------
    def plot_please(self,data):
        self.plot = Plot(data)
        self.plot.plot( ("x1", "y1"), type='polygon', face_color='auto' )
        self.plot.plot( ("x2", "y2"), type='polygon', face_color='auto'  )
        self.plot.plot( ("x3", "y3"), type='polygon', face_color='auto'  )
        self.plot.plot( ("x4", "y4"), type='polygon', face_color='auto'  )
        self.plot.aspect_ratio =  1.0

        # Add Pan & ZoomTool
        self.plot.tools.append( PanTool(self.plot, speed=1.2) )
        zoom = ZoomTool(self.plot, tool_mode="box",always_on=False,
                        always_on_modifier='control', zoom_factor=1.08,)
        self.plot.overlays.append(zoom)
        self.plot.padding = 200
        return self.plot


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
        self.plot_please(self.plotdata)
        return self.plot

    #---------------------------------------------------------------------------
    def _replot_fired(self):
        self.plot_please(self.plotdata)


#-------------------------------------------------------------------------------
if __name__ == '__main__':
    tst = TestPlot()
    tst.configure_traits()
