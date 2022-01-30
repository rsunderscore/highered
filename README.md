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

## EDA
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
  - [x] download common data set
  - [ ] download other data sets?
- [ ] exploration ipynb
- [ ] pyth9on module
