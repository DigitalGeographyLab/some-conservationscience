# BOX 3. TEMPORAL VARIATION OF VISITOR ACTIVITIES IN PROTECTED AREAS

Supplementary information for Box 3 in *Toivonen, T., Heikinheimo, V., Fink, C., Hausmann, A., Hiippala, T., Järv, O., Tenkanen, H., Di Minin, E. (2019). Social media data for conservation science: a methodological overview. Biological Conservation.*

### Analysis steps: 

1. Data was obtained from the Instagram API in Spring 2016 (see [Heikinheimo et al. 2017](https://www.mdpi.com/2220-9964/6/3/85/htm)). The spatial query covered 10 km buffer zone around each Finnish National Park
2. Required attributes were stored in a PostgreSQL/PostGIS database: 
    - unique identifier for each post (`photoid`)
    - point location (`geom`)
    - pseudonymized user identifier (`userid`)
    - timestamp (`time_local`)
    - caption (`text`) 
3. Temporal data related to activities in the National Park were extracted using an SQL query:
    - Spatial condition limiting the results to Pallas-Yllästunturi National Park
    - Conditional statement for thematic content (posts mentioning skiing, hiking and biking)
    - Grouping the data by month, and counting the number of users and posts per month.
4. Temporal graphs were plotted in Excel.

*Example script for extracting monthly count of skiing-related users and posts*

```
SELECT EXTRACT(MONTH FROM time_local) as month, count(DISTINCT photoid) as photocount,  count(DISTINCT userid) as usercount 

FROM(
    SELECT time_local, photoid, userid
    FROM   insta_data_finland_np_buffer_clean
    WHERE  lower(text) similar to '%(ski|hiihto|cross-country|hiiht)%' 
            AND geom 
                && -- intersects
                ST_MakeEnvelope ( --boundingbox limits:
                    23.3314,67.4699, -- xmin, ymin
                    24.7706,68.3913, -- xmax, ymax 
                    4326) --srid
    ORDER BY time_local
    ) as 
    pallasyllas_skiing

GROUP BY month;

```

