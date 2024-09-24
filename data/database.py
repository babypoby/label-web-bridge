import os
from supabase import create_client, Client
import json
from dotenv import load_dotenv

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# Fetch existing conversation IDs from the database
existing_ids_response = supabase.table("bridge_response").select("conversation_id").execute()
existing_ids = set(item['conversation_id'] for item in existing_ids_response.data)
print(f"Existing IDs: {len(existing_ids)}")

# Read the JSON file
with open('bridge/test_edited.json', 'r') as file:
    json_data = json.load(file)

# Initialize an empty list to store the entries
entries = []
seen_conversation_ids = set()
count = 0

# Iterate through the JSON data and create entries
for item in json_data:
    conversation_id = item.get("conversation_id")
    if conversation_id not in existing_ids and conversation_id not in seen_conversation_ids:
        count += 1
        last_index = item.get("conversation_history")[-1].get("id")
        for turn in item.get("conversation_response"):
            if (turn.get("id")):
                 entry = {
                "conversation_id": conversation_id,
                "id": turn.get("id"),
                "text": turn.get("text"),
                "user": turn.get("user")
                }
            else: 
                last_index = last_index+1
                entry = {
                "conversation_id": conversation_id,
                "id": last_index,
                "text": turn.get("text"),
                "user": turn.get("user")
                }

           
            entries.append(entry)
        seen_conversation_ids.add(conversation_id)

local_unique_ids = set(item['conversation_id'] for item in entries)
print(f"Unique conversation IDs to be inserted: {len(local_unique_ids)}")

# Insert the unique entries into the Supabase table
if entries:
    try:
        response = supabase.table("bridge_response").insert(entries).execute()
        print(f"Inserted {len(entries)} new unique entries.")
        
        result = supabase.table("bridge_response").select("conversation_id").execute()

        
        if hasattr(result, 'data'):
            result_ids = set(item['conversation_id'] for item in result.data)
            print(f"Total unique entries after insertion: {len(result.data)}")
            print(f"Total unique conversation IDs after insertion: {len(result_ids)}")
    
        else:
            print("Unexpected result structure. Cannot process conversation IDs.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
else:
    print("No new unique entries to insert.")



# After insertion
