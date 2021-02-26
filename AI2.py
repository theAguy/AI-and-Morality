import streamlit as st
import pandas as pd
#from scipy.optimize import linear_sum_assignment as linear_assignment
from sklearn.ensemble import RandomForestClassifier
pd.options.display.float_format = "{:,.2f}".format
# # Import train_test_split function
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns


# import image to top of the page
st.image("https://kanstatic.azureedge.net/download/pictures/2020/12/28/imgid=44378_X.jpeg")

# set the title and description
st.write("""
# Parties Prediction App
This app predicts the **party** you should vote for!\n
More explanation is needed here.........................
""")

## spaces
st.text("")
st.text("-----------------------------------------------------------------------------------------")
st.text("-----------------------------------------------------------------------------------------")
st.text("-----------------------------------------------------------------------------------------")
## spaces

#set side bar header
st.sidebar.header('User Input Parameters')


############ settings ####################

# creating the user's input interface
def user_input_features():
    gender = st.sidebar.selectbox('Gender', tuple(gender_dict.keys()))
    age = st.sidebar.slider('Age', 18, 120,40)
    living = st.sidebar.selectbox('Where do you live?', tuple(living_dict.keys()))
    type_living = st.sidebar.selectbox('What kind of settlement do you live in?', tuple(type_living_dict.keys()))
    rooms = st.sidebar.slider('Number of rooms in the house', 1, 10, 3)
    education = st.sidebar.selectbox('What is your education?', tuple(education_dict.keys()))
    salary = st.sidebar.selectbox('What is your salary?', tuple(salary_dict.keys()))
    family_status = st.sidebar.selectbox('What is your family status?', tuple(family_stat_dict.keys()))
    kids = st.sidebar.slider('Number of kids', 0, 20, 0)
    religion = st.sidebar.selectbox('What religion do you believe in?', tuple(religion_dict.keys()))
    believe = st.sidebar.selectbox('How much do you believe in your religion?', tuple(believe_dict.keys()))
    important = st.sidebar.selectbox('What is the most important topic?', tuple(important_dict.keys()))
    left_right = st.sidebar.slider('Rank yourself on the political map - 0 = most Left, 100 = Most right', 0, 100, 50)

    data = {'gender': gender,
            'age': age,
            'living': living,
            'type_living':type_living,
            'rooms': rooms,
            'education': education,
            'salary': salary,
            'family_status':family_status,
            'kids': kids,
            'religion': religion,
            'believe': believe,
            'important': important,
            'left_right': left_right}
    features = pd.DataFrame(data, index=[0])
    return features


## Dictionaries of the question in the questionnaire
gender_dict = {'Man': 0,
            'Woman': 1,
            'Other': 2}

living_dict = {'North': 0,
            'Haifa': 1,
            'Center': 2,
            'Tel Aviv': 3,
            'Jerusalem':4,
            'South':5,
            'Yehuda Ve Shomron' : 6,
            'Out of Israel': 7}

type_living_dict = {'City': 0,
            'Yeshuv': 1,
            'Moshav': 2,
            'Kibutz': 3,
            'Kefar':4,
            'Other':5}

education_dict = {'None': 0,
            'High school': 1,
            'Graduate High school': 2,
            'First degree': 3,
            'Second degree': 4,
            'Third degree and above':5,
            'Other':6}

salary_dict = {'less then 5K': 0,
            '5K-10K': 1,
            '10K-15K': 2,
            '15K-20K': 3,
            '20K-25K':4,
            '25K+':5,
            'Unemployed' : 6,
            'Other': 7}

family_stat_dict = {'Single': 0,
            'Married': 1,
            'Divorced': 2,
            'Widowed': 3,
            'Other':4}

religion_dict = {'Jewish': 0,
            'Muslim': 1,
            'Christian': 2,
            'Druze': 3,
            'Other':4}

believe_dict = {'Very religious': 0,
            'religious': 1,
            'observant': 2,
            'secular': 3,
            'atheist': 4,
            'Other':5}

important_dict = {'Economy': 0,
            'Security': 1,
            'Social equality': 2,
            'Culture': 3,
            'Health':4}

class_dict = {'Likud': 0,
            'Yesh Atid': 1,
            'Tikva Hadasha': 2,
            'Yamina': 3,
            'Hareshima Hameshutefet':4,
            'Kahol Lavan':5,
            'Haavoda' : 6,
            'Shas': 7,
            'Yahadut Hatora': 8,
            'Israel Beitenu': 9,
            'Hatsionut Hadatit': 10,
            'Merets':11,
            'Raam':12,
            'Hakalkalit Hahadasha': 13,
            'Other': 14}

parties_pictures = {0 : 'https://www.idi.org.il/media/5955/likud.jpg?mode=crop&width=259&height=169',
            1 : 'https://shkifut.info/wp-content/uploads/2018/07/%D7%9C%D7%95%D7%92%D7%95-%D7%99%D7%A9-%D7%A2%D7%AA%D7%99%D7%93-1210x423.jpg',
            2 : 'https://www.newhope.org.il/wp-content/uploads/2020/12/SSB-logo-pos.png',
            3 : 'https://www.idi.org.il/media/13891/yamina.jpg?mode=crop&width=259&height=169',
            4 : 'https://www.idi.org.il/media/13893/joint-arab-list.jpg?mode=crop&width=259&height=169',
            5 : 'https://www.idi.org.il/media/13890/blue-white.jpg?mode=crop&width=259&height=169',
            6 : 'https://havoda.org.il/wp-content/uploads/2019/01/logo-havoda.png',
            7 : 'https://upload.wikimedia.org/wikipedia/he/thumb/0/05/Shas_logo.svg/1200px-Shas_logo.svg.png',
            8 : 'https://upload.wikimedia.org/wikipedia/he/thumb/9/97/%D7%99%D7%94%D7%93%D7%95%D7%AA_%D7%94%D7%AA%D7%95%D7%A8%D7%94_%D7%9C%D7%95%D7%92%D7%95_2019.svg/1200px-%D7%99%D7%94%D7%93%D7%95%D7%AA_%D7%94%D7%AA%D7%95%D7%A8%D7%94_%D7%9C%D7%95%D7%92%D7%95_2019.svg.png',
            9 : 'https://www.idi.org.il/media/13919/israel-beitenu.jpg?mode=crop&width=259&height=169',
            10 : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEUqB9yPogF6HbKR_fYEQoI5Q20pdqiKg-hA&usqp=CAU',
            11 : 'https://upload.wikimedia.org/wikipedia/he/thumb/6/67/Meretz_Logo.svg/1200px-Meretz_Logo.svg.png',
            12 : 'https://upload.wikimedia.org/wikipedia/he/1/1a/%D7%9C%D7%95%D7%92%D7%95_%D7%A8%D7%A2%22%D7%9D-%D7%91%D7%9C%22%D7%93_2019.png',
            13 : 'https://upload.wikimedia.org/wikipedia/he/thumb/c/c9/%D7%94%D7%9E%D7%A4%D7%9C%D7%92%D7%94_%D7%94%D7%9B%D7%9C%D7%9B%D7%9C%D7%99%D7%AA_%D7%94%D7%97%D7%93%D7%A9%D7%94_%D7%9C%D7%95%D7%92%D7%95.svg/640px-%D7%94%D7%9E%D7%A4%D7%9C%D7%92%D7%94_%D7%94%D7%9B%D7%9C%D7%9B%D7%9C%D7%99%D7%AA_%D7%94%D7%97%D7%93%D7%A9%D7%94_%D7%9C%D7%95%D7%92%D7%95.svg.png',
            14 : 'https://images.globes.co.il/images/NewGlobes/big_image_800/2019/800x392.2019410T124656.jpg'}

########### preparing the data to analysis #############

## Importing the questionnaire answers
parties = pd.read_csv('parties.csv')

## convert the questionnaire answers to the dictionaries categories
parties2 = parties.copy()
parties2 = parties2.replace({"gender": gender_dict})
parties2 = parties2.replace({"living": living_dict})
parties2 = parties2.replace({"type_living": type_living_dict})
parties2 = parties2.replace({"education": education_dict})
parties2 = parties2.replace({"salary": salary_dict})
parties2 = parties2.replace({"family_status": family_stat_dict})
parties2 = parties2.replace({"religion": religion_dict})
parties2 = parties2.replace({"believe": believe_dict})
parties2 = parties2.replace({"important": important_dict})
parties2 = parties2.replace({"class": class_dict})


## printing the user's set of parameters he chose
df = user_input_features()

## replacing the user's input to categories according to dictionaries
df2 = df.copy()
df2 = df2.replace({"gender": gender_dict})
df2 = df2.replace({"living": living_dict})
df2 = df2.replace({"type_living": type_living_dict})
df2 = df2.replace({"education": education_dict})
df2 = df2.replace({"salary": salary_dict})
df2 = df2.replace({"family_status": family_stat_dict})
df2 = df2.replace({"religion": religion_dict})
df2 = df2.replace({"believe": believe_dict})
df2 = df2.replace({"important": important_dict})
df2 = df2.replace({"class": class_dict})

features_names = ['gender','age','living','type_living','rooms',
                    'education','salary','family_status','kids',
                    'religion','believe','important','left_right']

######## predicting #########
X = parties2.loc[:,features_names]
Y = parties2.loc[:,'class']
Y=Y.astype('int')

my_dict2 = {y:x for x,y in class_dict.items()}
parties_names = pd.DataFrame.from_dict(my_dict2,orient='index')

# Split dataset into training set and test set
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1) # 70% training and 30% test

#Create a Gaussian Classifier
clf = RandomForestClassifier(n_estimators=100)

#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(X_train,Y_train)
Y_pred=clf.predict(X_test)

#all the data using for prediction
# clf.fit(X, Y)

# predict given user input

index_to_name = ['Likud', 'Yesh Atid', 'Tikva Hadasha', 'Yamina', 'Hareshima Hameshutefet', 'Kahol Lavan', 'Haavoda',
                 'Shas', 'Yahadut Hatora', 'Israel Beitenu', 'Hatsionut Hadatit', 'Merets', 'Raam', 'Hakalkalit Hahadasha']
prediction = clf.predict(df2)
prediction_proba = clf.predict_proba(df2)
prediction_proba = prediction_proba.transpose()
prediction_proba = pd.DataFrame(prediction_proba,columns=['probability'], index=index_to_name)


####### show ########

# Show user input
st.subheader('User Input parameters (expand to see fully)')
st.write(df)

## spaces
st.text("")
st.text("-----------------------------------------------------------------------------------------")
st.text("")
## spaces

# st.subheader('Class labels and their corresponding index number')
# st.write(parties_names)

st.subheader('Party prediction')
# st.write(prediction)
st.image(parties_pictures.get(prediction[0]))
st.subheader('Prediction Probability')
if st.checkbox('Show Prediction probability per party'):
    st.write(prediction_proba)

## spaces
st.text("")
st.text("-----------------------------------------------------------------------------------------")
st.text("")
## spaces

st.subheader('Most impact parameters')
feature_imp = pd.Series(clf.feature_importances_,index=features_names).sort_values(ascending=False)
fig, ax = plt.subplots()
sns.barplot(x=feature_imp, y=feature_imp.index, ax=ax)
if st.checkbox('Show impact parameters strength in numbers'):
    st.write(feature_imp)
st.pyplot(fig)

## spaces
st.text("")
st.text("-----------------------------------------------------------------------------------------")
st.text("-----------------------------------------------------------------------------------------")
st.text("")
st.text("")
## spaces

st.write("""
# Prediction satisfaction
Are you satisfied from the prediction?\n
This is your opportunity to help us to improve it!\n
Please choose, on scale from 0 to 100, how accurate was our prediction.\n
It will help us improve the algorithm and get better!
""")
st.slider('How much do you satisfy from the prediction?', 0, 100, 100)

## spaces
st.text("")
st.text("-----------------------------------------------------------------------------------------")
st.text("-----------------------------------------------------------------------------------------")
st.text("-----------------------------------------------------------------------------------------")
st.text("")
## spaces

st.write("""
# Some Data Statistics""")

corrMatrix = parties2.corr()
fig2, ax2 = plt.subplots()
sns.heatmap(corrMatrix,  square=True,
        linewidths=0.1, annot=True, annot_kws={"size":5}, ax=ax2)
st.pyplot(fig2)

st.write(parties2.describe())

# relegion plot
fig3, axes = plt.subplots(1,3, figsize=(17, 7))
axes[0].set_title('Distribution by religion')
sns.histplot(ax=axes[0], x=parties['religion'])
axes[1].set_title('Distribution by age')
sns.histplot(ax=axes[1], x=parties['age'])
sns.lineplot(ax=axes[2], x=parties['left_right'], y=parties['left_right'].count())
st.pyplot(fig3)



## spaces
st.text("")
st.text("-----------------------------------------------------------------------------------------")
st.text("-----------------------------------------------------------------------------------------")
st.text("-----------------------------------------------------------------------------------------")
st.text("")
## spaces


st.write("""
# Discussion""")

# Model Accuracy, how often is the classifier correct?
st.subheader('How accurate is this prediction is going to be?')
st.write(round(metrics.accuracy_score(Y_test, Y_pred),2))
