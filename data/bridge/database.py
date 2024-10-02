import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# Fetch existing conversation IDs from the database
existing_ids_response = supabase.table("bridge").select("conversation_id").execute()
existing_ids = set(item['conversation_id'] for item in existing_ids_response.data)
print(f"Existing IDs in bridge table: {len(existing_ids)}")

# Read the JSONL file
entries_bridge = []
entries_bridge_convo = []
seen_conversation_ids = set()
count = 0

with open('your_file.jsonl', 'r') as file:
    for line in file:
        data = json.loads(line)
        qid = data['qid']
        
        if qid not in existing_ids and qid not in seen_conversation_ids:
            count += 1
            # Add entry for bridge table
            entries_bridge.append({"conversation_id": qid})
            
            # Process conversation for bridge_convo table
            conversation = data['conversation']
            parts = conversation.split("|EOM|")
            for i, part in enumerate(parts):
                part = part.strip()
                if part.startswith("Teacher:"):
                    user = "tutor"
                    text = part[8:].strip()
                elif part.startswith("Student:"):
                    user = "student"
                    text = part[8:].strip()
                else:
                    continue  # Skip if it doesn't start with Teacher or Student
                
                entries_bridge_convo.append({
                    "conversation_id": qid,
                    "id": i,  # Starting from 0 and incrementing
                    "user": user,
                    "text": text
                })
            
            seen_conversation_ids.add(qid)

print(f"New unique conversation IDs to be inserted: {count}")

# Insert the unique entries into the Supabase tables
if entries_bridge:
    try:
        # Insert into bridge table
        response_bridge = supabase.table("bridge").insert(entries_bridge).execute()
        print(f"Inserted {len(entries_bridge)} new unique entries into bridge table.")
        
        # Insert into bridge_convo table
        response_bridge_convo = supabase.table("bridge_convo").insert(entries_bridge_convo).execute()
        print(f"Inserted {len(entries_bridge_convo)} new entries into bridge_convo table.")
        
        # Verify the insertions
        result_bridge = supabase.table("bridge").select("conversation_id").execute()
        result_bridge_convo = supabase.table("bridge_convo").select("conversation_id, id").execute()
        
        if hasattr(result_bridge, 'data') and hasattr(result_bridge_convo, 'data'):
            result_ids_bridge = set(item['conversation_id'] for item in result_bridge.data)
            result_ids_bridge_convo = set(item['conversation_id'] for item in result_bridge_convo.data)
            max_id = max(item['id'] for item in result_bridge_convo.data) if result_bridge_convo.data else -1
            print(f"Total unique entries in bridge table after insertion: {len(result_ids_bridge)}")
            print(f"Total entries in bridge_convo table after insertion: {len(result_bridge_convo.data)}")
            print(f"Total unique conversation IDs in bridge_convo table after insertion: {len(result_ids_bridge_convo)}")
            print(f"Highest 'id' in bridge_convo table: {max_id}")
        else:
            print("Unexpected result structure. Cannot process conversation IDs.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
else:
    print("No new unique entries to insert.")




# After insertion
