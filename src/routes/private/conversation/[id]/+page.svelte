<script lang="ts">
    import { createClient } from "@supabase/supabase-js";
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { afterNavigate, goto } from "$app/navigation";
    import ConversationComponent from "$lib/ConversationComponent.svelte";
    import type { Database } from "$lib/supabase-types";
    import { fetchRandomConversation } from "$lib";
    import ProgressBar from "$lib/ProgressBar.svelte";
    import confetti from 'canvas-confetti';

    export let data;

    let supabase = data.supabase;

    let conversation = null;
    let ratedConversations = 0;
    let loading = true;
    let showBigRewardNotification = false;

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
                        .from("bridge_convo_copy")
                        .select("*")
                        .eq("conversation_id", id),
                    supabase
                        .from("bridge_response_copy")
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

    function triggerConfetti() {
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });
    }

    function triggerBigReward() {
        const duration = 15 * 1000;
        const animationEnd = Date.now() + duration;
        const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

        function randomInRange(min, max) {
            return Math.random() * (max - min) + min;
        }

        const interval = setInterval(function() {
            const timeLeft = animationEnd - Date.now();

            if (timeLeft <= 0) {
                return clearInterval(interval);
            }

            const particleCount = 50 * (timeLeft / duration);
            
            confetti(Object.assign({}, defaults, { 
                particleCount, 
                origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
                colors: ['#ff0000', '#00ff00', '#0000ff'],
                emojis: ['🎉', '🎊', '🥳', '🎈'],
            }));
            confetti(Object.assign({}, defaults, { 
                particleCount, 
                origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
                colors: ['#ff0000', '#00ff00', '#0000ff'],
                emojis: ['🎉', '🎊', '🥳', '🎈'],
            }));
        }, 250);
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
            const newCount = count || 0;
            if (newCount % 100 === 0 && newCount > 0) {
                triggerBigReward();
                showBigRewardNotification = true;
            } else if (newCount % 10 === 0 && newCount > 0) {
                triggerConfetti();
            }
            ratedConversations = newCount;
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

    afterNavigate(() => {
       fetchRatedConversationsCount()
    });

    $: if ($page.params.id) {
        fetchConversation($page.params.id);
    }

    $: if (showBigRewardNotification) {
        setTimeout(() => {
            showBigRewardNotification = false;
        }, 5000); // Hide after 5 seconds
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

    {#if showBigRewardNotification}
        <div class="big-reward-notification">
            Wow! You've rated {ratedConversations} conversations! 🎉
        </div>
    {/if}
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

    .big-reward-notification {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #FFD700;
        color: #000;
        padding: 15px 30px;
        border-radius: 10px;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: bounceIn 0.5s;
    }

    @keyframes bounceIn {
        0% { transform: translateX(-50%) scale(0.1); opacity: 0; }
        60% { transform: translateX(-50%) scale(1.2); opacity: 1; }
        100% { transform: translateX(-50%) scale(1); }
    }
</style>
