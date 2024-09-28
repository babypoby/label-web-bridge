<script lang="ts">
    import { createClient } from "@supabase/supabase-js";
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import type { Database } from "$lib/supabase-types";
    import { fetchRandomConversation } from "$lib";

    export let data;

    let eligibleConversations = [];
    let conversation_id = null;

    async function fetchData() {
        const user = $page.data.session?.user;
        data.supabase
        conversation_id = await fetchRandomConversation(data.supabase, user)
    }

    onMount(() => {
        fetchData();
    });
</script>

<main>
    <h1>Conversation Data</h1>
    {#if conversation_id}
        <nav>
            <a
                href={`/private/conversation/${conversation_id}`}
            >
                Go to random unrated conversation
            </a>
        </nav>
    {:else if eligibleConversations.length === 0}
        <p>Loading data...</p>
    {:else}
        <p>No eligible conversations available.</p>
    {/if}
</main>

<style>
    nav {
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;
    }
    nav a {
        margin-bottom: 10px;
    }
</style>
