import sys
from PyQt5 import QtWidgets
from GUI import Ui_MainWindow
import matplotlib.animation as animation
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.ui.simulate_ch1.clicked.connect(self.simulate)
        self.ui.export_ch1.clicked.connect(lambda: self.export(self.ui.export_ch1))
        self.ui.export_ch2.clicked.connect(lambda: self.export(self.ui.export_ch2))

        # simulation of the flow rate of the cough over time
        ########################################################
        V = 4.68 #volume in l
        M = 0.27 #mean
        G = 3.00 #std
        diamemter= 0.01905 # meter
        area=(diamemter**2)*(np.pi/4)
        self.t = np.arange(1, 50)

        ########################################################

        flow_rate = []  #m^3/s
        self.velocity = []  #m/s

        # calculate flow rate in m^3/s and velocity in m/s
        for i in range(0, len(self.t)):

            F = ((4.68) * (1 / math.sqrt(2 * np.pi) * self.t[i] * math.log(3)) * math.exp(
                (-0.5) * (math.log(self.t[i]) - math.log(0.27) / math.log(3)) ** 2))*(0.001)
            flow_rate.append(F)
            self.velocity.append(F/area)

        # self.ui.ch1.canvas.axes.set_title('flow rate of cough')
        # self.ui.ch1.canvas.axes.plot(t,flow_rate,'r')
        #
        # self.ui.ch2.canvas.axes.set_title('Cough Propagation in Sagittal Plane')
        # self.ui.ch2.canvas.axes.plot(t,velocity)


        #######################################################################
        # animation

        # def update_line(num, data, line):
        #     line.set_data(data[..., :num])
        #     return line,

        # fig=plt.figure()
        #
        #
        # data = np.vstack((t,velocity))
        # l, = plt.plot([], [])
        #
        #
        # plt.xlim(0, 50)
        # plt.ylim(-0.5, 3)

        # self.line_ani = animation.FuncAnimation(fig, update_line, frames=100,
        #                                    fargs=(data, l), interval=20, blit=False)

        # plt.show()

        ######################################################################

    def simulate(self):
        self.canvas = FigureCanvasQTAgg(Figure(figsize = (5,5), dpi = 100))
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        fig=self.ui.ch1.canvas
        # self.canvas.show()
        data = np.vstack((self.t, self.velocity))
        l, = plt.plot([], [])

        self.line_ani = animation.FuncAnimation(fig,self.update_line, frames=100,
                                                fargs=(data, l), interval=20, blit=False)

    def update_line(self,num, data, line):
        line.set_data(data[..., :num])
        return line,










    def export(self,simulation):   # in futere it will take the button exporte aas an argumnet
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
        if simulation == self.ui.export_ch1:
          #self.line_ani.save('simulation of cough propagation in sagittal plane.mp4', writer=writer)
          print(1)
        else:
          #self.line_ani.save('simulation of cough propagation in coronal plane.mp4', writer=writer)
          print(2)

    def prograss(self):
        self.completed = 0
        while self.completed < 100:
            self.completed += 0.0001
            self.ui.progressBar_ch1.setValue(self.completed)
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
