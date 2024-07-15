openpixelcontrol
================

A simple stream protocol for controlling RGB lighting, particularly RGB LEDs.
See http://openpixelcontrol.org/ for a spec.

Using this implementation, you can write your own patterns and animations,
test them in a simulator, and run them on real RGB light arrays.  This
repository includes these programs:

* `dummy_client`: Sends OPC commands for the RGB values that you type in.

* `dummy_server`: Receives OPC commands from a client and prints them out.

* `gl_server` (Mac or Linux only): Receives OPC commands from a client and
  displays the LED pixels in an OpenGL simulator.  Takes a "layout file"
  that specifies the locations of the pixels in a JSON array; each item
  in the array should be a JSON object of the form {"point": [x, y, z]}
  where x, y, z are the coordinates of the pixel in space.  Click and drag
  to rotate the 3-D view; hold shift and drag up or down to zoom.

* `tcl_server`: Receives OPC commands from a client and uses them to
  control Total Control Lighting pixels (see http://coolneon.com/) that
  are connected to the SPI port on a Beaglebone.

* `python/opc.py`: A Python client library for connecting and sending pixels.

* `python/color_utils.py`: A Python library for manipulating colors.

* `python/raver_plaid.py`: An example client that sends rainbow patterns.

To build these programs, run "make" and then look in the bin/ directory.

---

# Ghost Tree Deployment on BB
config.py
```python
AUDIO_PC_IP = '10.0.0.34'
AUDIO_PC_PORT = 6011

trunk = [0, 100]
branches = {
        "branchA": [101, 150],
        "branchB": [151, 200],
        "branchC": [201, 250],
        "branchD": [251, 300],
        "branchE": [301, 350],
}

# map amplitude to float brightness
PD_AMPLITUDE_LOW = 80
PD_AMPLITUDE_HIGH = 100
FLOAT_LOW = 0.2
FLOAT_HIGH = 1.0
```


`AUDIO_PC_IP` / `AUDIO_PC_PORT` ip and port for pd data

`trunk`/ `branches` start and end LED index for each part of the tree

assuming `amplitude xx` messages from pd:

maps `xx` value between `PD_AMPLITUDE_LOW` and `PD_AMPLITUDE_HIGH`
to between `FLOAT_LOW` and `FLOAT_HIGH` to be used to change the brightness of each pixel.

Pattern looks like a rainbow starting at the bottom of the trunk and propagating up the tree with the brightness of the leds mapped to the amplitude also propagating up the tree