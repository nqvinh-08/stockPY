create table stock_db.stocks
(
	symbol String,
	datetime DateTime,
	open Float64,
	close Float64,
	high Float64,
	low Float64,
	volume Int32
)
engine = MergeTree()
order by (symbol, datetime);
	
--bang user--
create table stock_db.user(
	username String,
	password String
)
engine = MergeTree()
order by username

----data mart-------
create table mart_stock
(	
	datetime Datetime,
	daily_return float,
	avg_range float
)
engine = SummingMergeTree()
order by datetime