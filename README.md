# Dab and T-Pose Controlled Lights

Control your lights by dabbing and t-pose'ing, duh

[![Dab and T-Pose Controlled Lights](https://github.com/burningion/dab-and-tpose-controlled-lights/raw/master/images/dab-tpose.gif)](https://www.makeartwithpython.com/blog/dab-and-tpose-controlled-lights/)

Check out the full blog post [here](https://www.makeartwithpython.com/blog/dab-and-tpose-controlled-lights/).

## Getting the ZWave Controller working on the TX2

By default, I couldn't write to the `/dev/ttyACM0` device that the ZWave USB controller came up on with my NVDIA Tegra TX2.

You'll need to do something along the following to get permissions:

```bash
$ sudoedit /etc/udev/rules.d/50-myusb.rules
```

Followed by inserting the following lines to add perms to the `/dev/ttyUSB*` and `/dev/ttyACM*`:

```
KERNEL=="ttyUSB[0-9]*",MODE="0666"
KERNEL=="ttyACM[0-9]*",MODE="0666"
```

## Getting an OpenPose Model running on the TX2

There are two ways, I started out by using the original [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) repo to get a build and proof of concept running.

I got ~~probably half a frame~~ 1.4(ish) frames per second out of that. You can see how I initialize and use the built in devboard camera in the `01_body_from_image.py` file in this repo. That comes directly out of the included Python examples.

Because I wanted better response time, I ended up searching for a better model. I found [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation).

It requires Tensorflow, so be sure to grab the latest Jetpack release from NVIDIA [here](https://developer.nvidia.com/embedded/downloads#?search=tensorflow) when installing.

After that, it should run with the included `run_webcam.py`, just be sure to run it with the right model. Mobilenet_v2_large was the bare minimum for an acceptable detection for me:

```bash
$ python3 run_webcam.py --model=mobilenet_v2_large --resize=432x368
```

With this model, I get 4(ish) frames per second on the TX2, much better for detection latency. I may try seeing if I can optimize further after getting a full proof of concept running.

## Exploring OpenPose Data and Training a New Classifier

We'll use some saved examples of T-Poses and Dabs in order to train our classifier. You can see the Jupyter notebook [here](https://github.com/burningion/dab-and-tpose-controlled-lights/blob/master/Data%20Play.ipynb) with examples of labeling and converting our raw `npy` Numpy exports to CSVs and Pandas datasets, along with cleanup and training.

The current (working) architecture looks like this:

![Dab and T-Pose Neural Network Architecture](https://github.com/burningion/dab-and-tpose-controlled-lights/raw/master/images/neural1.png)

## Running the Project Itself

![Dab and T-Pose Architecture](https://github.com/burningion/dab-and-tpose-controlled-lights/raw/master/images/dab-tpose.png)

You'll need to get OpenPose up and running, along with the Python libraries for OpenCV and ZWave. After that, you can use the included program, just run it under the `openpose/examples/tutorial_api_python` directory.

If you want to grab more example poses for retraining, just replace the `01_body_from_image.py` with the one included in this repo's `src/` directory.


## Known bugs

For some reason, the model test I run on my original `X` and `y` dataset doesn't seem to work. I think I messed the data up somewhere along the way in the Jupyter Notebook. If you figure out where that happens, open a PR please. :)
