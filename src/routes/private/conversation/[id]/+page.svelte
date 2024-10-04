<script lang="ts">
    import { createClient } from "@supabase/supabase-js";
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import ConversationComponent from "$lib/ConversationComponent.svelte";
    import type { Database } from "$lib/supabase-types";
    import { fetchRandomConversation } from "$lib";
    import ProgressBar from "$lib/ProgressBar.svelte";

    export let data;

    let supabase = data.supabase;

    let conversation = null;
    let ratedConversations = 0;
    let loading = true;

    async function fetchConversation(id) {
        loading = true;
        try {
            const [{ data: bridge_filtered }, { data: convos }, { data: responses }] =
                await Promise.all([
                    supabase
                        .from("bridge_filtered")
                        .select("*")
                        .eq("conversation_id", id)
                        .limit(1)
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
                ...bridge_filtered,
                convos: convos || [],
                responses: responses || [],
            };
        } catch (error) {
            console.error("Error fetching conversation:", error);
        } finally {
            loading = false;
        }
    }

    async function getNextRandomUnratedConversation() {
        if (!confirm("Are you sure? You won't be able to change your answers after this.")) {
            return;
        }

        try {
            console.log("Fetching unrated conversations...");
            
            const user = $page.data.session?.user;
            
            if (!user) goto('/auth');
            const conversationId = await fetchRandomConversation(supabase, user!);
            if (conversationId !== null) {
                goto(`/private/conversation/${conversationId}`);
            }
            
        } catch (error) {
            console.error("Error in getNextRandomUnratedConversation:", error);
            alert("An error occurred while fetching the next conversation.");
        }
    }

    function goToHome() {
        goto("/");
    }

    async function fetchRatedConversationsCount() {
        const user = $page.data.session?.user;
        if (!user) return;

        const { count, error } = await supabase
            .from("rating")
            .select("*", { count: "exact", head: true })
            .eq("user_id", user.id);

        if (error) {
            console.error("Error fetching rated conversations count:", error);
        } else {
            ratedConversations = count || 0;
        }
    }

    async function initializeData() {
        await fetchRatedConversationsCount();
        if ($page.params.id) {
            await fetchConversation($page.params.id);
        }
    }

    onMount(() => {
        initializeData();
    });

    $: if ($page.params.id) {
        fetchConversation($page.params.id);
    }
</script>

<div class="container">
    <ProgressBar current={ratedConversations} />

    {#if loading}
        <p class="loading">Loading conversation...</p>
    {:else if conversation}
        <ConversationComponent {conversation} />
    {:else}
        <p class="loading">No conversation available.</p>
    {/if}

    <div class="navigation">
        <button on:click={goToHome} class="nav-button">Back to home</button>
        <button on:click={getNextRandomUnratedConversation} class="nav-button">
            Next random unrated conversation
        </button>
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
