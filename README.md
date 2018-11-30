realestate
==========

realestate.com.au command line interface

NB this no longer works, I rewrote it in golang which can be found here: https://gist.github.com/grasevski/b5528ec1929423326e5cdc59dde6e183


INSTALL
-------

----
    $ sudo apt-get install python-scrapy        # Install scrapy if necessary
    $ git clone https://github.com/grasevski/realestate.git     # Download this repository
----


USAGE
-----

----
    $ ./realestate.py -h        # Display usage information
    $ ./realestate.py buy tempe |head   # List all properties for sale in Tempe and its surrounding suburbs in CSV format
    $ ./realestate.py sold 'Oatley, NSW'        # List all properties sold in Oatley and its surrounding suburbs in CSV format
    $ ./realestate.py rent redfern >redfern.csv # List all properties for rent in Redfern and its surrounding suburbs in CSV format
----
