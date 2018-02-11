import itertools



def write(out, geom):
	# Generate the header
	out.write(' 999\n')
	out.write('DXF created from gear.py (https://github.com/marmakoide/gear-profile-generator)\n')
	out.write(' 0\n')
	out.write('SECTION\n')
	out.write(' 2\n')
	out.write('HEADER\n')
	out.write(' 9\n')
	out.write('$ACADVER\n')
	out.write(' 1\n')
	out.write('AC1009\n')
	out.write(' 0\n')
	out.write('ENDSEC\n')

	out.write(' 0\n')
	out.write('SECTION\n')
	out.write(' 2\n')
	out.write('TABLES\n')
	out.write(' 0\n')
	out.write('TABLE\n')
	out.write(' 2\n')
	out.write('LAYER\n')
	out.write(' 0\n')
	out.write('LAYER\n')
	out.write('2\n')
	out.write('1\n')
	out.write('0\n')
	out.write('ENDTAB\n')
	out.write(' 0\n')
	out.write('ENDSEC\n')
	out.write(' 0\n')
	out.write('SECTION\n')
	out.write(' 2\n')
	out.write('BLOCKS\n')
	out.write(' 0\n')
	out.write('ENDSEC\n')

	# For each ring
	out.write(' 0\n')
	out.write('SECTION\n')
	out.write(' 2\n')
	out.write('ENTITIES\n')

	for ring in itertools.chain.from_iterable([[geom.exterior], geom.interiors]):
		for vertex_pair in zip(ring.coords[:-1], ring.coords[1:]):
			out.write(' 0\n')
			out.write('LINE\n')
			out.write(' 8\n')
			out.write('1\n')
			out.write(' 62\n')
			out.write('1\n')
			for i, (x, y) in enumerate(vertex_pair):
				out.write(' %d\n' % (10 + i))
				out.write('%f\n' % x)
				out.write(' %d\n' % (20 + i))
				out.write('%f\n' % y)

	out.write(' 0\n')
	out.write('ENDSEC\n')

	# Generate the footer
	out.write(' 0\n')
	out.write('EOF\n')	
