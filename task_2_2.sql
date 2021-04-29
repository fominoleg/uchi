select
		avg(money) as arpu,
		avg(money) filter (where resolved_peas >= 30) as arpau,
		count(*) filter (where money is not null) / count(*) as cr,
		count(*) filter (where money is not null and resolved_peas >= 30) / count(*) as cr1,
		count(*) filter (where money is not null and peas.subject = 'math') / count(*) as cr2
	from (
	--Джойн горошин с справочником группы в эксперименте
	select peas.*, studs.test_grp
		from (
		--Считаем для каждого студента и предмета по дням кол-во решенных "горошин"
		select st_id, subject, timest::date as dt, count(*) as resolved_peas
			from peas
		group by st_id, subject, dt
		) as peas
		left join
		studs
	on peas.st_id = studs.st_id
	) as peas
	left join
	(select st_id, sale_time::date as dt, subject, sum(money) as money
		from checks
	group by st_id, dt, subject) as checks
on peas.dt = checks.dt
and peas.st_id = checks.st_id
and peas.subject = checks.subject
