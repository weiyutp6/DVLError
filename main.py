import numpy as np
import yaml
import matplotlib.pyplot as plt

'''
input DVLError(start(m),end(m),bias(m/s),random(m/s),time interval(s/frame),total time passed(s))
runs three times for x,y,z separately
start at point [startx, starty, startz]
end at point [endx, endy, endz]
velocity has bias [biasx,biasy,biasz] (static errors like misalignment)
velocity(vx,vy,vz) has Gaussian white noise with distribution N(0,random)(dynamic error that can be modeled as Gaussian)
velocity has fixed transient error with distribution N(0,0.0001) (that son of a bitch you can never get rid of)
there are a total of total time passed/interval number of datapoints with a rate of 1/interval frames per second
average velocity is (end-start)/total time passed
'''


class DVLError:
    def __init__(self, point_start=0.0, point_end=10.0, error_bias=0.0, error_random=0.0, interval=0.1, total_time=1.0):
        self.__point_start = point_start
        self.__point_end = point_end
        self.__interval = interval
        self.__total_trajectory = point_end - point_start
        self.__data_points = int(total_time / interval)
        self.__error_bias = error_bias
        self.__error_random = np.random.normal(0, error_random, self.__data_points)
        self.__error_transient = np.random.normal(0, 0.0001, self.__data_points)
        self.__total_time = total_time
        self.__init_velocity = (point_end - point_start) / total_time
        self.__velocity_log = []
        self.__result_trajectory = [0]
        self.set_velocity_log()
        self.__error_percentage = 0
        self.calculate_final_pos()

    def set_velocity_log(self):
        for i in range(self.__data_points):
            self.__velocity_log.append(self.__init_velocity + self.__error_transient[i] + self.__error_random[i]
                                       + self.__error_bias)

    def calculate_final_pos(self):
        for i in range(len(self.__velocity_log) - 1):
            self.__result_trajectory.append(self.__result_trajectory[-1] + self.__velocity_log[i] * self.__interval)
        self.__error_percentage = (self.__result_trajectory[-1] / self.__total_trajectory - 1) * 100

    def get_final_pos(self):
        return self.__result_trajectory[-1]

    def get_result_trajectory(self):
        return self.__result_trajectory

    def __main__(self):
        print(self.__error_random)
        print(self.__velocity_log)
        print(self.__result_trajectory)
        print(self.__error_percentage, end="%")


with open('param.yaml', 'r') as file:
    param = yaml.safe_load(file)

total_e = 0
for i in range(10000):
    x = DVLError(param['x']['start'], param['x']['end'], param['x']['bias'], param['x']['random'], param['interval'],
                 param['total_time'])
    y = DVLError(param['y']['start'], param['y']['end'], param['y']['bias'], param['y']['random'], param['interval'],
                 param['total_time'])
    z = DVLError(param['z']['start'], param['z']['end'], param['z']['bias'], param['z']['random'], param['interval'],
                 param['total_time'])
    error = np.array([x.get_final_pos() - param['x']['end'], y.get_final_pos() - param['y']['end'], z.get_final_pos() -
                      param['z']['end']])
    error_percentage = np.linalg.norm(error) / np.linalg.norm(
        [param['x']['end'], param['y']['end'], param['z']['end']]) * 100
    print(error)
    print(error_percentage, end="%\n")
    total_e += error_percentage
print(total_e/10000)
fig = plt.figure()
ax = plt.axes(projection='3d')
zline = np.linspace(param['z']['start'], param['z']['end'], int(param['total_time'] / param['interval']))
yline = np.linspace(param['y']['start'], param['y']['end'], int(param['total_time'] / param['interval']))
xline = np.linspace(param['x']['start'], param['x']['end'], int(param['total_time'] / param['interval']))
ax.plot3D(xline, yline, zline, 'blue')
ax.plot3D(x.get_result_trajectory(), y.get_result_trajectory(), z.get_result_trajectory(), 'red')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
