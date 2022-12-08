## Top 5 neighborhoods witch high number of posts for nextdoor
MATCH (post:NEXTDOOR_POST)-[:HAPPENED_IN]->(n:neighborhood)
WITH n, size(collect(distinct post)) AS countof_posts
ORDER BY countof_posts DESC
RETURN n.neighborhood_set,countof_posts limit 5


## Top 5 neighborhoods with highest number of posts
MATCH (post)-[:HAPPENED_IN]->(n:neighborhood)
WITH n, size(collect(distinct post)) AS countof_posts
ORDER BY countof_posts DESC
RETURN n.neighborhood_set,countof_posts limit 5

## Top 5 neighborhoods with highest number of crime related posts or police calls
MATCH (post)-[:HAPPENED_IN]->(n:neighborhood),(post)-[:BELONGS_TO]->(c)
WITH n, size(collect(distinct post)) AS countof_posts
ORDER BY countof_posts DESC
RETURN n.neighborhood_set,countof_posts limit 5


## Higher number of crime related nextdoor posts for a neighborhood
MATCH (post:NEXTDOOR_POST)-[:HAPPENED_IN]->(n:neighborhood)
WITH n, size(collect(distinct post)) AS countof_posts
RETURN max(countof_posts)


## Sample output with neighborhood_set and correspoinding list of crimes associated in all the posts 
match (post:NEXTDOOR_POST)-[:BELONGS_TO]->(c),(post)-[:HAPPENED_IN]->(n)
WITH n,c.crime_set as crimes
return n.neighborhood_set, collect(crimes) limit 10


## Top 10 neighborhoods with diverse crimes commited (NEXTDOOR)
match (post:NEXTDOOR_POST)-[:BELONGS_TO]->(c),(post)-[:HAPPENED_IN]->(n)
WITH n,size(collect(DISTINCT c.crime_set)) as count_of_crimes
order by count_of_crimes DESC
return n.neighborhood_set,count_of_crimes  limit 10


## Top 10 neighborhoods with diverse crimes commited(For all posts)
match (post)-[:BELONGS_TO]->(c),(post)-[:HAPPENED_IN]->(n)
WITH n,size(collect(DISTINCT c.crime_set)) as count_of_crimes
order by count_of_crimes DESC
return n.neighborhood_set,count_of_crimes  limit 10



## Top Crime commited in Top 5 neighborhoods with most crime related posts
CALL {match (report)-[:BELONGS_TO]->(c),(report)-[:HAPPENED_IN]->(n)
WITH n,size(collect(DISTINCT c.crime_set)) as count_of_crimes
order by count_of_crimes DESC RETURN n.neighborhood_set_id AS top_n LIMIT 5}
UNWIND top_n as n_i
MATCH (report)-[:BELONGS_TO]->(c),(report)-[:HAPPENED_IN]->(n:neighborhood {neighborhood_set_id:n_i})
WITH c, n, count(n_i) as n_count
ORDER BY n_count DESC
RETURN n_count, n.neighborhood_set as neighbourhood,c.crime_set as crime



## Top Crime commited with Top 5 ethnicities with most crime related posts
CALL {match (report)-[:BELONGS_TO]->(c),(report)-[:ETHNICITY_MENTIONED]->(e)
WITH e,size(collect(DISTINCT c.crime_set)) as count_of_crimes
order by count_of_crimes DESC RETURN e.eth_id AS top_e LIMIT 5}
UNWIND top_e as e_i
MATCH (report)-[:BELONGS_TO]->(c),(report)-[:ETHNICITY_MENTIONED]->(e:ethnicity {eth_id:e_i})
WITH c, e, count(e_i) as e_count
ORDER BY e_count DESC
RETURN e.ethnicity ,e_count, c.crime_set as crime


## Top 5 neighborhoods with crime related posts from republican and democrat
match (p)-[:ETHNICITY_MENTIONED]->(e:ethnicity {ethnicity : 'republican'}) ,
(p)-[:BELONGS_TO]->(c),
(p)-[:HAPPENED_IN]->(n)
with n, size(collect(distinct p)) AS countof_posts, e.ethnicity as eth
ORDER BY countof_posts DESC
return  n.neighborhood_set,countof_posts, eth limit 5
UNION
match (p)-[:ETHNICITY_MENTIONED]->(e:ethnicity {ethnicity : 'democrat'}) ,
(p)-[:BELONGS_TO]->(c),
(p)-[:HAPPENED_IN]->(n)
with n, size(collect(distinct p)) AS countof_posts, e.ethnicity as eth
ORDER BY countof_posts DESC
return  n.neighborhood_set,countof_posts, eth limit 5

## Top 5 neighborhoods with all posts from republican and democrat
match (p)-[:ETHNICITY_MENTIONED]->(e:ethnicity {ethnicity : 'republican'}) ,
//(p)-[:BELONGS_TO]->(c),
(p)-[:HAPPENED_IN]->(n)
with n, size(collect(distinct p)) AS countof_posts, e.ethnicity as eth
ORDER BY countof_posts DESC
return  n.neighborhood_set,countof_posts, eth limit 5
UNION
match (p)-[:ETHNICITY_MENTIONED]->(e:ethnicity {ethnicity : 'democrat'}) ,
//(p)-[:BELONGS_TO]->(c),
(p)-[:HAPPENED_IN]->(n)
with n, size(collect(distinct p)) AS countof_posts, e.ethnicity as eth
ORDER BY countof_posts DESC
return  n.neighborhood_set,countof_posts, eth limit 5




## (CARTESIAN PROBLEM SOV=LVED) Top 5 neighborhoods with crime related posts from republican and democrat
match (p)-[:ETHNICITY_MENTIONED]->(e:ethnicity {ethnicity : 'republican'})  ,
(p)-[:BELONGS_TO]->(c),
(p)-[:HAPPENED_IN]->(n)
with n, p.post_id as pid, e.ethnicity as eth, c.crime_set as crimes
//ORDER BY countof_posts DESC
return distinct  n.neighborhood_set_id,pid, eth , crimes



## UGLY QUERY

match (p)-[:BELONGS_TO]->(c)
where p.ORG =~ '.*walmart.*'
WITH 'walmart' as org,count(distinct p.post_id) as count_posts
return org,count_posts 
UNION
match (p)-[:BELONGS_TO]->(c)
where p.ORG =~ '.*vons.*'
WITH 'vons' as org,count(distinct p.post_id) as count_posts
return org,count_posts
UNION
match (p)-[:BELONGS_TO]->(c)
where p.ORG =~ '.*cvs.*'
WITH 'cvs' as org,count(distinct p.post_id) as count_posts
return org,count_posts
UNION
match (p)-[:BELONGS_TO]->(c)
where p.ORG =~ '.*ralphs.*'
WITH 'ralphs' as org,count(distinct p.post_id) as count_posts
return org,count_posts
UNION
match (p)-[:BELONGS_TO]->(c)
where p.ORG =~ '.*walgreens.*'
WITH 'walgreens' as org,count(distinct p.post_id) as count_posts
return org,count_posts
UNION
match (p)-[:BELONGS_TO]->(c)
where p.ORG =~ '.*ikea.*'
WITH 'ikea' as org,count(distinct p.post_id) as count_posts
return org,count_posts


## WORKING QUERY - [Distribution of crime posts related to an ORG]
WITH ['walmart','ikea','walgreens','costco','vons','ralphs','target','gamestop','arco','chevron'] AS org
UNWIND org as x
MATCH (p)-[:BELONGS_TO]->(c)
where p.ORG =~ (".*" + x + ".*") 
WITH x as org, count(distinct p.post_id) as count_posts
order by count_posts DESC
return distinct org, count_posts



## Social media - ethnicities [NOT PERFECT]
match (p:NEXTDOOR_POST)-[:ETHNICITY_MENTIONED]->(e)
with e.ethnicity as eth, count(distinct p.post_id) as count_posts
ORDER BY count_posts DESC
WITH count_posts, COLLECT(distinct eth) as rs,eth 
UNWIND range(1,8) as rank
RETURN distinct eth,rank, count_posts


# top 10 ethnicities for nextdoor [with rank]
match (p:NEXTDOOR_POST)-[:ETHNICITY_MENTIONED]->(e)
with e.ethnicity as eth, count(distinct p.post_id) as count_posts
ORDER BY count_posts DESC
WITH COLLECT(eth) as rs
UNWIND range(1,size(rs)) as rank
RETURN rs[rank-1] as r, rank limit 10

# top 10 ethnicities for reddit [with rank]
match (p:REDDIT_POST)-[:ETHNICITY_MENTIONED]->(e)
with e.ethnicity as eth, count(distinct p.post_id) as count_posts
ORDER BY count_posts DESC
WITH COLLECT(eth) as rs
UNWIND range(1,size(rs)) as rank
RETURN rs[rank-1] as r, rank limit 10



## SUCKS - DID NOT WORK - PRint Ethnicities between reddit and nextdoor against each other as per rank

WITH {match (p:NEXTDOOR_POST)-[:ETHNICITY_MENTIONED]->(e)
with e.ethnicity as eth, count(distinct p.post_id) as count_posts
ORDER BY count_posts DESC
WITH COLLECT(eth) as rs
UNWIND range(1,size(rs)) as rank
RETURN rank, rs[rank-1] as r_n limit 10} as resultSet1

WITH resultSet1, {match (p:REDDIT_POST)-[:ETHNICITY_MENTIONED]->(e)
with e.ethnicity as eth, count(distinct p.post_id) as count_posts
ORDER BY count_posts DESC
WITH COLLECT(eth) as rs
UNWIND range(1,size(rs)) as rank
RETURN rank, rs[rank-1] as r_r limit 10} as resultSet2

UNWIND resultSet2 as rec
WITH [item in resultSet1 WHERE item.rank = rec.rank][0] as match, rec

RETURN match.rank, match.r_n, rec.r_r



## Ranking according to order and print top ethnicities.

CALL {match (p:REDDIT_POST)-[:ETHNICITY_MENTIONED]->(e)
with e.ethnicity as eth, count(distinct p.post_id) as count_posts
ORDER BY count_posts DESC
WITH COLLECT(eth) as rs
UNWIND range(1,size(rs)) as rank
RETURN (rs[rank-1]+'_reddit') as r, rank limit 5
UNION
match (p:NEXTDOOR_POST)-[:ETHNICITY_MENTIONED]->(e)
with e.ethnicity as eth, count(distinct p.post_id) as count_posts
ORDER BY count_posts DESC
WITH COLLECT(eth) as rs
UNWIND range(1,size(rs)) as rank
RETURN  (rs[rank-1]+'_nextdoor') as r, rank limit 5}
WITH r, rank
order by rank
return r,rank



# Unique crimes committed at a particular Time of Day

match (r:REPORTED_CRIME)-[:HAPPENED_AT]->(tod)
,(r)-[:BELONGS_TO]->(c)
WITH tod.date_time_bin as tod, count(distinct c.crime_set) as count_crimes
order by count_crimes desc
return tod, count_crimes

# Total crimes committed at a particular Time of Day
match (r:REPORTED_CRIME)-[:HAPPENED_AT]->(tod)
,(r)-[:BELONGS_TO]->(c)
WITH tod.date_time_bin as tod, count(c.crime_set) as count_crimes
order by count_crimes desc
return tod, count_crimes



# Time of day - Top 3 crimes

CALL {match (report)-[:BELONGS_TO]->(c),(report)-[:HAPPENED_AT]->(t)
WITH t, size(collect(DISTINCT c.crime_set)) as count_of_crimes
order by count_of_crimes DESC RETURN distinct t.time_of_day_id AS top_t }
UNWIND top_t as t_i
MATCH (report)-[:BELONGS_TO]->(c),(report)-[:HAPPENED_AT]->(t:TIME_OF_DAY {time_of_day_id:t_i})
WITH c, t, count(t_i) as t_count
ORDER BY t_count DESC
RETURN t.date_time_bin, collect(c.crime_set)[..3] as crime