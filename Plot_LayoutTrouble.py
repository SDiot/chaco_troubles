""" Simple example to show a problem with the Layout

    HOW TO:
        1) Run Plot_LayoutTrouple.py
        2) Zoom by creating a rectangular box with the left click so that the aspect_ratio is changed
        3) Click on Reset Asp. Ratio
        4) Click on Reset View ===> the plot is not taking all the room it could!
        5) Resize the window ===> the plot is now taking all the room it can!

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
    reset_view = Button(label='Reset View')
    reset_asp_ratio= Button(label='Reset Asp. Ratio')

    view = View(
                VGroup(
                    UItem('plot', editor=ComponentEditor(), resizable=True, width = .8, height = .8,),
                    HGroup(
                        Item("reset_asp_ratio", label="Reset Asp. Ratio", show_label=False),
                        Item("reset_view", label="Reset View", show_label=False),
                        ),
                    ),
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
        zoom = ZoomTool(self.plot, tool_mode="box",always_on=True,)
        self.plot.overlays.append(zoom)
        return self.plot

    #---------------------------------------------------------------------------
    def _reset_asp_ratio_fired(self):
        x_lo = self.plot.x_axis.mapper.range.low
        x_hi = self.plot.x_axis.mapper.range.high
        y_lo = self.plot.y_axis.mapper.range.low
        y_hi = self.plot.y_axis.mapper.range.high
        self.plot.aspect_ratio = (x_hi-x_lo)/(y_hi-y_lo)
        self.plot.invalidate_and_redraw()

    #---------------------------------------------------------------------------
    def _reset_view_fired(self):
        self.plot.x_axis.mapper.range.set(low=0, high=2)
        self.plot.y_axis.mapper.range.set(low=0, high=2)
        self.plot.aspect_ratio = 1.0
        self.plot.invalidate_and_redraw()


#-------------------------------------------------------------------------------
if __name__ == '__main__':
    tst = TestPlot()
    tst.configure_traits()
