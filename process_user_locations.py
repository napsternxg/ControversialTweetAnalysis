# coding: utf-8
import sys
TWEET_USER_GEOLOCATION_PATH="/home/entity/Code/twitter-user-geocoder"
sys.path.append(TWEET_USER_GEOLOCATION_PATH)

import pandas as pd
from tweet_us_state_geocoder import TweetUSStateGeocoder

USER_LOC_FILE="USER_LOCATIONS.txt"
print("Processing user location using TweetUSStateGeocoder from %s" % TWEET_USER_GEOLOCATION_PATH)
df = pd.read_csv(USER_LOC_FILE, header=None, sep="\t")
df.columns = ["location", "user_counts"]
tug = TweetUSStateGeocoder()
print("Processing %s locations"  % df.shape[0])

PROCESSING_ERRORS=0
def tug_get_state(x):
    global PROCESSING_ERRORS
    try:
        return tug.get_state(x)
    except UnicodeDecodeError:
        PROCESSING_ERRORS += 1
        return None


df["parsed_state"] = df.location.apply(tug_get_state)
print("Finished with %s UnicodeDecodeError" % PROCESSING_ERRORS)
print("Saving to PARSED_STATES.txt")
df.to_csv("PARSED_STATES.txt", sep="\t", index=False, encoding='utf-8')
print(df.shape)


## Add manual processing
df = pd.read_csv("PARSED_STATES.txt", sep="\t")
df.parsed_state = df.parsed_state.str.upper()
df_states = pd.read_csv("US_STATES.txt", sep="\t")
print("Read states data with shape: ", df_states.shape)
df_cities = pd.read_json("us.cities.json", orient="records")
df_cities["state"] = df_cities.state.str.upper()
print("Read cities data with shape: ", df_cities.shape)

# In[3]:
STATE_NAMES = dict(zip(df_states["State Name"].values.tolist(), df_states["Abbreviation"].values.tolist()))
STATE_CAPITALS = dict(zip(df_states["Capital"].values.tolist(), df_states["Abbreviation"].values.tolist()))
CITY_STATES = dict(zip(df_cities["city"].values.tolist(), df_cities["state"].values.tolist()))
STATE_ABBR = set(df_states["Abbreviation"].values.tolist())
STATE_ABBR.update(["USA"])

EXTRA_CITY_STATE_MAPPING = pd.read_csv("EXTRA_CITY_STATE_MAPPING.txt", sep="\t", header=None, index_col=0)
print("Loaded extra city state mappings from EXTRA_CITY_STATE_MAPPING.txt", EXTRA_CITY_STATE_MAPPING.shape)
CITY_STATES.update(EXTRA_CITY_STATE_MAPPING[1].to_dict())

def get_state_from_text(x):
    if x.upper() in STATE_ABBR:
        return x.upper()
    for k, v in STATE_NAMES.items():
        if k.lower() in x.lower():
            return v
    for k, v in STATE_CAPITALS.items():
        if k.lower() in x.lower():
            return v
    for k, v in CITY_STATES.items():
        if k.lower() in x.lower():
            return v
    for k in x.upper().split():
        k = k.replace(".", "")
        if k in STATE_ABBR:
            return k
    return None

def get_state(x):
    x = x.replace(".", "").strip()
    x_state = x.rsplit(",", 1)
    if len(x_state) < 2:
        return get_state_from_text(x)
    x_state = x_state[-1].strip().upper()
    if len(x_state) == 2:
        if x_state in STATE_ABBR:
            return x_state
    return get_state_from_text(x)


df["parse_manual"] = df.location.apply(lambda x: get_state(x))
print("Locations with no states: ")
print(df[df.parse_manual.isnull()].shape)
print(df[df.parse_manual.isnull()].head(10))

print("Users covered by locations with mapped state: ", df[~df.parse_manual.isnull()].user_counts.sum())
print("Users covered by locations without mapped state: ", df[df.parse_manual.isnull()].user_counts.sum())
print("Coverage of users with mapped state: ", df[~df.parse_manual.isnull()].user_counts.sum() / df.user_counts.sum())


# In[13]:

print("Locations with parsed_state but not parsed_manual: ", df[(df.parse_manual.isnull()) & (~df.parsed_state.isnull())].shape)
print(df[(df.parse_manual.isnull()) & (~df.parsed_state.isnull())].head())

# In[14]:
print("Mapping states from parsed_state to parse_manual")
df.ix[(df.parse_manual.isnull()) & (~df.parsed_state.isnull()), "parse_manual"] = df.ix[
    (df.parse_manual.isnull()) & (~df.parsed_state.isnull()), "parsed_state"]
df.head()

# In[15]:

print("Proportion of users geolocated: %s" % (df[~df.parse_manual.isnull()].user_counts.sum() * 1./df.user_counts.sum()))
print("Users covered by locations with mapped state: ", df[~df.parse_manual.isnull()].user_counts.sum())


# In[18]:
print("Writing to PARSED_STATES.final.txt")
df.to_csv("PARSED_STATES.final.txt", sep="\t", index=False, encoding="utf-8")
