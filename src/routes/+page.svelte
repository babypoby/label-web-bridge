<script lang="ts">
    import { createClient } from "@supabase/supabase-js";
    import { onMount } from "svelte";

    const supabase = createClient(
        "https://jryeokpjkidbgzscmrcj.supabase.co",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpyeWVva3Bqa2lkYmd6c2NtcmNqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU5ODQ3NjIsImV4cCI6MjA0MTU2MDc2Mn0.nLeYIrrnbkSVqKeY7XOZkgHxDYwDcQOSVwmzrZgQrMo",
    );

    let groupedData = [];
    let randomConversation = null;

    async function fetchData() {
        const { data: bridges, error: bridgeError } = await supabase
            .from("bridge")
            .select("*");

        if (bridgeError) {
            console.error("Error fetching conversations:", bridgeError);
            return;
        }

        groupedData = bridges;
        selectRandomConversation();
    }

    function selectRandomConversation() {
        if (groupedData.length > 0) {
            const unratedConversations = groupedData.filter(conv => conv.explains_concepts_0 === null && conv.identifies_goal_1 === null);
            if (unratedConversations.length > 0) {
                const randomIndex = Math.floor(Math.random() * unratedConversations.length);
                randomConversation = unratedConversations[randomIndex];
            } else {
                console.log("No unrated conversations found");
            }
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
            <a href={`/conversation/${randomConversation.conversation_id}`}>
                Go to random unrated conversation
            </a>
        </nav>
    {:else if groupedData.length === 0}
        <p>Loading data...</p>
    {:else}
        <p>No unrated conversations available.</p>
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
