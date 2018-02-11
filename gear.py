import sys
import numpy
import argparse
import itertools

import backends.dxf
import backends.text

from shapely.ops import cascaded_union
from shapely.geometry import Point, MultiPoint, Polygon, box
from shapely.affinity import rotate, scale, translate



def rot_matrix(x):
	c, s = numpy.cos(x), numpy.sin(x)
	return numpy.array([[c, -s], [s, c]])



def rotation(X, angle, center = None):
	if center is None:
		return numpy.dot(X, rot_matrix(angle))
	else:
		return numpy.dot(X - center, rot_matrix(angle)) + center



def deg2rad(x):
	return (numpy.pi / 180) * x



def generate(teeth_count = 8,
             tooth_width = 1.,
             pressure_angle = deg2rad(20.),
             backlash = 0.,
             frame_count = 16):
	tooth_width -= backlash
	pitch_circumference = tooth_width * 2 * teeth_count
	pitch_radius = pitch_circumference / (2 * numpy.pi)
	addendum = tooth_width * (2 / numpy.pi)
	dedendum = addendum
	outer_radius = pitch_radius + addendum
	print pitch_radius - dedendum
	# Tooth profile
	profile = numpy.array([
  	[-(.5 * tooth_width + addendum * numpy.tan(pressure_angle)),  addendum],
  	[-(.5 * tooth_width - dedendum * numpy.tan(pressure_angle)), -dedendum],
  	[ (.5 * tooth_width - dedendum * numpy.tan(pressure_angle)), -dedendum],
  	[ (.5 * tooth_width + addendum * numpy.tan(pressure_angle)) , addendum]
	])

	outer_circle = Point(0., 0.).buffer(outer_radius)

	poly_list = []
	prev_X = None
	l = 2 * tooth_width / pitch_radius
	for theta in numpy.linspace(0, l, frame_count):
		X = rotation(profile + numpy.array((-theta * pitch_radius, pitch_radius)), theta)
		if prev_X is not None:
			poly_list.append(MultiPoint([x for x in X] + [x for x in prev_X]).convex_hull)
		prev_X = X	

	def circle_sector(angle, r):
		box_a = rotate(box(0., -2 * r, 2 * r, 2 * r), -angle / 2, Point(0., 0.))
		box_b = rotate(box(-2 * r, -2 * r, 0, 2 * r),  angle / 2, Point(0., 0.))
		return Point(0., 0.).buffer(r).difference(box_a.union(box_b))

	# Generate a tooth profile
	tooth_poly = cascaded_union(poly_list)
	tooth_poly = tooth_poly.union(scale(tooth_poly, -1, 1, 1, Point(0., 0.)))

	# Generate the full gear
	gear_poly = Point(0., 0.).buffer(outer_radius)
	for i in range(0, teeth_count):
		gear_poly = rotate(gear_poly.difference(tooth_poly), (2 * numpy.pi) / teeth_count, Point(0., 0.), use_radians = True)
	
	# Job done
	return gear_poly, pitch_radius



def main():
	# Command line parsing
	parser = argparse.ArgumentParser(description = 'Generate 2d spur gears profiles')
	parser.add_argument('-c', '--teeth-count', type = int, default = 17, help = 'Teeth count')
	parser.add_argument('-w', '--tooth-width', type = float, default = 10., help = 'Tooth width')
	parser.add_argument('-p', '--pressure-angle', type = float, default = 20., help = 'Pressure angle in degrees')
	parser.add_argument('-n', '--frame-count', type = int, default = 16, help = 'Number of frames used to build the involute')
	parser.add_argument('-b', '--backlash', type = float, default = 0.2, help = 'Backlash')
	parser.add_argument('-t', '--output-type', choices = ['dxf', 'text'], default = 'dxf', help = 'Output type')
	parser.add_argument('-o', '--output-path', default = 'out', help = 'Output file')
	args = parser.parse_args()

	# Input parameters safety checks
	if args.teeth_count <= 0:
		sys.stderr.write('Invalid teeth count\n')
		sys.exit(1)

	# Generate the shape
	poly, pitch_radius = generate(args.teeth_count,
	                              args.tooth_width,
	                              deg2rad(args.pressure_angle),
	                              args.backlash,
	                              args.frame_count)

	# Write the shape to the output
	print 'pitch radius =', pitch_radius

	with open(args.output_path, 'w') as f:
		if args.output_type == 'dxf':
			backends.dxf.write(f, poly)
		elif args.output_type == 'text':
			backends.text.write(f, poly)



if __name__ == '__main__':
	main()
