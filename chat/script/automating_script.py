#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import pandas as pd
import asyncio
import nest_asyncio
from chatgpt import generate_response_langchat
import openai

#%%

openai.api_key = "YOUR_OPENAI_API_KEY"

#%%

df = pd.read_csv("data/filtered_MSRBot_dataset.csv")

data = df[['Project', 'User Query']].dropna()

#%%
nest_asyncio.apply()

#%%
df_copy = data.copy()

#%%
project_urls = {
    "Hibernate": "https://github.com/hibernate/hibernate-orm",
    "Kafka": "https://github.com/apache/kafka"
}

#%%
async def apply_func(row):
    user_input = row['User Query']
    url = project_urls[row['Project']]
    response, sources = await generate_response_langchat(user_input, openai.api_key, url)
    docs = [doc.page_content for doc in sources]
    return response, docs

#%%
df_copy['Response'], df_copy['Sources'] = zip(*df_copy.apply(lambda row: asyncio.run(apply_func(row)), axis=1))

#%%
df_copy.to_csv("data/responses_sources.csv")

# %%
