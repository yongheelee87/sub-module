# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
o3 = session.openOdb(name='C:\git\PycharmProjects\ABAQUS_API_time\inp\Job-Au_113mJ_tset.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.mdbData.summary()
odb = session.odbs['C:\git\PycharmProjects\ABAQUS_API_time\inp\Job-Au_113mJ_tset.odb']
xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=((
        'S', INTEGRATION_POINT, ((COMPONENT, 'S22'), )), ), nodeSets=(
        'SET-1-LOADING-PT', ))
xyp = session.XYPlot('XYPlot-1')
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
curveList = session.curveSet(xyData=xyList)
chart.setValues(curvesToPlot=curveList)
session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
xyp = session.xyPlots['XYPlot-1']
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
print('chartName: ', chartName)
print('chart: ', chart)
x0 = chart.curves['_S:S22 (Avg: 75%) SP:1 PI: PART-TOTAL-1 N: 5']
session.writeXYReport(fileName='C:\git\PycharmProjects\ABAQUS_API_time\inp\Result\Job-Au_113mJ_tset_loading_pt.csv', appendMode=OFF, xyData=(x0, ))
odb = session.odbs['C:\git\PycharmProjects\ABAQUS_API_time\inp\Job-Au_113mJ_tset.odb']
xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S22'), )), ), nodeSets=('SET-PT1', ))
xyp = session.xyPlots['XYPlot-1']
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
curveList = session.curveSet(xyData=xyList)
chart.setValues(curvesToPlot=curveList)
xyp = session.xyPlots['XYPlot-1']
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
x0 = chart.curves['_S:S22 (Avg: 75%) SP:1 PI: PART-TOTAL-1 N: 2']
session.writeXYReport(fileName='C:\git\PycharmProjects\ABAQUS_API_time\inp\Result\Job-Au_113mJ_tset_pt1.csv', xyData=(x0, ))
odb = session.odbs['C:\git\PycharmProjects\ABAQUS_API_time\inp\Job-Au_113mJ_tset.odb']
xy1 = xyPlot.XYDataFromHistory(odb=odb, outputVariableName='Kinetic energy: ALLKE in ELSET SET-3-AL', steps=('Step-1', ), )
c1 = session.Curve(xyData=xy1)
xyp = session.xyPlots['XYPlot-1']
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
chart.setValues(curvesToPlot=(c1, ), )
xyp = session.xyPlots['XYPlot-1']
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
x0 = chart.curves['_temp_1']
session.writeXYReport(fileName='C:\git\PycharmProjects\ABAQUS_API_time\inp\Result\Job-Au_113mJ_tset_K.csv',xyData=(x0, ))
