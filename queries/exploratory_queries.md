## Top 5 neighborhoods witch high number of posts for nextdoor
MATCH (post:NEXTDOOR_POST)-[:HAPPENED_IN]->(n:neighborhood)
WITH n, size(collect(post)) AS countof_posts
ORDER BY countof_posts DESC
RETURN n.neighborhood_set,countof_posts limit 5


## Top 5 neighborhoods with highest number of posts
MATCH (post)-[:HAPPENED_IN]->(n:neighborhood)
WITH n, size(collect(post)) AS countof_posts
ORDER BY countof_posts DESC
RETURN n.neighborhood_set,countof_posts limit 5

## Top 5 neighborhoods with highest number of crime related posts or police calls
MATCH (post)-[:HAPPENED_IN]->(n:neighborhood),(post)-[:BELONGS_TO]->(c)
WITH n, size(collect(post)) AS countof_posts
ORDER BY countof_posts DESC
RETURN n.neighborhood_set,countof_posts limit 5


## Higher number of crime related nextdoor posts for a neighborhood
MATCH (post:NEXTDOOR_POST)-[:HAPPENED_IN]->(n:neighborhood)
WITH n, size(collect(post)) AS countof_posts
RETURN max(countof_posts)


## Sample output with neighborhood_set and correspoinding list of crimes associated in all the posts 
match (post:NEXTDOOR_POST)-[:BELONGS_TO]->(c),(post)-[:HAPPENED_IN]->(n)
WITH n,c.crime_set as crimes
return n.neighborhood_set, collect(crimes) limit 10
