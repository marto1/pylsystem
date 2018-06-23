draw_polygons.py
================

Generate all possible bounded polygons for a fixed number of lines
with equal lenght that have only 90 degree angles.

First all possible shapes with fixed number of lines and 90 degree
angles are generated. Then we filter useless polygons by mapping the
drawing on coordinates and checking if end line lands on (0,0) and
trace point history and eliminate on repetition except for (0,0).


Example for 12 lines, 140 shapes generated:

[![polygon video](https://raw.githubusercontent.com/marto1/pylsystem/master/polygon_place.jpg)](https://gfycat.com/ScalyFrankBasil)
