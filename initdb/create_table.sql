create table contents (
  url text not null
  , domain_name text not null
  , register_date timestamp with time zone not null
  , title text not null
  , contents text not null
  , constraint contents_PKC primary key (url)
) ;

comment on table contents is 'コンテンツ';
comment on column contents.url is 'URL';
comment on column contents.domain_name is 'ドメイン';
comment on column contents.register_date is '登録日時';
comment on column contents.title is 'タイトル';
comment on column contents.contents is 'コンテンツ';