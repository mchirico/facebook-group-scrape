--
--
--

create table if not exists post (
gid text,
pid text,
id text,
name text,
timeStamp datetime,
shares text,
url text,
msg text,
likes text);

create index if not exists igid on post(gid);
create index if not exists ipid on post(pid);
create index if not exists iid on post(id);
create index if not exists iname on post(name);
create index if not exists itimeStamp on post(timeStamp);
create index if not exists imsg on post(msg);
create index if not exists ilikes on post(msg);

.separator ","
.import postNH.csv post

-- like

create table if not exists like (
gid text,
pid text,
cid text,
response text,
id text,
name text);


create index if not exists ilgid on like(gid);
create index if not exists ilpid on like(pid);
create index if not exists ilcid on like(cid);
create index if not exists ilresponse on like(response);
create index if not exists ilid on like(id);
create index if not exists ilname on like(name);


.separator ","
.import likeNH.csv like



-- comment
--  SQLITE imports data as text, which means you won's
--  get null values.  Should this be set later?
--
--  UPDATE comment SET rid=NULL WHERE rid='';

create table if not exists comment (
gid text,
pid text,
cid text,
timeStamp datetime,
id text,
name text,
rid text,
msg text);


create index if not exists icgid on comment(gid);
create index if not exists icpid on comment(pid);
create index if not exists iccid on comment(cid);
create index if not exists ictimeStamp on comment(timeStamp);
create index if not exists icid on comment(id);
create index if not exists icname on comment(name);
create index if not exists icrid on comment(rid);
create index if not exists icmsg on comment(msg);


.separator ","
.import commentNH.csv comment



-- member

create table if not exists member (
gid text,
id text,
name text,
url text);


create index if not exists imgid on member(gid);
create index if not exists imid on member(id);
create index if not exists imname on member(name);
create index if not exists imurl on member(url);



.separator ","
.import memberNH.csv member

