def write(out, geom):
	ring_list = [geom.exterior] + list(geom.interiors)
	for ring in ring_list:
		for x, y in ring.coords:
			out.write('%f %f\n' % (x, y))

