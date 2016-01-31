#!/usr/bin/env python

'''
Gets the visual representation of database schema (data model)
'''

import os
import sys

# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.inspection import inspect
# from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
import pygraphviz as pgv
from jinja2 import Environment, FileSystemLoader


# Capture our current directory
try:
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    THIS_DIR = os.getcwd()


def main(sqlalchemy_connection, show_type=False):
    '''
    The main function used to generate database schema
    description in the dot language
    '''
    engine = create_engine(sqlalchemy_connection)

    meta = MetaData()
    meta.reflect(bind=engine)

    env = Environment(
        loader=FileSystemLoader(THIS_DIR),
        trim_blocks=True,
        lstrip_blocks=True)
    node_template = env.get_template('node-template.html')

    G = pgv.AGraph(strict=False,
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
                headport="{0}:e".format(fk.column.name +
                                        ('_type' if show_type else '')),
                # headlabel="+ %s"%fk.column.name,
                # taillabel='+ %s'%fk.parent.name,
                # arrowhead='odottee' if fk.parent.nullable else 'teetee',
                # dir='both',
                arrowhead='none', dir='back',
                arrowtail='teeodot' if uniq_child else 'crowodot'
                #samehead=fk.column.name, sametail=fk.parent.name,
            )
    return G.to_string()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: {0} [database-connection]')
    print main(sys.argv[1], True)


'''

def __row2dict(row):
    dictret = dict(row.__dict__)
    dictret.pop('_sa_instance_state', None)
    return dict((k, v) for k, v in dictret.items())


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


def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    name = referred_cls.__name__.lower()
    local_table = local_cls.__table__
    if name in local_table.columns:
        return name + "_"
    return name


__COLLECTION_SUFFIX = "_collection"
def name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    s= "{0}_{1}_from_{2}({3})".format(
            local_cls.__name__,# .lower(),
            #referred_cls.__name__,# .lower(),
            __COLLECTION_SUFFIX,
            constraint.table.name,
            ','.join(c.name for c in constraint.columns))
    #pdb.set_trace()
    #print s
    return s


def main2(sqlalchemy_connection):
    engine = create_engine(sqlalchemy_connection)
    session = Session(engine)
    Base = automap_base()
    Base.prepare(engine, reflect=True,
        name_for_collection_relationship=name_for_collection_relationship,
        name_for_scalar_relationship=name_for_scalar_relationship)

    for table_name, table_class in Base.classes.items():
        print table_name
        for m in dir(table_class):
            if __COLLECTION_SUFFIX in m:
                child = getattr(table_class, m)
                print '\t{0}, {1}, {2}'.format(child, child.property.uselist, child.property.secondary)
        tabledata = session.query(table_class).all()
        for row in tabledata:
            row_dict = __row2dict(row)
            print row_dict
    #list(meta.tables['bar'].columns['foo'].foreign_keys)
'''
