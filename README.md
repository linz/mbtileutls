# MBTiles Tools

## patch_mbtiles.py

Python tool that allows you to add (patch) tile data from one MBTiles database into another destination MBTiles database. Tiles will be overwritten in the destination MBTiles database.

###Usage

```
python patch_mbtile.py [options] source_mbtile destination_mbtile

Options:

  -h, --help            show this help message and exit
  -n NAME, --name=NAME  Set mbtiles internal name 

source_mbtile           MBTile you want to patch onto a destination MBTile 
destination_mbtile      MBTile that will have data added to

```

## Requirements

* Python `>= 2.6`

## License

BSD - see LICENSE
