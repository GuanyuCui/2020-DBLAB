insert into conferjournal values('SIGIR','c','sigir','A+','A+','A+','sigir');

insert into conferjournal values('ACL','c','acl','A','A','A','acl');

insert into conferjournal values('IEEE','j','ieee','B','B','B','ieee');

insert into paper(title,conferorjournal,publishtime,volume,issue,startpage,endpage,keywords,conferencelocation,papertype,language,conferjournalname) values('AAA','c','2020-11-30',null,null,10,14,'','xinjiang','长文Poster','E','SIGIR');

insert into paper(title,conferorjournal,publishtime,volume,issue,startpage,endpage,keywords,conferencelocation,papertype,language,conferjournalname) values('BBB','j','2018-11-30',1,1,20,30,'','beijing','正刊','E','IEEE');

insert into paper(title,conferorjournal,publishtime,volume,issue,startpage,endpage,keywords,conferencelocation,papertype,language,conferjournalname) values('CCC','c','2020-11-30',null,null,10,14,'','beijing','短文Oral','E','ACL');

insert into author values('2018202180','pt');
insert into author values('2018202175','snl');
insert into author values('szh','szh');

insert into pa(authorname,authorrank,authoridentity,authortype,paperid) values('pt',1,'普通作者','本院教师',1);
insert into pa(authorname,authorrank,authoridentity,authortype,paperid) values('snl',2,'普通作者','本院学生',1);
-- 应该只给普通作者排authorrank？
insert into pa(authorname,authorrank,authoridentity,authortype,paperid) values('szh',1,'通讯作者','其他',2);
insert into pa(authorname,authorrank,authoridentity,authortype,paperid) values('snl',1,'普通作者','本院教师',2);
