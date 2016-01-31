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
    -- ,CONSTRAINT PK_bar PRIMARY KEY (id, foo, foo2)
);

insert into bar(id, foo, foo2) values (5, 1, 14);
insert into bar(id, foo, foo2) values (7, 1, 14);
insert into bar(id, foo, foo2) values (8, 2, 14);
insert into bar(id, foo, foo2) values (15, 2, 14);
--insert into bar(id, foo, foo2) values (42, 4, 15);
