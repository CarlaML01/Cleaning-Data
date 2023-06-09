#!/usr/bin/env python
# coding: utf-8

# ## Gather

# In[1]:


import pandas as pd


# In[2]:


patients = pd.read_csv('patients.csv')
treatments = pd.read_csv('treatments.csv')
adverse_reactions = pd.read_csv('adverse_reactions.csv')


# ## Assess

# In[3]:


patients


# In[4]:


treatments


# In[5]:


adverse_reactions


# In[6]:


patients.info()


# In[7]:


treatments.info()


# In[8]:


adverse_reactions.info()


# In[9]:


all_columns = pd.Series(list(patients) + list(treatments) + list(adverse_reactions))
all_columns[all_columns.duplicated()]


# In[10]:


list(patients)


# In[11]:


patients[patients['address'].isnull()]


# In[12]:


patients.describe()


# In[13]:


treatments.describe()


# In[14]:


patients.sample(5)


# In[15]:


patients.surname.value_counts()


# In[16]:


patients.address.value_counts()


# In[17]:


patients[patients.address.duplicated()]


# In[18]:


patients.weight.sort_values()


# In[19]:


weight_lbs = patients[patients.surname == 'Zaitseva'].weight * 2.20462
height_in = patients[patients.surname == 'Zaitseva'].height
bmi_check = 703 * weight_lbs / (height_in * height_in)
bmi_check


# In[20]:


patients[patients.surname == 'Zaitseva'].bmi


# In[21]:


sum(treatments.auralin.isnull())


# In[22]:


sum(treatments.novodra.isnull())


# #### Quality
# ##### `patients` table
# - Zip code is a float not a string
# - Zip code has four digits sometimes
# - Tim Neudorf height is 27 in instead of 72 in
# - Full state names sometimes, abbreviations other times
# - Dsvid Gustafsson
# - Missing demographic information (address - contact columns) ***(can't clean yet)***
# - Erroneous datatypes (assigned sex, state, zip_code, and birthdate columns)
# - Multiple phone number formats
# - Default John Doe data
# - Multiple records for Jakobsen, Gersten, Taylor
# - kgs instead of lbs for Zaitseva weight
# 
# ##### `treatments` table
# - Missing HbA1c changes
# - The letter 'u' in starting and ending doses for Auralin and Novodra
# - Lowercase given names and surnames
# - Missing records (280 instead of 350)
# - Erroneous datatypes (auralin and novodra columns)
# - Inaccurate HbA1c changes (leading 4s mistaken as 9s)
# - Nulls represented as dashes (-) in auralin and novodra columns
# 
# ##### `adverse_reactions` table
# - Lowercase given names and surnames

# #### Tidiness
# - Contact column in `patients` table contains two variables: phone number and email
# - Three variables in two columns in `treatments` table (treatment, start dose and end dose)
# - Adverse reaction should be part of the `treatments` table
# - Given name and surname columns in `patients` table duplicated in `treatments` and `adverse_reactions` tables

# ## Clean

# In[23]:


patients_clean = patients.copy()
treatments_clean = treatments.copy()
adverse_reactions_clean = adverse_reactions.copy()


# ### Missing Data

# #### `treatments`: Missing records (280 instead of 350)

# ##### Define
# Import the cut treatments into a DataFrame and concatenate it with the original treatments DataFrame.

# ##### Code

# In[24]:


treatments_cut = pd.read_csv('treatments_cut.csv')
treatments_clean = pd.concat([treatments_clean, treatments_cut],
                             ignore_index=True)


# ##### Test

# In[25]:


treatments_clean.head()


# In[26]:


treatments_clean.tail()


# #### `treatments`: Missing HbA1c changes and Inaccurate HbA1c changes (leading 4s mistaken as 9s)

# ##### Define
# Recalculate the `hba1c_change` column: `hba1c_start` minus `hba1c_end`. 

# ##### Code

# In[27]:


treatments_clean.hba1c_change = (treatments_clean.hba1c_start - 
                                 treatments_clean.hba1c_end)


# ##### Test

# In[28]:


treatments_clean.hba1c_change.head()

