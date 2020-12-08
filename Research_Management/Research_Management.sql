create table ConferJournal(
    Name varchar(512) primary key,
    ConferOrJournal char(1) not null,  -- C or J
    Abbreviation varchar(50),
    RUCLevel char(2) not null,
    CCFLevel char(2) not null,
    CCFChinaLevel char(2) not null,
    ISSN varchar(50)
);

create table Author(
    AuthorID varchar(12) primary key,
    Name varchar(20) not null
);

create table Paper(
    PaperID bigint primary key auto_increment,
	Title varchar(1024) not null,
    ConferOrJournal char(1) not null,  -- C or J
	ConferJournalName varchar(512) not null,
    PublishTime date not null,
    Volume integer,
    Issue integer,
	StartPage integer not null,
	EndPage integer not null,
    Keywords varchar(100),
    ConferenceCountry varchar(50),
    ConferenceCity varchar(50),
    PaperType varchar(20) not null,
    Language char(1), -- E or C
    foreign key(ConferJournalName) references ConferJournal(Name)
);

create table PA(
    PAID bigint primary key auto_increment,
    PaperID bigint not null,
    AuthorName varchar(20) not null,
    AuthorRank integer not null,            -- 第几作者
    AuthorIdentity varchar(20) not null,    -- 通讯作者、普通作者
    AuthorType varchar(20) not null,        -- 本院教师 本院学生 其他
    foreign key(PaperID) references Paper(PaperID)
);

create table tmpPaper(
    PaperID bigint primary key auto_increment,
    CommitAuthorID varchar(12) not null,
	Title varchar(1024) not null,
    ConferOrJournal char(1) not null,  -- C or J
	ConferJournalName varchar(512) not null,
    PublishTime date not null,
    Volume integer,
    Issue integer,
	StartPage integer not null,
	EndPage integer not null,
    Keywords varchar(100),
    ConferenceCountry varchar(50),
    ConferenceCity varchar(50),
    PaperType varchar(20) not null, -- 正刊 专刊 增刊 长文Oral 长文Poster 短文Oral 短文Poster Demo
    Language char(1), -- E or C
    foreign key(CommitAuthorID) references Author(AuthorID),
    foreign key(ConferJournalName) references ConferJournal(Name)
);

create table tmpPA(
    PAID bigint primary key auto_increment,
    PaperID bigint not null,
    AuthorName varchar(20) not null,
    AuthorRank integer not null,            -- 第几作者
    AuthorIdentity varchar(20) not null,    -- 通讯作者、普通作者
    AuthorType varchar(20) not null,        -- 本院教师 本院学生 其他
    foreign key(PaperID) references tmpPaper(PaperID)
);