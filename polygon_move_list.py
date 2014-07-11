""" Based on <<Polygon plot with drag-move>>.

Used as a simple example to show that the modifications made to polygon_plot.py
in order to allow a list of polygon to be plotted at once also allows each list
to be consider as one "list of polygon" when using hittest.

TEST: Drag the "list of polygons" using left click
"""
#-------------------------------------------------------------------------------
# Force Qt4 since issue
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

# Major library imports
from numpy import transpose, nan

# Enthought library imports
from enable.api import Component, ComponentEditor
from traits.api import HasTraits, Instance, Enum, CArray
from traitsui.api import Item, Group, View

# Chaco imports
from chaco.api import ArrayPlotData, Plot
from chaco.base import n_gon
from chaco.tools.api import DragTool

class DataspaceMoveTool(DragTool):
    """
    Modifies the data values of a plot.  Only works on instances
    of BaseXYPlot or its subclasses
    """

    event_state = Enum("normal", "dragging")
    _prev_pt = CArray

    def is_draggable(self, x, y):
        return self.component.hittest((x,y))

    def drag_start(self, event):
        data_pt = self.component.map_data((event.x, event.y), all_values=True)
        self._prev_pt = data_pt
        event.handled = True

    def dragging(self, event):
        plot = self.component
        cur_pt = plot.map_data((event.x, event.y), all_values=True)
        dx = cur_pt[0] - self._prev_pt[0]
        dy = cur_pt[1] - self._prev_pt[1]
        index = plot.index.get_data() + dx
        value = plot.value.get_data() + dy
        plot.index.set_data(index, sort_order=plot.index.sort_order)
        plot.value.set_data(value, sort_order=plot.value.sort_order)
        self._prev_pt = cur_pt
        event.handled = True
        plot.request_redraw()


#===============================================================================
# # Create the Chaco plot.
#===============================================================================
def _create_plot_component():

    # Use n_gon to compute center locations of the "global" polygons
    points = n_gon(center=(0,0), r=8, nsides=4)

    # Choose some colors for our polygons
    colors = {0:0xaabbcc,   1:'orange', 2:'yellow', 3:'lightgreen'}

    # Create a PlotData object to store the polygon data
    pd = ArrayPlotData()

    # Create a Polygon Plot to draw the regular polygons
    polyplot = Plot(pd)

    # Store path data for each polygon, and plot
    for n, ctr in enumerate(points):

        nsides = 3
        nodes_x = []
        nodes_y = []

        # Use n_gon again to compute center locations of the "local" polygons
        polyg_pnts = n_gon(center=ctr, r=3, nsides=4)

        for p in polyg_pnts:
            npoints = n_gon(center=p, r=2, nsides=nsides)
            nxarray, nyarray = transpose(npoints)
            nodes_x = nodes_x + list(nxarray) + [nan] # Updates list of polygons
            nodes_y = nodes_y + list(nyarray) + [nan] # Updates list of polygons
            nsides = nsides + 1
        pd.set_data("x"+str(n), nodes_x) # The list of 6 local polygons
        pd.set_data("y"+str(n), nodes_y) # The list of 6 local polygons

        plot = polyplot.plot(("x"+str(n), "y"+str(n)), type="polygon",
                             face_color=colors[n], hittest_type="poly")[0]

        plot.tools.append(DataspaceMoveTool(plot, drag_button="left"))

    # Tweak some of the plot properties
    polyplot.padding = 50
    polyplot.title = "Polygon Plot"
    polyplot.x_axis.mapper.range.set(low=-20, high=20)
    polyplot.y_axis.mapper.range.set(low=-20, high=20)

    return polyplot

#===============================================================================
# Attributes to use for the plot view.
size=(800,800)
title="Polygon Plot"

#===============================================================================
# # Demo class that is used by the demo.py application.
#===============================================================================
class Demo(HasTraits):
    plot = Instance(Component)

    def _plot_default(self):
         return _create_plot_component()

    traits_view = View(
                    Group(
                        Item('plot', editor=ComponentEditor(size=size),
                             show_label=False),
                        orientation = "vertical"),
                    resizable=True, title=title
                    )

demo = Demo()

if __name__ == "__main__":
    demo.configure_traits()

#--EOF---
