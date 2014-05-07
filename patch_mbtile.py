#!/usr/bin/python
################################################################################
#
# Copyright 2013 Crown copyright (c)
# Land Information New Zealand and the New Zealand Government.
# All rights reserved
#
# This program is released under the terms of the new BSD license. See the 
# LICENSE file for more information.
#
################################################################################

import sys
import os.path
import sqlite3

from optparse import OptionParser

usage = "usage: %prog [options] source_mbtile destination_mbtile"

parser = OptionParser(usage=usage)

parser.add_option(
    "-n",
    "--name",
    type="string",
    dest="name",
    help="Set mbtiles name"
)
    
(cmd_opt, args) = parser.parse_args()

source_mbtile      = args[0]
destination_mbtile = args[1]

if not os.path.isfile(source_mbtile):
    print "Source file: " + source_mbtile + " does not exist"
    exit(1)

if not os.path.isfile(destination_mbtile):
    print "destination file: " + destination_mbtile + " does not exist"
    exit(1)

conn = sqlite3.connect(destination_mbtile)
c = conn.cursor()
c.execute("PRAGMA journal_mode=PERSIST")
c.execute("PRAGMA page_size=80000")
c.execute("PRAGMA synchronous=OFF")
c.execute("ATTACH DATABASE '" + source_mbtile + "' AS source")

# get bounds (left, bottom, right, top) for source database
c.execute("SELECT value FROM source.metadata WHERE name='bounds'")
row = c.fetchone()
src_bounds = row[0].split(',')

# get bounds (minx, miny, maxx, maxy) for destination database
c.execute("SELECT value FROM main.metadata WHERE name='bounds'")
row = c.fetchone()
dst_bounds = row[0].split(',')

dst_xmin = float(dst_bounds[0])
dst_ymin = float(dst_bounds[1])
dst_xmax = float(dst_bounds[2])
dst_ymax = float(dst_bounds[3])

src_xmin = float(src_bounds[0])
src_ymin = float(src_bounds[1])
src_xmax = float(src_bounds[2])
src_ymax = float(src_bounds[3])

if src_xmin < dst_xmin:
    dst_xmin = src_xmin
if src_xmax > dst_xmax:
    dst_xmax = src_xmax

if src_ymin < dst_ymin:
    dst_ymin = src_ymin
if src_ymax > dst_ymax:
    dst_ymax = src_ymax

bounds = "{0},{1},{2},{3}".format(dst_xmin,dst_ymin,dst_xmax,dst_ymax)

c.execute("REPLACE INTO map SELECT * FROM source.map")
c.execute("REPLACE INTO images SELECT * FROM source.images")
c.execute("UPDATE main.metadata SET value = min((SELECT value FROM source.metadata WHERE name='minzoom'), value) WHERE name='minzoom'")
c.execute("UPDATE main.metadata SET value = max((SELECT value FROM source.metadata WHERE name='maxzoom'), value) WHERE name='maxzoom'")
c.execute("UPDATE main.metadata SET value = ? WHERE name='bounds'", (bounds,))

if cmd_opt.name:
    c.execute("UPDATE main.metadata SET value = ? WHERE name='name'", (cmd_opt.name,))

conn.commit()

exit(0)

