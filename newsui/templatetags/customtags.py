import os
import pandas as pd
from django import template
from ..models import article  # Assuming article is a Django model defined elsewhere

register = template.Library()

@register.filter
def split(value, key):
    return value.split(key)

@register.filter
def replacestr(value, key):
    return value.replace(key, '_')

@register.filter
def keywordfilter(value, key):
    # Assuming newsdata.pkl is in the same directory as the Django app
    pkl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'newsdata.pkl')
    
    try:
        df = pd.read_pickle(pkl_path)
        entity_cols = ['LOC', 'ORG', 'GPE', 'PERSON', 'NORP']
        filtered_rows = df[df['Entity'].apply(lambda x: any(value in x[entity] for entity in entity_cols))]
        filtered_data = filtered_rows[['Heading', 'Link', 'Image', 'Summary', 'Date']].copy()
        filtered_data['Summary'] = filtered_data['Summary'].apply(lambda x: x[:500])  # Truncate summary if needed
        article_list = [article(title=row['Heading'], img=row['Image'], lnk=row['Link'], summary=row['Summary'], date=row['Date']) for _, row in filtered_data.iterrows()]
        return article_list
    except FileNotFoundError:
        # Handle file not found error
        return []
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
        return []
