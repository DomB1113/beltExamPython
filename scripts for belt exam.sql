-- SELECT * from skeptics JOIN logins on skeptics.login_id = logins.id 
select sightings.* , skeptics.login_id as skeptic_id
	, count(skeptics.login_id) as skeptics from sightings 
left join skeptics
	on skeptics.sighting_id = sightings.id
group by sighting_id