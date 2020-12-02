insert into conferjournal values('SIGIR','c','sigir','A+','A+','A+','sigir');

insert into conferjournal values('ACL','c','acl','A','A','A','acl');

insert into conferjournal values('IEEE','j','ieee','B','B','B','ieee');

insert into paper(title,conferorjournal,publishtime,volume,issue,startpage,endpage,keywords,conferencecountry,conferencecity,papertype,language,conferjournalname) values('AAA','C','2020-11-30',null,null,10,14,'nbnbnb','China','Xinjiang','长文Poster','E','SIGIR');

insert into paper(title,conferorjournal,publishtime,volume,issue,startpage,endpage,keywords,conferencecountry,conferencecity,papertype,language,conferjournalname) values('BBB','J','2018-11-30',1,1,20,30,'','','','正刊','E','IEEE');

insert into paper(title,conferorjournal,publishtime,volume,issue,startpage,endpage,keywords,conferencecountry,conferencecity,papertype,language,conferjournalname) values('CCC','C','2020-11-30',null,null,10,14,'why keywords','USA','New York','短文Oral','E','ACL');

insert into author values('2018202180','pt');
insert into author values('2018202195','snl');
insert into author values('szh','szh');

insert into pa(authorname,authorrank,authoridentity,authortype,paperid) values('pt',1,'普通作者','本院教师',1);
insert into pa(authorname,authorrank,authoridentity,authortype,paperid) values('snl',2,'普通作者','本院学生',1);
insert into pa(authorname,authorrank,authoridentity,authortype,paperid) values('szh',1,'通讯作者','其他',2);
insert into pa(authorname,authorrank,authoridentity,authortype,paperid) values('snl',1,'普通作者','本院学生',2);
insert into pa(authorname,authorrank,authoridentity,authortype,paperid) values('pt',1,'普通作者','本院教师',3);
insert into pa(authorname,authorrank,authoridentity,authortype,paperid) values('snl',2,'普通作者','本院学生',3);
insert into pa(authorname,authorrank,authoridentity,authortype,paperid) values('szh',1,'通讯作者','其他',3);