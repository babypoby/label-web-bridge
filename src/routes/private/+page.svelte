<script lang="ts">
    import { createClient } from "@supabase/supabase-js";
    import { onMount } from "svelte";
    import { page } from "$app/stores";

    const supabase = createClient(
        "https://jryeokpjkidbgzscmrcj.supabase.co",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpyeWVva3Bqa2lkYmd6c2NtcmNqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU5ODQ3NjIsImV4cCI6MjA0MTU2MDc2Mn0.nLeYIrrnbkSVqKeY7XOZkgHxDYwDcQOSVwmzrZgQrMo",
    );

    let eligibleConversations = [];
    let randomConversation = null;

    async function fetchData() {
    const user = $page.data.session.user;

    try {
        // Step 1: Get all conversations from the bridge table
        const { data: allConversations, error: bridgeError } = await supabase
            .from('bridge')
            .select('conversation_id');

        if (bridgeError) throw bridgeError;

        // Step 2: Get all ratings
        const { data: allRatings, error: ratingError } = await supabase
            .from('rating')
            .select('conversation_id, user_id');

        if (ratingError) throw ratingError;

        // Process the data
        const userRatedSet = new Set(allRatings
            .filter(r => r.user_id === user.id)
            .map(r => r.conversation_id));

        const ratingCountMap = allRatings.reduce((acc, r) => {
            acc[r.conversation_id] = (acc[r.conversation_id] || 0) + 1;
            return acc;
        }, {});

        eligibleConversations = allConversations
            .filter(conv => {
                const ratingCount = ratingCountMap[conv.conversation_id] || 0;
                return !userRatedSet.has(conv.conversation_id) && ratingCount < 3;
            });

        selectRandomConversation();
    } catch (error) {
        console.error("Error fetching conversations:", error);
    }
}



    function selectRandomConversation() {
        if (eligibleConversations.length > 0) {
            const randomIndex = Math.floor(Math.random() * eligibleConversations.length);
            randomConversation = eligibleConversations[randomIndex];
        } else {
            console.log("No eligible conversations found");
            randomConversation = null;
        }
    }

    onMount(() => {
        fetchData();
    });
</script>

<main>
    <h1>Conversation Data</h1>
    {#if randomConversation}
        <nav>
            <a href={`/private/conversation/${randomConversation.conversation_id}`}>
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
