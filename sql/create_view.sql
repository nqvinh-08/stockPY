create materialized view mv_stock_analysis
to mart_stock
as 
select 
	datetime,
	round(
		(close-open)*100.0 / open ,2
	) as daily_return,
	avg(high -low) as avg_range
from stock_db.stocks
group by datetime,close,open,high,low