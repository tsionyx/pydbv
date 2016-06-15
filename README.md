# About
The handy tool to produce ER-diagrams for databases expressed in [dot language](http://www.graphviz.org/doc/info/lang.html)


# Installation
To install all the tools needed to see the diagram (alongside with the Graphviz), use the following commands depending on your distro:
``` bash
$ sudo apt-get install python-dev virtualenvwrapper pkg-config graphviz-dev
$ sudo yum install python-devel python-virtualenvwrapper pkgconfig graphviz-devel

$ ./setup.py install
```


# Usage
#### get the dot file
``` bash
$ python pydbv/model.py sqlite:///the/path/to/your/sqlite.db3 > sample.gv
```

#### get the diagram (in SVG format)
``` bash
$ python pydbv/model.py sqlite:///the/path/to/your/sqlite.db3 | dot -Kdot -Tsvg > sample.svg
```

#### ... or get both
``` bash
$ python pydbv/model.py sqlite:///the/path/to/your/sqlite.db3 | tee sample.gv | dot -Kdot -Tsvg > sample.svg
```

#### for the databases other than SQLite, use the [SQLAlchemy](http://www.sqlalchemy.org/) [connection URLs](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)


# Tests
before you run the test, do
``` bash
$ sudo apt-get install sqlite3 graphviz
$ sudo yum install sqlite graphviz
```

and then the test itself
``` bash
$ bash test/create-svg.sh
```