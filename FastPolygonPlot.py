''' Simple example to show the improvement of plotting a list of polygons.

1) We set a list of random polygons to plot.
2) The Class PlotPolyg is the original way to plot a list of polygons.
3) The Class FastPlotPolyg is the new way to plot a list of polygons by
separating them with numpy.nan and calling the plot only once.

The computational times to plot with both techniques is displayed and clearly
show the huge improvement. Of course, this is only valid (for now) for a list
of polygons that have the same properties, that is colors and line width.
'''

#-------------------------------------------------------------------------------
# Force Qt4 since issue with wx when clicking the window close button
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
#-------------------------------------------------------------------------------
import sys
import time
import random
import numpy as np
from enable.api import ComponentEditor
from chaco.tools.api import HighlightTool
from chaco.api import Plot, ArrayPlotData, MultiArrayDataSource
from traits.api import HasTraits, Instance
from traitsui.api import View, UItem


#-------------------------------------------------------------------------------
# Define a global list of polygon to plot so that it's the same for both method
x_ = []
y_ = []
polyg_nb = 1000

for i in range(polyg_nb):
    x1 = random.random()
    x2 = x1 + random.random()/5.0
    x3 = x1 + random.random()/5.0
    x_.append([x1,x2,x3])
    y1 = random.random()
    y2 = y1 + random.random()/5.0
    y3 = y1 + random.random()/5.0
    y_.append([y1,y2,y3])


#-------------------------------------------------------------------------------
class PlotPolyg(HasTraits):

    #---------------------------------------------------------------------------
    plot = Instance(Plot)
    plot_data = Instance(ArrayPlotData)
    polyg_nb = polyg_nb


    #---------------------------------------------------------------------------
    def _plot_data_default(self):
        """Filling the ArrayPlotData before plotting"""
        data = ArrayPlotData()
        for i in range(self.polyg_nb):
            data.set_data("polyg"+str(i)+"_x", x_[i])
            data.set_data("polyg"+str(i)+"_y", y_[i])
        return data


    #---------------------------------------------------------------------------
    def _plot_default(self):
        """The plot itself with a measure of compuational time"""
        t0 = time.time()

        p = Plot(self.plot_data)
        for m in range(self.polyg_nb):
            p.plot( ("polyg"+str(m)+"_x", "polyg"+str(m)+"_y"), type='polygon',
                    face_color='blue', edge_color='black',
                    )

        t1 = time.time()
        print 'Execution time for one-by-one plotting = %f sec' % (t1-t0)

        return p


    view = View(
                UItem('plot', editor=ComponentEditor(), resizable=True, width = .8, height = .8,),
                resizable=True, width=.6, height=.8,
                )


#-------------------------------------------------------------------------------
class FastPlotPolyg(HasTraits):

    #---------------------------------------------------------------------------
    plot = Instance(Plot)
    plot_data = Instance(ArrayPlotData)
    polyg_nb = polyg_nb


    #---------------------------------------------------------------------------
    def _plot_data_default(self):
        """Filling the ArrayPlotData before plotting"""
        data = ArrayPlotData()

        xx_, yy_ = [], []
        for i in range(self.polyg_nb):
            xx_ += x_[i] + [np.nan]
            yy_ += y_[i] + [np.nan]

        data.set_data("polyg_x", xx_)
        data.set_data("polyg_y", yy_)
        return data


    #---------------------------------------------------------------------------
    def _plot_default(self):
        """The plot itself with a measure of compuational time"""
        t0 = time.time()

        p = Plot(self.plot_data)
        p.plot( ("polyg_x", "polyg_y"), type='polygon',
                face_color='blue', edge_color="black",
                )

        t1 = time.time()
        print 'Execution time for fast plotting = %f sec' % (t1-t0)

        return p


    view = View(
                UItem('plot', editor=ComponentEditor(), resizable=True, width = .8, height = .8,),
                resizable=True, width=.6, height=.8,
                )



#-------------------------------------------------------------------------------
if __name__ == '__main__':

    tst = PlotPolyg()     # Create an instance of the original PolygonPlot
    fst = FastPlotPolyg() # Create an instance of the new fast PolygonPlot
    tst.edit_traits()
    fst.configure_traits()
