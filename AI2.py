import streamlit as st
import pandas as pd
from scipy.optimize import linear_sum_assignment as linear_assignment
from sklearn.ensemble import RandomForestClassifier
pd.options.display.float_format = "{:,.2f}".format
# Import train_test_split function
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
In the left side (if using mobil, please press on the **black arrow**) you should fill in your personal data\n
After filling in and pressing "done", your predicted party will be shown in the middle of the screen! (scroll down a little bit to see the party's name)\n
If you would like to know what was the odds for the app to predict different party press on "Prediction Probability", which is below your prediction\n\n
The **privacy policy** is written at the bottom of the page and we encourage you to read it!
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
    gender = st.sidebar.selectbox('1. Gender', tuple(gender_dict.keys()))
    age = st.sidebar.number_input('2. Age', 18, 120)
    living = st.sidebar.selectbox('3. Where do you live?', tuple(living_dict.keys()))
    type_living = st.sidebar.selectbox('4. What kind of settlement do you live in?', tuple(type_living_dict.keys()))
    rooms = st.sidebar.number_input('5. Number of rooms in the house', 1, 20)
    education = st.sidebar.selectbox('6. What is your education?', tuple(education_dict.keys()))
    salary = st.sidebar.selectbox('7. What is your salary?', tuple(salary_dict.keys()))
    family_status = st.sidebar.selectbox('8. What is your family status?', tuple(family_stat_dict.keys()))
    kids = st.sidebar.number_input('9. Number of kids', 0, 20)
    religion = st.sidebar.selectbox('10. What religion do you believe in?', tuple(religion_dict.keys()))
    believe = st.sidebar.selectbox('11. How much do you believe in your religion?', tuple(believe_dict.keys()))
    important = st.sidebar.selectbox('12. What is the most important topic?', tuple(important_dict.keys()))
    left_right = st.sidebar.slider('13. Rank yourself on the political map - 0 = most Left, 100 = Most right', 0, 100, 50)

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


###### show ########

st.sidebar.error("By pressing 'Done and proceed', you confirm the use of your personal data")
if st.sidebar.button("Done and proceed"):
    st.sidebar.write("Your preferences are now set!")
    st.sidebar.write("**if you are using mobile phone - scroll back up and press the X**")


# Show user input
st.subheader('Your Input parameters (expand to see fully)')
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

####### Statistics and plotting #######
st.write("""
# Some Data Statistics""")
if st.checkbox('Press to extend the Statistics'):

    st.write("""
    1. Corelation matrix between all parameters""")
    corrMatrix = parties2.corr()
    fig2, ax2 = plt.subplots()
    sns.heatmap(corrMatrix,  square=True,
            linewidths=0.1, annot=True, annot_kws={"size":5}, ax=ax2)
    st.pyplot(fig2)

    #st.write(parties2.describe())
    st.write("""
    2. Some statistical polts:""")
    # plotting
    fig3, axes = plt.subplots(1,3, figsize=(10, 4))
    axes[0].set_title('Distribution by religion')
    sns.histplot(ax=axes[0], x=parties['religion'],color='teal')
    axes[1].set_title('Distribution by age')
    sns.histplot(ax=axes[1], x=parties['age'],color='tan')
    axes[2].set_title('Distribution by gender')
    sns.histplot(ax=axes[2], x=parties['gender'],color='pink')
    st.pyplot(fig3)

    # plotting 2
    fig4, axes = plt.subplots(1,2, figsize=(10, 4))
    axes[0].set_title('Distribution by believe')
    ax0 = sns.histplot(ax=axes[0], x=parties['believe'],color='azure')
    plt.setp(ax0.get_xticklabels(), rotation=45)
    axes[1].set_title('Distribution by most important topic')
    sns.histplot(ax=axes[1], x=parties['important'],color='lightcoral')
    plt.xticks(rotation=30)
    st.pyplot(fig4)

    # plotting 3
    plot_left_right = parties['left_right']
    fig5, ax11 = plt.subplots()
    ax11.set_title('Distribution of the right or left wing preferences')
    ax11 = sns.kdeplot(data=plot_left_right,cut=0)
    ax11.set(xlabel='Left or Right wing', ylabel='Probability')
    fig5.set_figwidth(7.27)
    fig5.set_figheight(2.7)
    st.pyplot(fig5)

## spaces
st.text("")
st.text("-----------------------------------------------------------------------------------------")
st.text("-----------------------------------------------------------------------------------------")
st.text("-----------------------------------------------------------------------------------------")
st.text("")
## spaces


## Model Accuracy, how often is the classifier correct?
## lst = []
## for i in range (1,30):
##     test = (100-i)/100
##     X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test)
##     clf = RandomForestClassifier(n_estimators=100)
##     clf.fit(X_train, Y_train)
##     Y_pred = clf.predict(X_test)
##     lst.append(metrics.accuracy_score(Y_test, Y_pred))
## st.write(lst)
##
## st.subheader('How accurate is this prediction is going to be?')
## st.write(round(metrics.accuracy_score(Y_test, Y_pred),2))

st.write("""
# Discussion""")
if st.checkbox('    Press to extend the discussion'):

    st.markdown("<p style='text-align: right;'>בפרוייקט שלנו ביצענו סקר עליו ענו כ-300 אנשים על מנת להתחיל ולכתוב תוכנה שממליצה לאזרח הפשוט לאחר מענה על מספר שאלות, לאיזו מפלגה להצביע</p>",
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: right;'>"
                """
                הרשומות שקיבלנו אינן מתפלגות נורמלית, אין מספר שווה או לפחות קרוב מכל סוג רשומה, דבר שעלול ליצור *הטיה* בתוצאות שכן אלגוריתם הלמידה שלנו רואה יותר דוגמאות מסוג אחד ופחות מסוג אחר, ביחס להתפלגות האמיתית באוכלוסייה
לדוגמה, 90% מהעונים על הסקר היו יהודים (בעוד שמספר היהודים באוכלוסייה הינו נע בין 70 ל75 אחוז, ראינו פרק סטטיסטיקה באתר זה)                
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
                מכיוון שכמות הנתונים שהצלחנו לאסוף יחסית קטנה, השתמשנו באלגוריתם שנקרא ״יער אקראי״ שמספק לנו תוצאות טובות (נבדק על כמות של כ-100 איש, מתוכם לכ-90% המערכת המליצה את המפלגה שהם באמת מתכננים להצביע עבורה)
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
                יער אקראי, בהגדרה, כפי ששמו מרמז עליו, מורכב מעצי החלטה.
העצים נוצרים לרוב על ידי דגימה מתוך המאפיינים או מתוך התצפיות.                 
                כל אחד מהעצים נותן תוצאה לא-אופטימאלית אך באופן כללי, על פי רוב, החיזוי בדרך זו משתפר
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
בהנחה והיו לנו מאות אלפי רשומות היינו משתמשים באלגוריתמי למידה עמוקה ורשתות נוירונים               
                """
                "</p>", unsafe_allow_html=True)


## spaces
st.text("")
st.text("-----------------------------------------------------------------------------------------")
st.text("-----------------------------------------------------------------------------------------")
st.text("-----------------------------------------------------------------------------------------")
st.text("")
## spaces

st.write("""
# Privacy Policy""")
if st.checkbox('Press to extend the Privacy Policy'):
    st.write("## Disclaimer")
    st.markdown("<p style='text-align: right;'>"
                """
אין בתוכן זה כוונה לפגוע במזיד או בשוגג במשתמשי התוכן. אם נוצרה פגיעה בעת מילוי השאלון, או כתוצאה מתוצאות האלגוריתם, אנו מביעים את התנצלותנו הכנה. נשמח לשמוע חוות דעת ולשפר את האלגוריתם בכל עת, לפי הצעות המשתמשים                 
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: right;'>"
                """
כללי                
                """
                "</h2>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
מדיניות זו נועדה על מנת להסביר למשתמש איזה מידע אנו אוספים, מדוע אנו אוספים אותו וכיצד ניתן לעדכן, לנהל, לייצא ולמחוק את המידע               
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו שואפים ליצור טכנולוגיה שפותרת בעיות חשובות ועוזרת לאנשים לכוון את רצונם בבחירות. אנו אופטימיים לגבי הפוטנציאל המדהים של בינה מלאכותית וטכנולוגיות מתקדמות אחרות ולכן אנו סבורים כי עם מתן המידע, ישנה תרומה גדולה של הפרט כחלק מהחברה
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו מאמינים כי טכנולוגיה זו תקדם חדשנות ותקדם את המשימה שלנו לארגן את המידע במדינה ולהפוך אותו לנגיש ושימושי ציבורי
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו מכירים בכך שהטכנולוגיה מעלה אתגרים חשובים שעלינו להתמודד עימם ולעמוד בפניהם באופן ברור, מתחשב ואחראי. עקרונות אלה קובעים את המחויבות שלנו לפתח טכנולוגיה באחריות ולהקים תחומי יישום ספציפיים
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: right;'>"
                """
הגנה על הציבור               
                """
                "</h2>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו משתמשים במידע כדי לשפר את הדיוק והאמינות של השירותים שלנו 
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו משתמשים בחישוב אלגוריתמי כדי לספק תוצאות חיפוש מותאמות אישית. אנו משתמשים גם באלגוריתמים כדי לזהות דפוסים בנתונים
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו נבקש את הסכמתך לפני השימוש במידע שלך למטרה שאינה מכוסה במדיניות פרטיות זו
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: right;'>"
                """
סוג המידע הנאסף               
                """
                "</h2>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: right;'>"
                """
מידע הנאסף באופן ישיר               
                """
                "</h4>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
מידע ותוכן המסופק על-ידי המשתמש - אנו אוספים את התוכן, והנתונים המוזנים על ידי המשתמש בעת מילוי השאלות שלנו. מידע זה יכול לכלול נתונים כגון מין, גיל, דת וכו'. המערכות שלנו מעבדות באופן אוטומטי תוכן ותקשורת המסופקת תוך ביצוע ניתוחים מתקדמים
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
נתונים עם הגנות מיוחדות: כלל המידע המסופק בתחומי השאלות באתר הקשור למידע אישי והשקפות המשתמש. מידע זה ומידע אחר (כגון מוצא גזעי או אתני, אמונות) עשויים להיות כפופים להגנות מיוחדות על פי חוקי המדינה.
הנתונים נמצאם תחת אחריות האתר, ואנו מתחייבים כי יהיו חסויים, ולא נגישים לגורמים חיצוניים אשר מעוניינים לבצע בהם שימוש, ללא אישור מראש של המשתמש
                """
                "</p>", unsafe_allow_html=True)


    st.markdown("<h4 style='text-align: right;'>"
                """
                 מידע הנאסף באופן בלתי ישיר – מהשרות של המשתמש
                """
                "</h4>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
בנוסף למידע הנאסף באופן ישיר, תוכן אותו המשתמש ממלא, אנו אוספים מידע בלתי ישיר.
המידע שאנו אוספים כולל מזהים ייחודיים. כמו כן, אנו אוספים מידע אודות האינטראקציה של האתר, כולל כתובת IP, תאריך, שעה והמפנה של בקשת המשתמש
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו אוספים מידע זה כאשר שירות האתר במכשיר יוצר קשר עם השרתים שלנו - לדוגמה, בעת מילוי השאלון או כאשר השירות בודק אם קיימים עדכונים אוטומטיים
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: right;'>"
                """
שימוש בנתונים
                """
                "</h2>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: right;'>"
                """
                אנו משתמשים בנתונים כדי לבנות שירות הכוונה טוב יותר
                """
                "</h4>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
:אנו משתמשים במידע שאנו אוספים מהשאלונים שלנו למטרות הבאות
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו משתמשים במידע המסופק על-ידי המשתמש למטרת אתר זה, ניתוח העדפות המשתמש בבחירת מפלגה
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו גם משתמשים במידע כדי להבטיח שהשירות שלנו פועל באופן הוגן ורצוי, כגון מעקב אחר הטיות של המערכת או פתרון בעיות מדווחות. כמו כן, אנו משתמשים במידע כדי לבצע שיפורים בשירותים שלנו
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: right;'>"
                """
מתן שירותים מותאמים אישית
                """
                "</h4>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו משתמשים במידע שאנו אוספים כדי להתאים אישית את השירותים שלנו עבור המשתמש, כולל מתן המלצות, תוכן מותאם אישית ותוצאות חיפוש מותאמות אישית
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<h4 style='text-align: right;'>"
                """
מדידת ביצועים
                """
                "</h4>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו משתמשים בנתונים לניתוח ומדידה כדי להבין כיצד להכווין את המשתמשים שלנו. לדוגמה, אנו מנתחים נתונים על השאלון שלך באתר שלנו כדי לבצע פעולות של טיוב הכוונה
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: right;'>"
                """
העברות נתונים 
                """
                "</h2>", unsafe_allow_html=True)


    st.markdown("<p style='text-align: right;'>"
                """
המידע שלך מעובד בשרתים הממוקמים במדינות ישראל ובארה"ב. חלה הגנה חוקתית מכוח המדינה.
אין בכוונתו הישירה לעשות שימוש והעברת נתונים אל שרתים אחרים ו/או אל חברות אחרות. במידה ונרצה להעביר את הנתונים, נידרש להסכמתו המפורשת של המשתמש
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: right;'>"
                """
מחיקת נתונים
                """
                "</h2>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אין באפשרותנו למחוק נתונים המתקבלים מהמשתמש באופן אוטומטי.
אם משתמש מעוניין במחיקת נתוניו מן השרות, עליו לפנות אל שירות התמיכה של האתר
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: right;'>"
                """
אבטחת הנתונים
                """
                "</h2>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
התוכן של המשתמש מאובטח באתרנו.
אתרנו משתמש בפלטפורמת "סטרימליט" היושבת על שרתי "גיט-האב" אשר מאובטחים בתקנון האבטחה של האתרים והשרתים הללו.
אנו נפעל נמרצות לשמור על אבטחת המידע של המשתמש הכולל הצפנת המידע, אחסונו בשרתים מאובטחים, והרשאות גישה מנוהלות למידע.
באופן יזום, נבצע ביקורות פתע על מנת לזהות פרצות אבטחה וגישה בלתי הולמת לנתונים.
אנו מתחייבים לשמור על נתוני המשתמש דיסקרטיים ככל הניתן
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: right;'>"
                """
סיבות משפטיות
                """
                "</h2>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
אנו נשתף מידע אישי מחוץ ל- לאתר אם אנו מאמינים בתום לב כי גישה, שימוש, שימור או גילוי של המידע נחוצים באופן סביר למקרים הבאים
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: center;'>"
                """
הליך משפטי או בקשה ממשלתית הניתנת לאכיפה
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: center;'>"
                """
מניעת בעיות הונאה, אבטחה או בעיות טכניות
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: center;'>"
                """
הגנה מפגיע בזכויות
                """
                "</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: right;'>"
                """
כאשר אנו מקבלים תלונות רשמיות בכתב, אנו מגיבים על ידי יצירת קשר עם האדם שהגיש את התלונה
                """
                "</p>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: right;'>"
                """
מדיניות פרטיות זו אינה חלה על
                """
                "</h2>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: right;'>"
                """
נוהלי המידע של חברות וארגונים אחרים המפרסמים את השירותים שלנו.
שירותים המוצעים על ידי חברות או אנשים אחרים או אתרים שעשויים לכלול שירותי הכוונה, או יקשרו אותם מהשירותים שלנו
                """
                "</p>", unsafe_allow_html=True)