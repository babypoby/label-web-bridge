// place files you want to import through the `$lib` alias in this folder.

import type { SupabaseClient, User } from "@supabase/supabase-js";
import type { Database } from "./supabase-types";


export async function fetchRandomConversation(supabase: SupabaseClient<Database>, user: User) {
    const { data }  = await supabase.rpc("get_random_conversation", { in_user_id: user.id }).throwOnError()
    return data
}