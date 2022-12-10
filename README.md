# dse203_project
python versions known to work: 3.8.9, 3.8.13
## Install
1. Clone repository
2. Set up python virtual environment called `venv`
    * unix: `python3 -m venv venv`
    * windows: `python -m venv venv`
3. Activate virtual environment
    * windows: `source venv/Scripts/activate`
    * unix fish activate: `. venv/bin/activate.fish`
    * unix: `. venv/bin/activate`
4. Install necessary dependencies
    * `pip install -r requirements.txt`
    
## Other Necessary Set Up
* C++ compliler is necessarey for py_stringmatching to be used
    * py_stringmatching is used to help match posts with specific crimes, neighborhoods, etc
    * [See py_stringmatching's dependencies for more details](https://pypi.org/project/py-stringmatching/)
* Spacy's en_core_web_sm
    * `python -m spacy download en_core_web_md`
    * This is used to do NER

## Neo4j Set Up
1. Install Neo4j Desktop
2. Create a new project
3. Navigate to project and spin up an instance
4. Create a graph database instance
5. Navigate to `...` on the graph dbms and open up the folder option
6. Navigate to the `import` directory in the graph dbms file system and copy and paste the `nodes` and `relationships` directory into `import`
7. Run the following command to upload the data into your graph dbms instance

```bash
./bin/neo4j-admin import --force --multiline-fields=true --nodes=import/nodes/crime_nodes.csv \
--nodes=import/nodes/nd_post_nodes.csv \
--nodes=import/nodes/neighborhood_nodes.csv \
--nodes=import/nodes/pd_crime_nodes.csv \
--nodes=import/nodes/reddit_post_nodes.csv \
--nodes=import/nodes/time_of_day_nodes.csv \
--nodes=import/nodes/ethnicity_nodes.csv \
--relationships=import/relationships/police_HI_rels.csv \
--relationships=import/relationships/reddit_HI_rels.csv \
--relationships=import/relationships/nextdoor_HI_rels.csv \
--relationships=import/relationships/reddit_BT_crime_rel.csv \
--relationships=import/relationships/nextdoor_BT_crime_rel.csv \
--relationships=import/relationships/police_BT_crime_rel.csv \
--relationships=import/relationships/police_HA_rels.csv \
--relationships=import/relationships/reddit_EM_rels.csv \
--relationships=import/relationships/nextdoor_EM_rels.csv
```