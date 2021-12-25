import numpy as np
from scipy import stats as st

## https://www.fixes.pub/program/670069.html?utm_source=pocket_mylist
## 上記を参考に作成
def get_slope_adjusted(df):
  df= df.dropna()
  min_date= df.index.min()
  x= (df.index -min_date)
  y= np.array(df)
  slope, intercept, r_value, p_value, std_err= st.linregress(x,y)
  return slope