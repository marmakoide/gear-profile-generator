# gear-profile-generator

This script generates spur gear profiles (or outlines). It gives a correct output
even for low numbers of teeth. 

The gears generated with this script have been 3d printed and worked fine. 
However, I am no mechanical engineer, I'm a guy who code late in the evening
while having a beer. If you use this script to design a suborbital passenger 
rocket, and that rocket blows up due to a faulty gear design, I take no 
responsability.

The implementation is based on a method explained on the excellent Michal 
Zalewski's [Guerrila Guide of CNC Machining](http://lcamtuf.coredump.cx/gcnc),
[chapter 6](http://lcamtuf.coredump.cx/gcnc/ch6).

## Getting Started

### Prerequisites

You will need

* Python 2.7 or above
* [Numpy](http://www.numpy.org)
* [Shapely](https://github.com/Toblerity/Shapely)


### Usage

The script generates a file from the gear parameters specified from the command-line

```
python gear.py --teeth-count=17 --tooth-width=0.25 --pressure-angle=20 --backlash=0.1 -tdxf -oout.dxf
```

This command will generate a spur gear with 

* 17 teeth
* a pressure angle of 20 degrees
* a backlash of 0.1

and it will be saved as a DXF file named *out.dxf*.

If you generate an inner gear, to design a planetary gearbox for instance, use
a negative backlash. The text output is just the raw coordinates of the multiline
defining the gear's shape.

## Authors

* **Alexandre Devert** - *Initial work* - [marmakoide](https://github.com/marmakoide)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

