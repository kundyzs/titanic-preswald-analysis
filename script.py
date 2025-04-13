from preswald import connect, get_df, text, table, slider, plotly
import plotly.express as px

# Initialize and load data
connect()
df = get_df("titanic")

# Data cleaning
initial_count = len(df)
df = df.dropna(subset=['Age', 'Fare'])  # Remove rows with missing Age or Fare
cleaned_count = len(df)

# Basic UI
text("# Titanic Passenger Analysis")
text("Explore survival rates by different factors")

# Show data cleaning info
text(f"*Analyzing {cleaned_count} passengers ({initial_count-cleaned_count} removed due to missing data)*")

# Show age range
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
text(f"### Passenger ages range from **{min_age}** to **{max_age}** years old")

# Interactive Age Filter
text("## Interactive Filter")
age_threshold = slider("Minimum Age", min_val=0, max_val=80, default=18)
filtered_df = df[df['Age'] > age_threshold]
table(filtered_df.head(20), title=f"First 20 Passengers Older Than {age_threshold}")

# Visualizations
text("## Survival Analysis")

# Survival by class and gender
text("### Survival by Passenger Class")
fig1 = px.bar(df, x='Pclass', y='Survived', color='Sex', barmode='group',
             title="Survival Rate by Class and Gender",
             labels={'Pclass': 'Passenger Class', 'Survived': 'Survival Rate'})
fig1.update_layout(
    yaxis_title="Survival Rate (%)",
    xaxis_title="Passenger Class"
)
plotly(fig1)

# Age distribution
text("### Age Distribution")
fig2 = px.histogram(df, x='Age', color='Survived', nbins=20,
                   title="Age Distribution by Survival Status",
                   labels={'Age': 'Age (years)', 'count': 'Number of Passengers'},
                   barmode='overlay', opacity=0.7)
fig2.update_layout(
    yaxis_title="Number of Passengers",
    margin=dict(l=50, r=50, t=50, b=50)
)
plotly(fig2)

from preswald import query

# SQL-like query example
text("## First Class Passengers Who Survived")
sql = """
SELECT Name, Age, Sex, Fare 
FROM titanic 
WHERE Pclass = 1 AND Survived = 1
ORDER BY Fare DESC
LIMIT 10
"""
first_class_survivors = query(sql, "titanic")
table(first_class_survivors, title="Top 10 First Class Survivors by Fare Paid")