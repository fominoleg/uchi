select count(distinct st_id)
from (
	select 	st_id, correct, timest,
			count(*) filter (where correct) over (partition by st_id
			                                      order by timest range between current row and '1hour' following) cnt
		from peas
	where timest >= '2020-03-01' and timest < '2020-04-01'
) t
where cnt >= 20