# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 16:48:39 2018

@author: Amin
"""

# import

import glob
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from sklearn.decomposition import TruncatedSVD # PCA used for sparce matrices
from sklearn.cluster import KMeans # used for clustering
from sklearn.pipeline import make_pipeline #developing a pipeline for our fit transform
import pandas as pd

# function definition
def book_importer(file_name): # to import the books as a text file
    with open(file_name, 'r', encoding="utf8") as myfile:
        line = myfile.read().replace('\t', ' ').replace('\n', ' ').replace(",","").replace(":","").replace("ۀ","ه").replace("-","").replace("،","")
        line = re.sub("\d|[a-z]|\.","",line) # removing numbers
    return line

# Importing all the poet books into a list
pattern = 'poets/*.txt'
poet_files = glob.glob(pattern)

poet_labels_persian = ['ابوسعید ابوالخیر', 'امیر معظی'
                       , 'انوری', 'عارف قزوینی', 'اسعد گرگانی', 'اسدی توسی', 'عطار نیشابوری',
 'ارزقی', 'بابافاضل', 'بباطاهر', 'شیخ بهایی', 'ملک الشعرای بهار', 'بیدل دهلوی', 'ابن حسام',
 'عراقی', 'فرخی', 'فایز', 'فردوسی', 'فیض کاشانی', 'فروغی', 'قاآنی', 'گیلانی', 'حافظ', 'هاتف اصفهانی',
 'هلالی', 'هجویری', 'اقبال لاهوری', 'جبلی', 'جامی', 'کمال اسماعیل', 'کسایی', 'خاقانی', 'خاجوی کرمانی',
 'خلیلی کرمانی', 'خیام', 'امیرخسرو', 'مهستی', 'منوچهری', 'مسعود سعد', 'میبدی', 'محتشم', 'نصرالله منشی',
 'مولوی', 'ناصر خسرو', 'نظامی گنجوی', 'نزاری قهستانی', 'عبید زاکانی', 'عمان سامانی', 'عنصری', 'عرفی',
 'اوحدی', 'پروین اعتصامی', 'رهی معیری', 'آرتیمانی', 'رودکی', 'سعدی', 'صائب', 'سلمان', 'سنایی',
 'سیف فرغانی', 'شبستری', 'شاه نعمت الله', 'شهریار', 'عباس صبوحی', 'وحشی بافقی', 'وراوینی', 'وطواط',
 'ظهیر']

# Getting all documents into a list
documents = []
for poet in poet_files:
    documents.append(book_importer(poet))
# tfidf
tfidf = TfidfVectorizer()
csr_mat = tfidf.fit_transform(documents)

#developing a pipeline
svd = TruncatedSVD(n_components=1)#25)
kmeans = KMeans(n_clusters=2)#4)
pipeline = make_pipeline(svd, kmeans)


# fitting the pipeline
pipeline.fit(csr_mat)
labels = pipeline.predict(csr_mat) #Generating the labels for each class

# cluster labels
#df = pd.DataFrame({'label': labels, 'poets': poet_labels_persian})

# Display df sorted by cluster label
#print(df.sort_values(by='label'))