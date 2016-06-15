#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gets the visual representation of database schema (data model)
"""


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
    """
    The main function used to generate database schema
    description in the dot language
    """
    engine = create_engine(sqlalchemy_connection)

    meta = MetaData()
    meta.reflect(bind=engine)

    env = Environment(
        loader=FileSystemLoader(THIS_DIR),
        trim_blocks=True,
        lstrip_blocks=True)
    node_template = env.get_template('node-template.html')

    g = pgv.AGraph(strict=False,
                   directed=True,
                   name=engine.url.database,
                   graph_type='digraph',
                   compound='true',
                   rankdir='RL')
    tables = meta.tables.values()
    # tables = engine.table_names()

    for table in tables:
        if table.name.lower().startswith('sqlite_'):
            continue
        g.add_node(
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
            g.add_edge(
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
                # samehead=fk.column.name, sametail=fk.parent.name,
            )
    return g.to_string()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: {0} [database-connection]')
    print main(sys.argv[1], True)
