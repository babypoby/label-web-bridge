import os
import json
import asyncio
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

async def update_data(table, data):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: supabase.table(table).upsert(data).execute())

async def main():
    entries_to_update = []
    processed_ids = set()
    update_count = 0

    with open('train.jsonl', 'r') as file:
        for line in file:
            data = json.loads(line)
            qid = data['qid']
            scenario = data['scenario']
            conversation_id = f"{qid}_{scenario}"
            
            if conversation_id not in processed_ids:
                update_count += 1
                entries_to_update.append({
                    "conversation_id": conversation_id,
                    "question": data.get('question', ''),
                    "solution": data.get('ground_truth', '')
                })
                processed_ids.add(conversation_id)

    print(f"Entries to be updated: {update_count}")

    if entries_to_update:
        try:
            response = await update_data("bridge_copy", entries_to_update)
            print(f"Updated {len(entries_to_update)} entries in bridge_copy table.")
        except Exception as e:
            print(f"An error occurred while updating: {str(e)}")
    else:
        print("No entries to update.")

if __name__ == "__main__":
    asyncio.run(main())
