SET GLOBAL local_infile=1;
SET SESSION max_heap_table_size = 1024 * 1024 * 256;
SET SESSION tmp_table_size = 1024 * 1024 * 256;
DROP DATABASE IF EXISTS subjects;
CREATE DATABASE subjects DEFAULT CHARACTER SET utf8mb4;
USE subjects;
drop table if exists base;
CREATE TABLE base(
    id MEDIUMINT PRIMARY KEY,
    yobi TINYINT,
    jigen TINYINT,
    year SMALLINT,
    name VARCHAR(32),
    kubun VARCHAR(16),
    keitai VARCHAR(5),
    tani TINYINT,
    gakunen TINYINT,
    gakki TINYINT,
    subj_id VARCHAR(6),
    teacher VARCHAR(200),
    keyword VARCHAR(500),
    gaiyo VARCHAR(2000),
    mokuhyo VARCHAR(1500),
    isActiveLearn VARCHAR(5),
    ActiveLearn VARCHAR(500),
    isJitsumu VARCHAR(5),
    Jitsumu VARCHAR(500),
    kimatsu VARCHAR(10),
    seiseki_kijun VARCHAR(1000),
    hyouka_ho VARCHAR(1500),
    youi VARCHAR(1000),
    risyu_chui VARCHAR(3000)
)
-- ENGINE=MEMORY
;
load data
    local
    infile '/docker-entrypoint-initdb.d/base.tsv'
    into table base
    fields
        TERMINATED by ','
        ENCLOSED BY '"'
    LINES TERMINATED BY '\t'
    IGNORE 1 LINES
    set
        id = nullif(id, ''),
        yobi = nullif(yobi, ''),
        jigen = nullif(jigen, ''),
        year = nullif(year, ''),
        name = nullif(name, ''),
        kubun = nullif(kubun, ''),
        keitai = nullif(keitai, ''),
        tani = nullif(tani, ''),
        gakunen = nullif(gakunen, ''),
        gakki = nullif(gakki, ''),
        subj_id = nullif(subj_id, ''),
        teacher = nullif(teacher, ''),
        keyword = nullif(keyword, ''),
        gaiyo = nullif(gaiyo, ''),
        mokuhyo = nullif(mokuhyo, ''),
        isActiveLearn = nullif(isActiveLearn, ''),
        ActiveLearn = nullif(ActiveLearn, ''),
        isJitsumu = nullif(isJitsumu, ''),
        Jitsumu = nullif(Jitsumu, ''),
        kimatsu = nullif(kimatsu, ''),
        seiseki_kijun = nullif(seiseki_kijun, ''),
        hyouka_ho = nullif(hyouka_ho, ''),
        youi = nullif(youi, ''),
        risyu_chui = nullif(risyu_chui, '')
;
drop table if exists kai;
CREATE TABLE kai(
    id MEDIUMINT,
    n_kai TINYINT,
    keikaku VARCHAR(500),
    naiyo VARCHAR(500)
)
-- ENGINE=MEMORY
;
load data
    local
    infile '/docker-entrypoint-initdb.d/kai.tsv'
    into table kai
    fields
        TERMINATED by ','
        ENCLOSED BY '"'
    LINES TERMINATED BY '\t'
    IGNORE 1 LINES
    set
        id = nullif(id, ''),
        n_kai = nullif(n_kai, ''),
        keikaku = nullif(keikaku, ''),
        naiyo = nullif(naiyo, '')
;
