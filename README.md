# Fake-Rental-Listing-Identification
This is the repository for Fake Housing Rental Info Identification(FRLI 假房源识别) made by Eden, Xinyao, and Yile  

## Proposal
Nowadays, when many people choose to rent houses, most of them will first search through the Internet. They prefer to select their desired houses through online pictures first, and then inspect real houses / to save efforts. In China, the top online housing platforms are 58, Anjuke, ziroom and Beike(贝壳). Most of the listing information is equipped with pictures of the houses and other basics. Online housing rental seem to bring huge convenience to people’s life, while problems such as online fake renting are common.  
  
Widely reported by official China media such as People’s Daily, ChinaNews, CTV News, online rental scams are so common / that around 80% of the people encountered fake houses when renting. They lost huge amouts of money because landlords conceal major defects in housing and the prices are opaque. As indicated by south China news survey, major problems are excessively beautified pictures, faking detailed information of houses as well as attracting people with false low price.  
  
Currently, there’s no existing solutions to this problem. Chinese government has issued plans on regulation policies and provided some suggestions on distinguishing fake houses. Comparing the average prices of identical houses and paying attention to textual descriptions are two solutions. While these methods takes huge work and are usually biased with subjective illustrations on information.  
  
Hence we are going to make a solution with systematic, unbiased machine learning methods, and trying to give the tenants an intuitive judgement of the reliability of rental sources.  

## Our Plan
Our project is going to have 3 steps: Firstly, collect as much datas as possible, since a larger dataset can give us more systematical prediction. The datas are collected from rental webpages by web crawlers. We’ve already made some gradual progresses crawling from Ziroom, Beike, 58.com, Anjuke, and get a 20k dataset. Then we are going to add true/false tags to some of them.  
  
The next step is going to be modeling, we’ve already implement linear regression and batch gradient descent to our simple model which predict reasonable rental price using floor, area, and numbers of rooms. We will try to implement more complex methods in the future such as Polynomial Regression and Neuron Network. We’ll also use Naive Bayes for fitting different tags into prediction model.  
  
Accompanied with modeling is training model with our datasets. Since our model and datasets will be updated constantly with training outputs, those three step will cycling simultaneously. Hopefully, after several loops, we will have a steady prediction model which output a percentile of how likely a rental information is fake.  
  
## Progresses
* Using xpath and BeautifulSoup, we are able to get a 20k dataset with different infos.
* Since some rental webpages using encryption methods to protect their price and other important infos, we also managed to cross that obstacle using decipher methods.
* In order to make the data coming handily, we standardized them with standard format and datatypes.  
* Trained a simple model using Linear Regression to predicting the housing price using bedroom, livingroom, area, and floor. This is based on Linear Regression and get a quite good result after training. We believe we can prove it with more complex methodology and datas. Here's what we got:  
![alt text](https://github.com/EdenWuyifan/Fake-Rental-Listing-Identification/blob/main/pics/problem3.png?raw=true)

  
## Dificulties
* One problem we faced when crawling for Ziroom dataset is that the price is directly crop out of one randomly generated picture. So we used BeautifulSoup to get that image from web sources. Then we use Tesseract to recognize the number orders.  
![alt text](https://github.com/EdenWuyifan/Fake-Rental-Listing-Identification/blob/main/pics/problem1.png?raw=true)
* Anjuke and 58 encrypted the numbers as some Chinese characters. We get its real-time key in its js fangchan-secret function, then refer it to the glyph dictionary to find the number with same suffix, we can substitute the Chinese character with the proper number.  
![alt text](https://github.com/EdenWuyifan/Fake-Rental-Listing-Identification/blob/main/pics/problem2.png?raw=true)

