# Dab and T-Pose Controlled Lights

Control your lights by dabbing and t-pose'ing, duh

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

## Exploring OpenPose Data for Training a New Classifier

We'll use some saved examples of T-Poses and Dabs in order to train our classifier. You can see the Jupyter notebook [here](https://github.com/burningion/dab-and-tpose-controlled-lights/blob/master/Data%20Play.ipynb) with examples of labeling and converting our raw `npy` Numpy exports to CSVs and Pandas datasets.
