# macropad
This app is built specifically the [Adafruit MacroPad RP2040](https://www.adafruit.com/product/5128). It let's you configure custom macros and LED settings for your macropad with, hopefully, minimal effort.

## hardware & pre-installation setup
Before you can install this app, you need to assemble and setup your macropad. Just follow the [Primary Guide: Adafruit MacroPad RP2040](https://www.adafruit.com/product/5128).

The only necessary sections are:
1. [Macropad Assembly](https://learn.adafruit.com/adafruit-macropad-rp2040/macropad-assembly)
2. [CircuitPython](https://learn.adafruit.com/adafruit-macropad-rp2040/circuitpython)

After that, you should see `CIRCUITPY` in your list of drives/devices. Make sure that is the case before continuing.

## installation
Make sure your macropad is plugged in and then execute the following command to install.

`./install`

If there are no errors, you can continue configuring and using your macropad.

## configuration
Once you have the app installed, you can configure the `config.json` in your macropad. If you've setup your macropad correctly, there should be a device connected to your machine called `CIRCUITPY`. You'll find the config file there. Open it up in your favorite text editor. It should look like this:

```
{
    "display": {
        "title": "",
        "title_scale": 1
    },
    "leds": {
        "brightness": 0.6,
        "starting animation": "default",
        "animations": {
            "default": {
                "type": "solid",
                "color": "teal"
            }
        }
    },
    "macros": {
        "0": {
            "key": "MUTE",
            "message": "f{volume_mute}"
        },
        "1": {
            "key": "PLAY_PAUSE",
            "message": "f{play} f{pause}"
        }
    }
}
```

You can change the values to your liking. When you save, your macropad should restart and load your new settings.

### settings
Settings must be defined with JSON formatting. You can use [this cheatsheet](https://quickref.me/json) as a reference if you're unfamiliar.

All settings are also optional.

**orientation:** Set the orientation of how you want to use your macropad. Do you want it display up? Sideways 90 degrees? Accepted values are `0`, `90`, `180`, and `270`. By default, it's `0` - display up.

**display:** Set what you want to always show on your screen/display.
* **title:** Sets the text that will always show at the top of macropad's screen/display. Can be left empty.
* **title_scale:** Sets how large, in scale, the title text will be. `1` is the default size.

**leds:** Define what you want to show with your key LEDs.
* **brightness:** Sets the brightness of the LEDs, between `0` and `1`.
* **starting animation:** Sets an animation you have defined to always be used when the macropad starts up.
* **animations:** Define custom LED animations you want to use. More info [here](TODO).

**macros:** Define your macros. Each macro starts with the key number on the macropad, followed by the action you want to execute in braces. The key number is based off your **orientation** and numbered left to right, top to bottom, starting with `0`. In addition, `+` can be specified for a clockwise rotation of the nob (rotary encoder) and `-` for counter/anti-clockwise.
* **key:** The primary key you want your macro to send to your computer. Here's a [list of recognized keys](TODO).
* **mods:** Specify a list of any modifiers to send. These can be `CONTROL`, `SHIFT`, or `ALT`.


## HAVE FUN!