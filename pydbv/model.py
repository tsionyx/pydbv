#!/usr/bin/env python

import os
import sys

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.schema import MetaData
import pygraphviz as pgv
from jinja2 import Environment, Template, FileSystemLoader


# Capture our current directory
try:
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    THIS_DIR = os.getcwd()

def __row2dict(row):
    dictret = dict(row.__dict__)
    dictret.pop('_sa_instance_state', None)
    return dict((k, v) for k, v in dictret.items())

__COLLECTION_SUFFIX = "_collection"
def name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    s= "{0}{1}_from_{2}({3})".format(
            referred_cls.__name__,# .lower(),
            __COLLECTION_SUFFIX,
            constraint.table.name,
            ','.join(constraint.columns))
    print s
    return s

def multiplicity_indicator(prop):
    if prop.uselist:
        return ' *'
    if hasattr(prop, 'local_side'):
        cols = prop.local_side
    else:
        cols = prop.local_columns
    if any(col.nullable for col in cols):
        return ' 0..1'
    if show_multiplicity_one:
        return ' 1'
    return ''


def main(sqlalchemy_connection, show_type=False):
    engine = create_engine(sqlalchemy_connection)

    meta = MetaData()
    meta.reflect(bind=engine)
    env = Environment(
        loader=FileSystemLoader(THIS_DIR),
        trim_blocks=True,
        lstrip_blocks=True)
    node_template = env.get_template('node-template.html')
    G=pgv.AGraph(strict=False,
        directed=True,
        name=engine.url.database,
        graph_type='digraph',
        compound='true',
        rankdir='RL')
    tables = meta.tables.values()
    #tables = engine.table_names()
    for table in tables:
        if table.name.lower().startswith('sqlite_'):
            continue
        G.add_node(
            table.name,
            label=node_template.render(
                title=table.name,
                columns=table.columns.values(),
                show_type=show_type),
            shape='plaintext'
        )
    for table in tables:
        for fk in table.foreign_keys:
            if fk.column.table not in tables:
                # print fk.column.table
                continue

            uniq_child = fk.parent.primary_key or fk.parent.unique
            G.add_edge(
                table.name,
                fk.column.table.name,
                tailport="{0}:w".format(fk.parent.name),
                headport="{0}:e".format(fk.column.name + ('_type' if show_type else '')),
                #headlabel="+ %s"%fk.column.name, taillabel='+ %s'%fk.parent.name,
                # arrowhead='odottee' if fk.parent.nullable else 'teetee', dir='both',
                arrowhead='none', dir='back',
                arrowtail='teeodot' if uniq_child else 'crowodot'
                #samehead=fk.column.name, sametail=fk.parent.name,
            )
        '''
        for column_name, column in table.columns.items():
            fks = ', '.join(
                '{0}.{1}'.format(fk.column.table.name, fk.column.name)
                # fk.target_fullname
                for fk in column.foreign_keys)
            print '\t', column_name, '--> {0}'.format(fks) if fks else ''
        '''
    return G.to_string()
    # return G.draw(format='svg', prog='dot')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: {0} [database-connection]')
    print main(sys.argv[1], True)
'''

    session = Session(engine)
    Base = automap_base()
    Base.prepare(engine, reflect=True, name_for_collection_relationship=name_for_collection_relationship)

    for table_name, table_class in Base.classes.items():
        print table_name
        for m in dir(table_class):
            if __COLLECTION_SUFFIX in m:
                child = getattr(table_class, m)
                print '\t{0}, {1}, {2}'.format(child, child.property.uselist, child.property.secondary)
    #list(meta.tables['bar'].columns['foo'].foreign_keys)
'''


'''
for table_name in table_names:
    table = Base.classes[table_name]
    tabledata = session.query(table).all()
    for row in tabledata:
        row_dict = __row2dict(row)
        print row_dict
'''

'''
PRAGMA foreign_keys=ON;

create table foo (
    id int not null,
    id2 int not null,
    flag boolean not null,
    constraint PK_foo primary key(id, id2)
);

insert into foo(id, id2, flag) values (1, 14, 1);
insert into foo(id, id2, flag) values (2, 14, 0);

create table bar (
    id int not null primary key,
    foo int not null,
    foo2 int not null,
    foreign key(foo, foo2) references foo(id, id2)
);

insert into bar(id, foo, foo2) values (5, 1, 14);
insert into bar(id, foo, foo2) values (7, 1, 14);
insert into bar(id, foo, foo2) values (8, 2, 14);
insert into bar(id, foo, foo2) values (15, 2, 14);
insert into bar(id, foo, foo2) values (42, 4, 15);

'''



'''

PRAGMA foreign_keys=ON;
CREATE TABLE foo(
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    CONSTRAINT PK_automount_maps PRIMARY KEY (name, location)
);

CREATE TABLE bar (
    name VARCHAR(255) NOT NULL,
    foo VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    FOREIGN KEY (foo, location) REFERENCES foo(name, location),
    CONSTRAINT PK_automount_keys PRIMARY KEY (name, foo, location)
);

insert into foo(name, location) values ('1', '14');
insert into foo(name, location) values ('2', '14');
insert into bar(name, foo, location) values ('5', '1', '14');
insert into bar(name, foo, location) values ('7', '1', '14');
insert into bar(name, foo, location) values ('8', '2', '14');
insert into bar(name, foo, location) values ('15', '2', '14');
insert into bar(name, foo, location) values ('42', '4', '15');

'''
