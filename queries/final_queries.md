### 1. Time of day - Top 3 crimes
```sql
CALL {match (report)-[:BELONGS_TO]->(c),(report)-[:HAPPENED_AT]->(t)
WITH t, size(collect(DISTINCT c.crime_set)) as count_of_crimes
order by count_of_crimes DESC RETURN distinct t.time_of_day_id AS top_t }
UNWIND top_t as t_i
MATCH (report)-[:BELONGS_TO]->(c),(report)-[:HAPPENED_AT]->(t:TIME_OF_DAY {time_of_day_id:t_i})
WITH c, t, count(t_i) as t_count
ORDER BY t_count DESC
RETURN t.date_time_bin as time_of_day, collect(c.crime_set)[..3] as top_3_crimes
```

### 2.  Top 3 crimes per neighborhood [Top 5 neighborhood with crime related posts]
```sql
CALL {match (report)-[:BELONGS_TO]->(c),(report)-[:HAPPENED_IN]->(n)
WITH n,size(collect(DISTINCT c.crime_set)) as count_of_crimes
order by count_of_crimes DESC RETURN n.neighborhood_set_id AS top_n LIMIT 5}
UNWIND top_n as n_i
MATCH (report)-[:BELONGS_TO]->(c),(report)-[:HAPPENED_IN]->(n:neighborhood {neighborhood_set_id:n_i})
WITH c, n, count(n_i) as n_count
ORDER BY n_count DESC
RETURN n.neighborhood_set as neighbourhood,collect(c.crime_set)[..3] as top_3_crimes
```


### 3. Distribution of crime posts related to few local stores [ORG label from NER]
```sql
WITH ['walmart','ikea','walgreens','costco','vons','ralphs','target','gamestop','arco','chevron'] AS org
UNWIND org as x
MATCH (p)-[:BELONGS_TO]->(c)
where p.ORG =~ (".*" + x + ".*") 
WITH x as org, count(distinct p.post_id) as count_posts
order by count_posts DESC
return distinct org as store, count_posts as crimes_posted
```


### 4. Ranking according to post counts and print top ethnicities. [Bias between two social media platforms]
```sql
CALL {match (p:REDDIT_POST)-[:ETHNICITY_MENTIONED]->(e), (p)-[:BELONGS_TO]->(c)
with e.ethnicity as eth, count(distinct p.post_id) as count_posts
ORDER BY count_posts DESC
WITH COLLECT(eth) as rs
UNWIND range(1,size(rs)) as rank
RETURN  'reddit' as media, rs[rank-1] as r, rank limit 10
UNION
match (p:NEXTDOOR_POST)-[:ETHNICITY_MENTIONED]->(e), (p)-[:BELONGS_TO]->(c)
with e.ethnicity as eth, count(distinct p.post_id) as count_posts
ORDER BY count_posts DESC
WITH COLLECT(eth) as rs
UNWIND range(1,size(rs)) as rank
RETURN 'nextdoor' as media, rs[rank-1] as r,  rank limit 10}
WITH media, r as ethnicity, rank 
order by rank, media
return rank, media, ethnicity
```


# GDS
## 5. Crime linked to crime using shared nodes
```SQL
MATCH (c1:crime)--(n)--(c2:crime)
WITH n,c1,c2
return c1,c2,n
Limit 200
```


## 6. Crime Graph Creation
```SQL
CALL gds.graph.project.cypher('crime_graph',
'MATCH (c) where c:crime return id(c) as id ',
'MATCH (c1:crime)--(n)--(c2:crime) WHERE id(c1) < id(c2) WITH COUNT(n) as cntn,c1,c2 
return distinct id(c1) as source, id(c2) as target, cntn as weight')
```

## 6.1. Page Rank
##### The PageRank algorithm measures the importance of each node within the graph, based on the number incoming relationships and the importance of the corresponding source nodes. The underlying assumption roughly speaking is that a page is only as important as the pages that link to it.
```SQL
CALL gds.pageRank.stream('crime_graph', {
  maxIterations: 20,
  dampingFactor: 0.85,
  relationshipWeightProperty: 'weight'
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).crime_set_id AS crime_id, gds.util.asNode(nodeId).crime_set as crime_bucket, score as full_pagerank
ORDER BY full_pagerank DESC limit 10
```

## 6.2. Community detection for crimes
##### The Louvain method is an algorithm to detect communities in large networks. It maximizes a modularity score for each community, where the modularity quantifies the quality of an assignment of nodes to communities. This means evaluating how much more densely connected the nodes within a community are, compared to how connected they would be in a random network.
```sql
CALL gds.louvain.stream('crime_graph')
YIELD nodeId, communityId, intermediateCommunityIds
WITH gds.util.asNode(nodeId).crime_set AS crime_bucket, communityId
with communityId, size(collect(crime_bucket)) AS size, collect(crime_bucket) as crimes
WHERE  size > 1 and  size <15
RETURN communityId, size, crimes limit 10
```

## 6.3. Degree Centrality for crime node
##### The Degree Centrality algorithm can be used to find popular nodes within a graph. Degree centrality measures the number of incoming or outgoing (or both) relationships from a node, depending on the orientation of a relationship projection.
```sql
CALL gds.degree.stream('crime_graph')
YIELD nodeId, score
RETURN  score ,  gds.util.asNode(nodeId).crime_set AS crime_bucket
ORDER BY score DESC limit 10
```

## 6.4. Drop an in-memory graph
```sql
CALL gds.graph.drop('crime_graph')
```

































# supplemental 

### Total posts grouped by neighborhood - S
```sql
MATCH (post)-[:HAPPENED_IN]->(n:neighborhood)
WITH n, size(collect(distinct post)) AS countof_posts
ORDER BY countof_posts DESC
RETURN n.neighborhood_set,countof_posts limit 5
```

### Total crime related posts grouped by neighborhood - S
```sql
MATCH (post)-[:HAPPENED_IN]->(n:neighborhood),(post)-[:BELONGS_TO]->(c)
WITH n, size(collect(distinct post)) AS countof_posts
ORDER BY countof_posts DESC
RETURN n.neighborhood_set,countof_posts limit 5
```



### Top 10 neighborhoods by unique crimes commited(For all posts) - S
```sql
match (post)-[:BELONGS_TO]->(c),(post)-[:HAPPENED_IN]->(n)
WITH n,size(collect(DISTINCT c.crime_set)) as count_of_crimes
order by count_of_crimes DESC
return n.neighborhood_set,count_of_crimes  limit 10
```



### Distribution of Unique crimes committed at a particular Time of Day - S
#change display alias
```sql
match (r:REPORTED_CRIME)-[:HAPPENED_AT]->(tod)
,(r)-[:BELONGS_TO]->(c)
WITH tod.date_time_bin as tod, count(distinct c.crime_set) as count_crimes
order by count_crimes desc
return tod, count_crimes
```


### Total crimes committed at a particular Time of Day - S
```sql
match (r:REPORTED_CRIME)-[:HAPPENED_AT]->(tod)
,(r)-[:BELONGS_TO]->(c)
WITH tod.date_time_bin as tod, count(c.crime_set) as count_crimes
order by count_crimes desc
return tod, count_crimes
```



### Top Crime commited with Top 5 ethnicities with most crime related posts - Modify - S
```sql
CALL {match (report)-[:BELONGS_TO]->(c),(report)-[:ETHNICITY_MENTIONED]->(e)
WITH e,size(collect(DISTINCT c.crime_set)) as count_of_crimes
order by count_of_crimes DESC RETURN e.eth_id AS top_e LIMIT 5}
UNWIND top_e as e_i
MATCH (report)-[:BELONGS_TO]->(c),(report)-[:ETHNICITY_MENTIONED]->(e:ethnicity {eth_id:e_i})
WITH c, e, count(e_i) as e_count
ORDER BY e_count DESC
RETURN e.ethnicity ,e_count, c.crime_set as crime
``` 



### Top 5 neighborhoods with all posts from republican and democrat - S
```sql
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

```
