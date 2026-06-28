import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
 
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
 
df = pd.read_csv('RuralCreditData.csv')
print(f"Total Rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
 
df.dropna(inplace=True)
print(f"Cleaned Rows: {len(df)}")
 
text_cols = ['city', 'sex', 'social_class', 'primary_business',
             'secondary_business', 'home_ownership',
             'type_of_house', 'sanitary_availability',
             'water_availabity', 'loan_purpose']
 
for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.title()
 
df['monthly_income'] = df['annual_income'] / 12
df['monthly_savings'] = df['monthly_income'] - df['monthly_expenses']
df['total_dependents'] = df['old_dependents'] + df['young_dependents']
df['loan_burden_%'] = (df['loan_installments'] / df['monthly_income']) * 100
 
def risk(x):
    if x > 40:
        return 'High Risk'
    elif x > 20:
        return 'Medium Risk'
    else:
        return 'Low Risk'
 
df['risk_level'] = df['loan_burden_%'].apply(risk)
 
print("\nRisk Level Count:")
print(df['risk_level'].value_counts())
 
q1 = df.groupby('city')['loan_burden_%'].mean().sort_values(ascending=False).head(10)
print("\nQ1 - Top 10 Cities by Loan Burden %:")
print(q1)
 
q2 = df.groupby('loan_purpose')['loan_amount'].mean().sort_values(ascending=False).head(8)
print("\nQ2 - Top 8 Loan Purposes by Amount:")
print(q2)
 
q3 = df.groupby('social_class')['loan_amount'].mean().sort_values(ascending=False).head(8)
print("\nQ3 - Top 8 Social Classes by Loan Amount:")
print(q3)
 
q4 = df.groupby('home_ownership')['loan_amount'].mean().sort_values(ascending=False)
print("\nQ4 - Loan Amount by Home Ownership:")
print(q4)
 
q5 = df.groupby('sex')['loan_amount'].mean().sort_values(ascending=False)
print("\nQ5 - Loan Amount by Gender:")
print(q5)
 
fig, axes = plt.subplots(2, 3, figsize=(22, 12))
fig.suptitle('Rural India — Agriculture Loan Risk Analysis Dashboard',
             fontsize=18, fontweight='bold', y=1.01, color='#2C3E50')
fig.patch.set_facecolor('#F8F9FA')
 
colors_bar = ['#E74C3C','#E67E22','#F1C40F','#2ECC71',
              '#1ABC9C','#3498DB','#9B59B6','#E91E63','#FF5722','#607D8B']
 
# Chart 1 — Top 10 Cities by Loan Burden %
bars1 = axes[0,0].bar(q1.index, q1.values, color=colors_bar[:len(q1)], edgecolor='white', linewidth=0.8)
axes[0,0].set_title('Top 10 Cities by Loan Burden %', fontweight='bold', fontsize=11, pad=10)
axes[0,0].set_xlabel('City', fontsize=9)
axes[0,0].set_ylabel('Avg Loan Burden %', fontsize=9)
axes[0,0].set_xticklabels(q1.index, rotation=35, ha='right', fontsize=8)
axes[0,0].set_facecolor('#FDFEFE')
for bar in bars1:
    axes[0,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                   f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=7, fontweight='bold')
 
# Chart 2 — Top 8 Loan Purposes
bars2 = axes[0,1].barh(q2.index, q2.values, color='#3498DB', edgecolor='white', linewidth=0.8)
axes[0,1].set_title('Top 8 Loan Purposes by Amount', fontweight='bold', fontsize=11, pad=10)
axes[0,1].set_xlabel('Average Loan Amount (₹)', fontsize=9)
axes[0,1].set_yticklabels(q2.index, fontsize=8)
axes[0,1].set_facecolor('#FDFEFE')
axes[0,1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
 
# Chart 3 — Top 8 Social Classes
bars3 = axes[0,2].barh(q3.index, q3.values, color='#2ECC71', edgecolor='white', linewidth=0.8)
axes[0,2].set_title('Top 8 Social Classes by Loan Amount', fontweight='bold', fontsize=11, pad=10)
axes[0,2].set_xlabel('Average Loan Amount (₹)', fontsize=9)
axes[0,2].set_yticklabels(q3.index, fontsize=8)
axes[0,2].set_facecolor('#FDFEFE')
axes[0,2].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
 
# Chart 4 — Risk Level Pie
colors_pie = ['#E74C3C', '#F39C12', '#27AE60']
risk_counts = df['risk_level'].value_counts()
wedges, texts, autotexts = axes[1,0].pie(
    risk_counts.values,
    labels=risk_counts.index,
    autopct='%1.1f%%',
    colors=colors_pie,
    startangle=90,
    pctdistance=0.75,
    wedgeprops=dict(edgecolor='white', linewidth=2)
)
for text in texts:
    text.set_fontsize(10)
for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_fontweight('bold')
axes[1,0].set_title('Risk Level Distribution', fontweight='bold', fontsize=11, pad=10)
 
# Chart 5 — Home Ownership vs Loan Amount
bars5 = axes[1,1].bar(q4.index, q4.values,
                      color=['#9B59B6','#8E44AD','#6C3483'],
                      edgecolor='white', linewidth=0.8)
axes[1,1].set_title('Loan Amount by Home Ownership', fontweight='bold', fontsize=11, pad=10)
axes[1,1].set_xlabel('Home Ownership', fontsize=9)
axes[1,1].set_ylabel('Average Loan Amount (₹)', fontsize=9)
axes[1,1].set_xticklabels(q4.index, rotation=20, ha='right', fontsize=9)
axes[1,1].set_facecolor('#FDFEFE')
axes[1,1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
for bar in bars5:
    axes[1,1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                   f'₹{bar.get_height()/1000:.1f}K', ha='center', va='bottom', fontsize=8, fontweight='bold')
 
# Chart 6 — Annual Income vs Loan Amount Scatter
scatter = axes[1,2].scatter(
    df['annual_income'], df['loan_amount'],
    alpha=0.3, c=df['loan_burden_%'], cmap='RdYlGn_r',
    s=15, edgecolors='none'
)
plt.colorbar(scatter, ax=axes[1,2], label='Loan Burden %')
axes[1,2].set_title('Annual Income vs Loan Amount', fontweight='bold', fontsize=11, pad=10)
axes[1,2].set_xlabel('Annual Income (₹)', fontsize=9)
axes[1,2].set_ylabel('Loan Amount (₹)', fontsize=9)
axes[1,2].set_facecolor('#FDFEFE')
axes[1,2].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
axes[1,2].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
 
plt.tight_layout(pad=3.0)
plt.savefig('loan_charts.png', dpi=180, bbox_inches='tight', facecolor='#F8F9FA')
print("\nCharts saved as loan_charts.png")
plt.show()
 
df.to_csv('cleaned_loan_data.csv', index=False)
print("Cleaned data saved as cleaned_loan_data.csv")