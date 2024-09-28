<script lang="ts">
    import { createClient } from "@supabase/supabase-js";
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import ConversationComponent from "$lib/ConversationComponent.svelte";
    import type { Database } from "$lib/supabase-types";
    import { fetchRandomConversation } from "$lib";

    export let data;

    let supabase = data.supabase

    let conversation = null;

    async function fetchConversation(id) {
        const [{ data: bridge }, { data: convos }, { data: responses }] =
            await Promise.all([
                supabase
                    .from("bridge")
                    .select("*")
                    .eq("conversation_id", id)
                    .single(),
                supabase
                    .from("bridge_convo")
                    .select("*")
                    .eq("conversation_id", id),
                supabase
                    .from("bridge_response")
                    .select("*")
                    .eq("conversation_id", id),
            ]);

        conversation = {
            ...bridge,
            convos: convos || [],
            responses: responses || [],
        };
    }

    async function getNextRandomUnratedConversation() {
    if (!confirm("Are you sure? You won't be able to change your answers after this.")) {
        return;
    }

    try {
        console.log("Fetching unrated conversations...");
        
        const user = $page.data.session?.user;
        
        if (!user) goto('/auth')
        const conversationId = await fetchRandomConversation(supabase, user!)
        if (conversationId !== null) {
            goto(`/private/conversation/${conversationId}`)
        }
        
    } catch (error) {
        console.error("Error in getNextRandomUnratedConversation:", error);
        alert("An error occurred while fetching the next conversation.");
    }
}

    function goToHome() {
        goto("/");
    }

    // This reactive statement will re-run whenever the page.params.id changes
    $: {
        if ($page.params.id) {
            fetchConversation($page.params.id);
        }
    }

    onMount(() => {
        if ($page.params.id) {
            fetchConversation($page.params.id);
        }
    });
</script>


<div class="container">
    {#if conversation}
        <ConversationComponent {conversation} />
    {:else}
        <p class="loading">Loading conversation...</p>
    {/if}

    <div class="navigation">
        <button on:click={goToHome} class="nav-button">Back to home</button>
        <button on:click={getNextRandomUnratedConversation} class="nav-button"
            >Next random unrated conversation</button
        >
    </div>
</div>

<style>
    .container {
        max-width: 800px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
        padding: 20px;
    }

    .loading {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin: 20px 0;
    }

    .navigation {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }

    .nav-button {
        background-color: #427afd;
        border: none;
        color: white;
        padding: 10px 15px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 10px;
        transition:
            background-color 0.3s,
            color 0.3s;
    }

    .nav-button:hover {
        background-color: #3062d7;
    
    }

    .nav-button:active {
        background-color: #1849ba;
    }
</style>
