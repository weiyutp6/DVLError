# DVLError

## Prerequisites

```bash
pip install numpy
pip install pyyaml
pip install matplotlib
```

## Code workings

parameters could be changed in the param.yaml file, the details are as follows
input DVLError(start(m),end(m),bias(m/s),random(m/s),time interval(s/frame),total time passed(s))
runs three times for x,y,z separately
start at point [startx, starty, startz]
end at point [endx, endy, endz]
velocity has bias [biasx,biasy,biasz] (static errors like misalignment)
velocity(vx,vy,vz) has Gaussian white noise with distribution N(0,random)(dynamic error that can be modeled as Gaussian)
velocity has fixed transient error with distribution N(0,0.0001) (that son of a bitch you can never get rid of)
there are a total of total time passed/interval number of datapoints with a rate of 1/interval frames per second
average velocity is (end-start)/total time passed
```bash
chmod +x main.py
./main.py
```
