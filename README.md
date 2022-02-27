# higher ed
we would like you to apply what you already know about business intelligence and be prepared to discuss an interesting analysis that would be appropriate for higher education. Feel free to be creative and to share any part of the analytical process (i.e organizing/modeling data, measures created, presentation of final product, tools used, test/deployment, questions answered/relevance). 

## data resources
- data.gov - https://catalog.data.gov/dataset?organization=ed-gov
- data.ed.gov - [scorecard](https://data.ed.gov/dataset/college-scorecard-all-data-files-through-6-2020/resources?resource=693ba436-110b-4a04-b6eb-d77804607f45)
- huggingface - https://huggingface.co
  - unsucessful searches: education, college, university, student
- kaggle - https://www.kaggle.com/datasets
  - https://www.kaggle.com/spscientist/students-performance-in-exams
  - https://www.kaggle.com/yasserh/student-marks-dataset
  - us department of education data - sqlite db - looks useful but old (2018)
  - https://www.kaggle.com/prasertk/qs-world-university-rankings-2021 - downloaded
  - https://www.kaggle.com/benroshan/factors-affecting-campus-placement
  - * https://www.kaggle.com/wsj/college-salaries (WSJ and degrees that pay back) - downloaded
- common data set - http://commondataset.org/
  - the url for data looks like: https://commondataset.org/wp-content/uploads/2021/10/CDS_2021-2022-1.xlsx
  - cannot find an archive of prior years - each universiy has a separate archive of their submissions over tiem (e.g. MIT)
  - subdirs are forbidden 403 error but CDS_2021-2022.xlsx is a valid file - could we gess the month and filename to get prior years data
  - :thumbsdown: this is just the form to fill out - does not contain any output
  - :heavy_dollar_sign: data can be obtained on usnews.com with ['college compass'](https://www.usnews.com/usnews/store/college_compass?src=web:col_compass:na:BC_homepage_headerpromo_CTA:20190418) subscriptions ($40 cost)
  - [ASC](https://professionals.collegeboard.org/higher-ed/recruitment/annual-survey) (Annual survey of colleges) contains CDS questions - can request ASC data access via [this form](https://collegeboard.tfaforms.net/69)
- government - http://nces.ed.gov/
  - [x] need an account? created - https://nces.ed.gov/datalab/
  - IPEDS - https://nces.ed.gov/ipeds/use-the-data
    - full data sets - https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx?gotoReportId=7&fromIpeds=true - data is by year for each category (it may be possible to derive patterns in file naming and automate downloads for many years)
  - tables were extracted frome existing papers and repserent summary statistics
  - can also run a powerstats analysis but this also doesn't give access to source data
  - https://nces.ed.gov/datalab/table/library - downloaded a few samples to see if they could be parsed

## data commentary
Much of the avaialble data is pre-summarized rather than source data.  Many resources have their own data analytics sites allowing for basic analysis on the data without downloading the full data set.  Much of the NCES data was in the form of papers with tables extracted for further use, but the raw source data was not accessible. Kaggle datasets mostly algined with expectations, but sources might be users themselves, or the data was older.  For example, the board of education  scorecard data was a few years older than the version available on the data.gov site.  Some sites had the option to contact them for specific data, but the forms for this would often fail if did not cite the intituation you were working for.  

## data prep
  - nulls
  - scale/standardize features?
  - nlp

## EDA data.gov - scorecard 
Scorecard data was relatively recent (Aug 2021) and had a large number of measures and data back through year 1996.  There was ~ 30 files contained in a zip archive, which we can access directly using python's zipfile package in the standard library. Files were generally split by academic year and there were 2 major categories: Field of Study, and all data elements; thse columns were confirmed to match through the files sets.  There was also a crosswalks.zip subfolder that contained excel files for each year for the purpose of matching POEID to IPEDS for each institution, and giving high level information regarding those data sources and how it changed from the prior year.  Metedata for the main set of files was in a yaml file, so I wrote some python code to parse the relevent details into python dictionaries.  I also created a sqlite DB to hold data so that it would not have to be re-loaded.
Data imports were challeged by mxed data types, several institutions opted to not report certain metrics for privacy reasons and the corresponding data elements were replaced with a text string 'Privacy Suppressed' it what would otherwise be a numeric column.  For the purposes of this analysis I replaced these fields with a -1 in the csv text to allow the data files to successfully load.  This allowed me to count the number of privacy suppressed items if that became necessary.  When summarizing the numeric columns it was necessary to replace the -1 with a null so that the calculations would not be skewed by the special numeric data marker.  
Other issues were encounted loading th data into the sqlite database.  The all data elements dataset had around 3500 columns, which exceeded the default 2000 column limit for this database type. `The default setting for SQLITE_MAX_COLUMN is 2000` (https://sqlite.org/limits.html) The workaround for this was to split the columns and laod that data as 2 separate tables.  the overall size of the database on disk was ~5GB.  

Unfortunately, while I found several cases where the prevalence of lending correlated with expectations regarding degree popularity (e.g. Law for Harvard and Yale), I found several instances where there was no significant correlation (e.g. Princeton).  In the interest of time I elected to forego degree popularity as a factor for the initial runs and use all degrees offered at each institution to determine similarity.

## Analysis

To get groupings of similar universities, I elected to use clustering of the degree offerings.  As the degree listing was a categorical dataset I used on-hot encoding to transpose the the row features into numeric columns that could be fed into a clustering algorithm.  Similar universities should be spatially close in the hyperplane defined by the data features, spherical clusters are expected.  Agglomerative clustering was chosen as a first approach to minimize distance between cluster members.  The n-clusters hyperparameter was then tuned to minimize clusters with a very large number of elements and also minimize clusters with only a single member.  The linkage type was also varied to determine best results.  Selections were for 75 clusters and using ward linkage for the 7643 colleges.  This yielded ~700 colleges that were similar to our target college, TCNJ.

The cluster analysis also served as a dimensionality reduction because we could reduce the size of the large dataset to only the data for the 700 institutions that were identified as similar to our target(members of the same cluster).  The resulting dataset had 95% fewer rows than the full dataset, allowing for much quicker metric calculation for subsequent analysis.  Since I was running out of time to demonstrate a result, I elected to go with a relatively simplistic comparison of financial aspects, graduate earnings and graduate debt.  Since recent news has focused on the increasing cost of higher education I felt that these financial aspects could be key differentiating factors for students when choosing an institution to attend.


## Results

First I looked at which colleges in the similar set yielded the highest earnings for their graduates.  The dataset contained several earnings metric, so I chose the median earnings two years after graduation (`EARN_MDN_HI_2YR`).  My experience after college was to take a retail job immediately after graduation, while I looked for something more suited to my education.  If this experience is common then a graduate might not be in their desired field within the first year.  Top earners from our pool of schools were from Trevecca Nazarene, Teachers College at Columbia and Antioch University PhD program.  I then compared these summary metrics to the average for top schools (95th percentile), and the overall average.  In this case TCNJ earnings were 1% higher than the average top school, and 33% higher than the average similar school.

![image](https://user-images.githubusercontent.com/51385580/155896566-5454833e-2d78-405a-ab5c-2275cc547cd8.png)

I then looked at which colleges in the similar set resulted in the least amount of debt for their graduates.  there were fewer metrics that tracked debt to choose from.  I selected the Median Stafford and Grad PLUS loan debt disbursed (DEBT_ALL_STGP_EVAL_MDN). There are other debt avenues outside that are not captured here, but hopefully students pursue Federal offerings prior to looking higher interest options.  Least debt school examples were Texas A&M (San Antonio), Unviersidad del Sagrado Corazon, and Wester Governors University.  TCNJ debt was compared with highest debt schools (95th percentile) as well as the overall average for similar schools.  We found that debt was 40% lower than the schools with high debt graduate,s, and 10% below the overall average.  Albizu University (Miami) debt was significantly higher than the next highest college, suggesting this may be an outlier or bad data.

![image](https://user-images.githubusercontent.com/51385580/155896557-dbf31f30-00df-47d0-b9bb-282cbca6c4eb.png)

I modified the visualizations in an attempt to emphasize certain data and tell the story that our target school is better than similar alternatives.  This might be a good opportunity to play with plotly dash to create interactive visualizations and group them together in a way that could be used for a powerpoint presentation or a marketing page on a web site.  

## Improvements

Looking back at the analysis there a few areas that could be improved and extended and I hope to explore these in the near future.  Foremost we could add additional features to the clustering to enhance the cluster analysis.  Tuition, housing, and book costs might be interesting to include, as would locality and campus size.  We could also explore additional clustering algorithms like DBSCAN or Spectral clustering to see if they result in an improved model.  A tree-based algorithm might have better explainability if we need to reinforce the results. We should also validate the quality of the clustering with silhouette plots, cluster cohesion and separation.  We could also implement a gridsearch of hyperparameters to find the optimal settings for each algorithm. Analytics of the similar schools could also be extended to answer additional questions: e.g. how does our target school compare with respect to transfers in vs out; how many students enroll but don't graduate, and what are the most diverse degree types (by gender).  

A lot of my time was spent identifying a data source to use and cleaning up the data.  This is a known time sink in data science from the texts I have read.   I have not worked with higher education data in the past, so someone that already works for a college or university could have probably accomplished the same analysis much more quickly leveraging their domain expertise.  A repeat of this analysis, or a similar one, would also be faster because much of the code from this project can be re-used to load and clean the data.  The knowledge I obtained on available data and how it can be leveraged will be extremely useful when I have a child exploring higher education options.  



<pre>data specs 'all data fields':
'pandas.core.frame.DataFrame'
Int64Index: 176720 entries, 0 to 6693
Columns: **2393** entries, UNITID to filename
dtypes: float64(647), int64(6), **object(1740)**
memory usage: 3.2+ GB</pre>

<pre>
class 'pandas.core.frame.DataFrame'>
Int64Index: 954880 entries, 0 to 260530
Data columns (total 93 columns)
dtypes: float64(3), int64(4), object(86)
memory usage: 684.8+ MB
</pre>
![image](https://user-images.githubusercontent.com/51385580/151902970-f50f0f32-f339-470c-be5a-e4567e97eeeb.png)


The large size of the datset was prohibitive for exploring the data so a single file was used to determine what measures might be of value.  Field of Study metrics contained more detailed information about each degree on offer at the institution with summary metrics around earnings and DEBT withing each.  The data labeled as 'all data sets' or 'MERGED' had a more diverse set of features but data was at the instituion level rather than for each degree.  Based on the field of study information it seemed possible to develop a profile for each school based on the degrees that were most taken at that institution (e.g. Law degrees at Harvard imply it should be compared to other schools that favor Law).  

- what measures are available
  - what are their dat types
- what should be the target variable


## analysis options
- what category of models should we run


## tools
- Tableau - https://public.tableau.com/en-us/s/
- python
  - sklearn
  - keras (simple neural network)
  - what visualization types?
- neo4j


## tasks
- [x] git repos
- [x] data directory (ignoredir)
  - [x] download data sets
  - [x] merge data categories
- [x] exploration ipynb
- [x] py module - to eliminate clutter


## lessons learned
- large datset options
  - dask
  - online learning
  - read from csv as needed Apache drill
  - data segmentation tool
  - spark
  - gitlab
