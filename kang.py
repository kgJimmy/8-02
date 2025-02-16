from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd


#df=pd.read_csv("C:\Users\AISW\Desktop\kangjim\fruit_vegetable.csv",encoding="utf-8")
df = pd.read_csv(r"C:\Users\AISW\Desktop\kangjim\fruit_vegetable.csv",encoding="utf-8")

wc=df.set_index("title").to_dict()["count"]

#words = {
 #   'HYUNDAI': 4,
  #  'KIA': 2,
   # 'Nike': 1,
    #'Samsung': 5,
   # 'LG': 3,
   # 'SK': 4,
    #'KwangWoon': 1,
    #'AI': 3,
    #'Volvo': 2,
    #'Korea': 3,
    #'Jeju': 3,
    #'Canada': 2,
    #'Paris': 3,
    #'Olympics': 2,
    #'Ios-18': 5,
    #'iphone': 2,
    #'Apple': 3,
    #'ipad': 4,
    #'FIBA': 2,
    #'FIFA': 3,
    #'EPL': 5,
    #'Son': 3,
    #'kane': 2,
    #'LeBron': 5,
    #'Jordan': 3,
    #'Luka': 2,
    #'Wemdy': 3,
    #'Curry': 1,
    #'cho': 1,
    #'kang': 2,
    #'Lee': 6,
    #'Nam': 1,
    #'football': 3,
    #'basketball': 2,
    #'volyball': 3,
    #'head': 4,
    #'leg': 3,
    #'hand': 2,
    #'foot': 1,
    #'sibal': 2
#}

#img_mask=np.array(Image.open('heart.png'))
img=Image.open('C:\\Users\\AISW\\Desktop\\kangjim\\fuckyou.jpg')
img_array=np.array(img)
wordcloud = WordCloud(
    #font_path = 'C:\\WINDOWS\\FONTS\\ARLRDBD.TTF',
    font_path = 'malgun',
    background_color = 'white',
    colormap='Greens_r',
    mask=img_array,
).generate_from_frequencies(wc)


plt.figure(figsize=(3,3))
plt.axis('off')
plt.imshow(wordcloud,interpolation='bilinear')
plt.show()