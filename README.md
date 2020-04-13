# ControversialTweetAnalysis
Analysis of controversial tweets
This project also introduces [a lexicon](./Final%20Lexicons/URL_CATEGORIES.tsv) which can be used to classify the URL into the following categories: 

| Type​ 	| Counts​ 	| Description​ 	| Example​ 	|
|:--------------|--------:|:----------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|
| Blog​ 	| 194​ 	| All blogging platforms indexed in Wikidata​ 	| wordpress.com​ 	|
| Commercial​ 	| 55​ 	| All commercial websites indexed in Wikidata​ 	| amazon.com​ 	|
| Fake news​ 	| 518​ 	| 1) A list developed by Melissa Zimdars and her research team at Merrimack College<br/>​2) A list of fake news websites from Wikipedia<br/>​3) FakeNewsChecker​   	| naturalnews.com​ 	|
| News​ 	| 1,988​ 	| 1) News sources indexed by Wikidata<br/>​2) List of trusted news domains created by Facebook ​  	| nytimes.com​ 	|
| Scientific​ 	| 2,962​ 	| All scientific publishers indexed by Wikidata​ 	| springer.com​ 	|
| Social media​ 	| 87​ 	| All social media domains indexed by Wikidata​ 	| facebook.com​ 	|
| Twitter​ 	| 1​ 	| Links to other tweets, twitter hosted images, videos​ 	| twitter.com​ 	|
| Videos​ 	| 13​ 	| All video sharing services from Wikipedia​ 	| vimeo.com​ 	|

[Click to access the URL categorization lexicon](./Final%20Lexicons/URL_CATEGORIES.tsv). 

## Citation

If you are using this lexicon please cite the following papers:

> Addawood, A., Rezapour, R., Mishra, S., Schneider, J., & Diesner, J. (2017). Developing an Information Source Lexicon. In NIPS workshop on Prioritising Online Content. Retrieved from https://www.k4all.org/wp-content/uploads/2017/09/WPOC2017_paper_8.pdf

```latex
@inproceedings{addawood2017,
  title = {Developing an Information Source Lexicon},
  author = {Addawood, Aseel and Rezapour, Rezvaneh and Mishra, Shubhanshu and Schneider, Jodi and Diesner, Jana},
  year = {2017},
  booktitle = {NIPS workshop on Prioritising Online Content},
  url = {https://www.k4all.org/wp-content/uploads/2017/09/WPOC2017_paper_8.pdf}
}
```


## Process URLs

* Extract urls using `Merge URLs and tweets.ipynb`
* Fix expanded URLs using `Fix expanded URL errors.ipynb`
* Process URL categories using `Process URL categories.ipynb`
* Fix files which don't have parallel structure using `Fix vaccine files.ipynb`
* Merge URLs using `Merge URLs and tweets.ipynb`
* Run `Prepare analysis data.ipynb` by uncommenting the Location blog

## Contributors:
* [Shubhanshu Mishra](https://github.com/napsternxg)
* [Aseel Addawood](https://github.com/aseelad)
* Shadi Rezapour


