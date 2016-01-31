PRAGMA foreign_keys=ON;

drop table if exists statuses;
create table statuses (
    id integer primary key autoincrement,
	status text not null
);
insert into statuses values(null, "done");
insert into statuses values(null, "pending");
insert into statuses values(null, "unread");

drop table if exists formats;
create table formats (
    id integer primary key autoincrement,
	format text not null
);
insert into formats values(null, "conference paper");
insert into formats values(null, "conference presentation");
insert into formats values(null, "vendor whitepaper");

drop table if exists documents;
create table documents (
    id integer primary key autoincrement,
    document_id text not null unique,
    fs_name text not null,
    friendly_name text
);

drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    status_id integer,
    format_id integer,
    citation text not null,
    document_id text,
    summary text,
    FOREIGN KEY(status_id) REFERENCES statuses(id),
    FOREIGN KEY(format_id) REFERENCES formats(id),
    FOREIGN KEY(document_id) REFERENCES documents(document_id)
);
