<script lang="ts">
    import { createClient } from "@supabase/supabase-js";
    import SelectButton from "./SelectButton.svelte";
    import { onMount, afterUpdate } from "svelte";

    export let conversation;

    const supabase = createClient(
        "https://jryeokpjkidbgzscmrcj.supabase.co",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpyeWVva3Bqa2lkYmd6c2NtcmNqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU5ODQ3NjIsImV4cCI6MjA0MTU2MDc2Mn0.nLeYIrrnbkSVqKeY7XOZkgHxDYwDcQOSVwmzrZgQrMo",
    );

    let explains_concepts_0,
        explains_concepts_1,
        inspires_interest_0,
        inspires_interest_1,
        monitors_motivation_0,
        monitors_motivation_1,
        speaks_encouragingly_0,
        speaks_encouragingly_1,
        identifies_goal_0,
        identifies_goal_1;

    function resetRatings() {
        explains_concepts_0 = null;
        explains_concepts_1 = null;
        inspires_interest_0 = null;
        inspires_interest_1 = null;
        monitors_motivation_0 = null;
        monitors_motivation_1 = null;
        speaks_encouragingly_0 = null;
        speaks_encouragingly_1 = null;
        identifies_goal_0 = null;
        identifies_goal_1 = null;
    }

    $: {
        if (conversation) {
            resetRatings();
        }
    }

    $: isFormComplete =
        explains_concepts_0 !== null &&
        explains_concepts_1 !== null &&
        inspires_interest_0 !== null &&
        inspires_interest_1 !== null &&
        monitors_motivation_0 !== null &&
        monitors_motivation_1 !== null &&
        speaks_encouragingly_0 !== null &&
        speaks_encouragingly_1 !== null &&
        identifies_goal_0 !== null &&
        identifies_goal_1 !== null;

    async function submitRating() {
        if (!isFormComplete) {
            alert("Please complete all ratings before submitting.");
            return;
        }

        const { data, error } = await supabase
            .from("bridge")
            .update({
                explains_concepts_0,
                explains_concepts_1,
                inspires_interest_0,
                inspires_interest_1,
                monitors_motivation_0,
                monitors_motivation_1,
                speaks_encouragingly_0,
                speaks_encouragingly_1,
                identifies_goal_0,
                identifies_goal_1,
            })
            .eq("conversation_id", conversation.conversation_id);

        if (error) {
            console.error("Error updating rating:", error);
            alert("Error updating rating. Please try again.");
        } else {
            alert("Rating submitted successfully!");
        }
    }

    onMount(() => {
        resetRatings();
    });
</script>

<div class="container">
    <div class="conversation-box">
        <h3>Conversation</h3>
        {#each conversation.convos as convo}
            <p><strong>{convo.user.toUpperCase()}:</strong> {convo.text}</p>
        {/each}
    </div>
    <div class="response-box">
        <h3>Tutor Response:</h3>
        {#each conversation.responses as response}
            <p>{response.text}</p>
        {/each}
    </div>
    <div class="rating-box">
        <h3>Rate this conversation</h3>
        <p class="instruction">
            For the following attributes, please annotate if the tutor should
            demonstrate the attribute at their specific point of progress in the
            conversation, and then whether the tutor actually demonstrates that
            attribute.
        </p>

        <div class="attribute">
            <p>
                Explains the underlying concepts or skills in a clear way that
                is easy for the student to understand
            </p>
            <div class="rating-row">
                <span>Should demonstrate:</span>
                <SelectButton bind:value={explains_concepts_0} />
            </div>
            <div class="rating-row">
                <span>Actually demonstrates:</span>
                <SelectButton bind:value={explains_concepts_1} />
            </div>
        </div>

        <div class="attribute">
            <p>
                Inspires and stimulates the interest or curiosity of the student
            </p>
            <div class="rating-row">
                <span>Should demonstrate:</span>
                <SelectButton bind:value={inspires_interest_0} />
            </div>
            <div class="rating-row">
                <span>Actually demonstrates:</span>
                <SelectButton bind:value={inspires_interest_1} />
            </div>
        </div>

        <div class="attribute">
            <p>
                Monitors the student's motivational state and adjusts responses
                accordingly
            </p>
            <div class="rating-row">
                <span>Should demonstrate:</span>
                <SelectButton bind:value={monitors_motivation_0} />
            </div>
            <div class="rating-row">
                <span>Actually demonstrates:</span>
                <SelectButton bind:value={monitors_motivation_1} />
            </div>
        </div>

        <div class="attribute">
            <p>
                Delivers feedback (whether positive or negative) in an
                encouraging way
            </p>
            <div class="rating-row">
                <span>Should demonstrate:</span>
                <SelectButton bind:value={speaks_encouragingly_0} />
            </div>
            <div class="rating-row">
                <span>Actually demonstrates:</span>
                <SelectButton bind:value={speaks_encouragingly_1} />
            </div>
        </div>

        <div class="attribute">
            <p>Identifies the student's goal or prior knowledge</p>
            <div class="rating-row">
                <span>Should demonstrate:</span>
                <SelectButton bind:value={identifies_goal_0} />
            </div>
            <div class="rating-row">
                <span>Actually demonstrates:</span>
                <SelectButton bind:value={identifies_goal_1} />
            </div>
        </div>
    </div>
    <div class="button-container">
        <button on:click={submitRating} disabled={!isFormComplete}
            >Submit</button
        >
    </div>
</div>

<style>
    .container {
        max-width: 800px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
    }
    .conversation-box,
    .response-box,
    .rating-box {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin: 20px 0;
        padding: 20px;
    }
    h3 {
        margin-top: 0;
        color: #333;
    }
    .instruction {
        font-style: italic;
        color: #666;
    }
    .attribute {
        margin-bottom: 20px;
    }
    .rating-row {
        display: flex;
        align-items: center;
        margin: 10px 0;
    }
    .rating-row span {
        width: 200px;
    }
    button {
        background-color: #427afd;
        border: none;
        color: white;
        padding: 15px 25px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 18px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 10px;
        transition: background-color 0.3s;
    }
    button:hover {
        background-color: #3062d7;
    }
    button:disabled {
        background-color: #cccccc;
        cursor: not-allowergb(155, 155, 155);        
        color: white;
    }

    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
</style>
